import subprocess
import time
import json

print('anything')


# POST api/users/change_password
while True:
    try:
        print('0000000000000000000 checking if sonar is up')
        running = subprocess.run(
            [
                "curl", "http://localhost:9000/api/system/status", "-X", "GET"
            ], capture_output=True
        )
        if json.loads(running.stdout.decode("utf-8"))["status"] != "UP":
            raise Exception("Sonar is not running")
        else:
            print('0000000000000000000 sonar is up')
        posted = subprocess.run(
            [
                "curl", "-u", "admin:admin", "-d", "login=admin", "-d", "password=password", "-d", "previousPassword=admin", "-v", "http://localhost:9000/api/users/change_password"
            ], check=True, capture_output=True
        )
        print(f'0000000000000000000 {posted.stdout}')
        print(f'0000000000000000000 {posted}')
        break
    except subprocess.CalledProcessError:
        print('0000000000000000000 Assuming that SonarQube has not launched yet.')
        print('0000000000000000000 Rertrying change password in 5 seconds...')
        time.sleep(5)
    except Exception as e:
        print('0000000000000000000', e)
        time.sleep(5)
