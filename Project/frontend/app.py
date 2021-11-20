import subprocess
import hashlib
# look into https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/

def launch_service(service):
    SERVICES[service]()


def hadoop():
    pass


def jupyter():
    pass


def spark():
    pass


def sonar():
    print("Would you like to\n\n\t(1) download and analyze a project or (2) go straight to SonarQube?")
    choice = input("> ")
    if choice == "1":
        get_project()

    subprocess.run(['xdg-open', "sonar.svc.cluster.local:9000"], check=True)
    pass


def get_project():
    print("Please enter the remote git URL to the project you would like to analyze.\n\te.g. https://github.com/benrucker/cs1660")
    path = input("> ")
    hashpath = hashlib.sha256(path.encode()).hexdigest()
    exists = subprocess.run(
        [
            "kubectl", "exec", "sonar", "--",
            "test -d " + hashpath
        ]
    )
    if exists.returncode == 0:
        pull = subprocess.run(
            [
                "kubectl", "exec", "sonar", "--",
                "cd " + hashpath + " && git pull"
            ]
        )
    else:
        result = subprocess.run(
            [
                "kubectl", "exec", "sonar", "--",
                "git", "clone", path, "--depth=1", "--recurse-submodules", "--progress", hashpath, "--",
            ], check=True, stdout=subprocess.PIPE
        )
    result = subprocess.run(
        [
            "kubectl", "exec", "sonar", "--",
            "curl", "--data-urlencode", f"name={hashpath}&project={hashpath}", "http://localhost:9000/api/projects/create"
        ], check=True, stdout=subprocess.PIPE
    )
    result = subprocess.run(
        [
            "kubectl", "exec", "sonar", "--",
            "sonar-scanner", f"-Dsonar.projectkey={hashpath}", f"-Dsonar.projectName={hashpath}", "-Dsonar.login=admin", "-Dsonar.password=password", f"-Dsonar.projectBaseDir={hashpath}", "-Dsonar.cobol.copy.directories=/copy"
        ], check=True, stdout=subprocess.PIPE
    )


SERVICES = {
    'Hadoop': hadoop,
    'Jupyter Notebook': jupyter,
    'Apache Spark': spark,
    'SonarQube & SonarScanner': sonar,
}

if __name__ == '__main__':
    print('Welcome to the Microservices Matrix! Which tool would you like to open?')

    for i, service in enumerate(SERVICES):
        print(f'{i+1}: {service}')

    choice = int(input('> ')) - 1

    print(f'Launching {SERVICES[choice]}...')
    
    launch_service(SERVICES[choice])
