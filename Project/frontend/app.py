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
    SERVICES[service](api_instance)


def hadoop(api_instance):
    service = api_instance.get_namedspaced_service('hadoop-service', 'default')
    print(service)
    # subprocess.run(['xdg-open', "hadoop.svc.cluster.local:9000"], check=True)


def jupyter(api_instance):
    service = api_instance.get_namedspaced_service('jupyter-service', 'default')
    print(service)
    # subprocess.run(['xdg-open', "jupyter.svc.cluster.local:9000"], check=True)


def spark(api_instance):
    service = api_instance.get_namedspaced_service('spark-service', 'default')
    print(service)
    # subprocess.run(['xdg-open', "spark.svc.cluster.local:9000"], check=True)


def sonar(api_instance):
    print("Would you like to\n\n\t(1) download and analyze a project or (2) go straight to SonarQube?")
    choice = input("> ")
    if choice == "1":
        get_project(api_instance)

    service = api_instance.get_namedspaced_service('sonar-service', 'default')
    print(service)
    # subprocess.run(['xdg-open', "sonar.svc.cluster.local:9000"], check=True)


def get_project(api_instance):
    print("Please enter the remote git URL to the project you would like to analyze.\n\te.g. https://github.com/benrucker/cs1660")
    path = input("> ")
    hashpath = hashlib.sha256(path.encode()).hexdigest()
    command = [
            "/bin/sh",
            "-c",
            "test -d " + hashpath
        ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  'sonar',
                  'default',
                  command=command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print(resp)
    if resp.status == 0:
        command = [
                "/bin/sh",
                "-c",
                "cd " + hashpath + " && git pull"
        ]
        resp = stream(api_instance.connect_get_namespaced_pod_exec,
                      'sonar',
                      'default',
                      command=command,
                      stderr=True, stdin=False,
                      stdout=True, tty=False)
        print(resp)
    else:
        command = [
                "/bin/sh",
                "-c",
                "git", "clone", path, "--depth=1", "--recurse-submodules", "--progress", hashpath, "--",
            ]
        resp = stream(api_instance.connect_get_namespaced_pod_exec,
                      'sonar',
                      'default',
                      command=command,
                      stderr=True, stdin=False,
                      stdout=True, tty=False)
        print(resp)
    command = [
            "/bin/sh",
            "-c",
            "curl", "--data-urlencode", f"name={hashpath}&project={hashpath}", "http://localhost:9000/api/projects/create"
        ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  'sonar',
                  'default',
                  command=command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print(resp)
    command = [
            "/bin/sh",
            "-c",
            "sonar-scanner", f"-Dsonar.projectkey={hashpath}", f"-Dsonar.projectName={hashpath}", "-Dsonar.login=admin", "-Dsonar.password=password", f"-Dsonar.projectBaseDir={hashpath}", "-Dsonar.cobol.copy.directories=/copy"
        ]
    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  'sonar',
                  'default',
                  command=command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)
    print(resp)


def wait_for_all_launches(api_instance):
    global hadoop_pod, jupyter_pod, spark_pod, sonar_pod
    hadoop_pod = wait_for_launch(api_instance, 'hadoop')
    jupyter_pod = wait_for_launch(api_instance, 'jupyter')
    spark_pod = wait_for_launch(api_instance, 'spark')
    sonar_pod = wait_for_launch(api_instance, 'sonar')


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
                time.sleep(1)
        except ApiException as e:
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

    for i, service in enumerate(SERVICES):
        print(f'{i+1}: {service}')

    choice = int(input('> ')) - 1

    print(f'Launching {SERVICES[choice]}...')
    
    launch_service(SERVICES[choice], core_v1)
