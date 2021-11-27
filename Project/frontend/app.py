import subprocess
import hashlib
import time
import os

from kubernetes import config
from kubernetes.client import Configuration, ApiClient
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream
# look into https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/

# TODO add services configs for all pods
# TODO if `xdg-open` doesn't exist, use `start` instead
# TODO replace local hostnames with external hostnames
# can we even use xdg-open or start?
# if not, just print out the URL for the user to paste into their browser
# that, or convert to a web server


def launch_service(service, api_instance):
    service(api_instance)


def hadoop(api_instance):
    show_lb_url(api_instance, 'namenode', 'Apache Hadoop')


def jupyter(api_instance):
    show_lb_url(api_instance, 'jupyter', 'Jupyter Notebook')


def spark(api_instance):
    show_lb_url(api_instance, 'spark', 'Apache Spark')


def sonar(api_instance):
    print("Would you like to\n\n\t(1) download and analyze a project or (2) go straight to SonarQube?")
    choice = input("> ")
    if choice == "1":
        get_project(api_instance)

    show_lb_url(api_instance, 'sonar', 'SonarQube')


def get_project(api_instance):
    print("Please enter the remote git URL to the project you would like to analyze.\n\te.g. https://github.com/benrucker/cs1660")
    path = input("> ")
    hashpath = hashlib.sha256(path.encode()).hexdigest()
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  'sonar',
                  'default',
                  command=['sh'],
                  stderr=True, stdin=True,
                  stdout=True, tty=False,
                  _preload_content=False)
    command = "test -d " + hashpath + '&& echo $?'
    resp.write_stdin(command + '\n')
    return_code = resp.read_stdout(timeout=10)
    print(return_code)
    if len(return_code) != 0:
        command = "cd " + hashpath + " && git pull"
        resp.write_stdin(command + '\n')
        output = resp.read_stdout(timeout=120)
        print(output)
    else:
        command = "git clone " + path + " --depth=1 --recurse-submodules --progress " + hashpath
        resp.write_stdin(command + '\n')
        output = resp.read_stdout(timeout=120)
        print(output)
    command = f"curl --data-urlencode name={hashpath}&project={hashpath} http://localhost:9000/api/projects/create"
    resp.write_stdin(command + '\n')
    output = resp.read_stdout(timeout=120)
    print(output)
    command = f"sonar-scanner -Dsonar.projectkey={hashpath} -Dsonar.projectName={hashpath} -Dsonar.login=admin -Dsonar.password=password -Dsonar.projectBaseDir={hashpath} -Dsonar.cobol.copy.directories=/copy"
    resp.write_stdin(command + '\n')
    output = resp.read_stdout(timeout=120)
    print(output)


def show_lb_url(api_instance, name, pretty_name):
    service = api_instance.read_namespaced_service(name, 'default')
    ip = service.status.load_balancer.ingress[0].ip
    port = service.spec.ports[0].port
    print(f"Open {pretty_name} by clicking this link or pasting it in your browser:")
    print(f"\thttp://{ip}:{port}")


def wait_for_all_launches(api_instance):
    global hadoop_pod, jupyter_pod, spark_pod, sonar_pod
    wait_for_hadoop(api_instance)
    jupyter_pod = wait_for_launch(api_instance, 'jupyter')
    spark_pod = wait_for_launch(api_instance, 'spark')
    spark_worker_pod = wait_for_launch(api_instance, 'spark-worker')
    sonar_pod = wait_for_launch(api_instance, 'sonar')


def wait_for_hadoop(api):
    wait_for_launch(api, 'namenode')
    wait_for_launch(api, 'datanode')
    wait_for_launch(api, 'datanode2')
    wait_for_launch(api, 'resourcemanager')
    wait_for_launch(api, 'nodemanager')


def wait_for_launch(api_instance, name):
    print(f"Waiting for {name} to launch...")
    while True:
        try:
            resp = api_instance.read_namespaced_pod(name=name,
                                                    namespace='default')
            if resp.status.phase != 'Pending':
                print(name, 'is running')
                return resp
            else:
                print(name, 'is pending')
                time.sleep(1)
        except ApiException as e:
            print(e)
            time.sleep(1)


def get_api():
    config.load_incluster_config()
    api = core_v1_api.CoreV1Api()
    return api


SERVICES = {
    'Hadoop': hadoop,
    'Jupyter Notebook': jupyter,
    'Apache Spark': spark,
    'SonarQube & SonarScanner': sonar,
}


if __name__ == '__main__':
    core_v1 = get_api()
    wait_for_all_launches(core_v1)

    print('Welcome to the Microservices Matrix! Which tool would you like to open?')

    indexed = list(SERVICES.keys())
    for i, service in enumerate(indexed):
        print(f'{i+1}: {service}')

    choice = int(input('> ')) - 1

    print(f'Launching {indexed[choice]}...')
    
    launch_service(SERVICES[indexed[choice]], core_v1)
