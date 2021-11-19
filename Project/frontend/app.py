import subprocess
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
    print("Would you like to (1) analyze a new project or (2) go straight to SonarQube?")
    choice = input("> ")
    if choice == "1":
        print("Please enter the path to the project you would like to analyze.")
        path = input("> ")
        result = subprocess.run(
            [
                "kubectl", "exec", "sonar", "--",
                "curl", "--data-urlencode", f"name={path}&project={path}", "http://localhost:9000/api/projects/create", "-X", "POST"
            ], check=True, stdout=subprocess.PIPE
        )
        result = subprocess.run(
            [
                "kubectl", "exec", "sonar", "--",
                "sonar-scanner", path # add the rest of the arguments, login, project, etc
            ], check=True, stdout=subprocess.PIPE
        )
    #
    # unconditionally go to sonarqube
    # get path to sonarqube pod
    subprocess.run(['xdg-open', "sonar.svc.cluster.local:9000"], check=True)
    pass


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
