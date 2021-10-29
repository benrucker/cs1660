SERVICES = ['Hadoop', 'Jupyter Notebook', 'Apache Spark', 'SonarQube & SonarScanner']
# look into https://kubernetes.io/docs/tasks/debug-application-cluster/get-shell-running-container/

def launch_service(service):
    match service:
        case 'Hadoop':
            pass
        case 'Jupyter Notebook':
            pass
        case 'Apache Spark':
            pass
        case 'SonarQube & SonarScanner':
            pass


if __name__ == '__main__':
    print('Welcome to the Microservices Matrix! Which tool would you like to open?')

    for i, service in enumerate(SERVICES):
        print(f'{i+1}: {service}')

    choice = int(input('> ')) - 1

    print(f'Launching {SERVICES[choice]}...')
    
    launch_service(SERVICES[choice])
