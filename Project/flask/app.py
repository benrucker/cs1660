import subprocess
import hashlib
import time
import os

from kubernetes import config
from kubernetes.client import Configuration, ApiClient
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream

import flask
from flask import (Flask, abort, g, redirect, render_template, request,
                   session, url_for)
from flask.wrappers import Request, Response
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)

app.config.update(dict(
    FLASK_ENV='development',
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin',
))


@app.route('/')
def index():
    api = get_api()
    all_running = are_all_running(api)
    service_urls = {
        'Hadoop': hadoop(api),
        'Jupyter': jupyter(api),
        'Spark': spark(api),
        'Sonar': sonar(api)
    }
    if not all_running:
        return render_template('wait.html')
    else:
        return render_template('index.html', service_urls=service_urls)


def launch_service(service, api_instance):
    service(api_instance)


def hadoop(api_instance):
    return get_lb_url(api_instance, 'namenode', 'Apache Hadoop')


def jupyter(api_instance):
    return get_lb_url(api_instance, 'jupyter', 'Jupyter Notebook')


def spark(api_instance):
    return get_lb_url(api_instance, 'spark', 'Apache Spark')


def sonar(api_instance):
    # print("Would you like to\n\n\t(1) download and analyze a project or (2) go straight to SonarQube?")
    # choice = input("> ")
    # if choice == "1":
    #     get_project(api_instance)

    return get_lb_url(api_instance, 'sonar', 'SonarQube')


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


def get_lb_url(api_instance, name, pretty_name):
    service = api_instance.read_namespaced_service(name, 'default')
    ip = service.status.load_balancer.ingress[0].ip
    port = service.spec.ports[0].port
    return f"\thttp://{ip}:{port}"


def are_all_running(api_instance):
    global hadoop_pod, jupyter_pod, spark_pod, sonar_pod
    return is_hadoop_running(api_instance) and \
        is_running(api_instance, 'jupyter') and \
        is_running(api_instance, 'spark') and \
        is_running(api_instance, 'spark-worker') and \
        is_running(api_instance, 'sonar')


def is_hadoop_running(api):
    return all([is_running(api, x) for x in [
        'namenode', 'datanode', 'datanode2', 
        'resourcemanager', 'nodemanager'
    ]])


def is_running(api_instance, name):
    print(f"Checking if {name} is running...")
    try:
        resp = api_instance.read_namespaced_pod(name=name,
                                                namespace='default')
        if resp.status.phase != 'Pending':
            print(name, 'is running')
            return True
        else:
            return False
    except ApiException as e:
        return False


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
    app.run(host='0.0.0.0', port=5000)