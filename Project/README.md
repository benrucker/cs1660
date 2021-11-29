# Microservices Matrix (Project Option 1)

## Steps

1. Activate GKE
2. Make a default cluster
3. Authenticate a cloud shell to the Kubernetes cluster
    1. Navigate to your Kubernetes cluster list
    2. Click the name of your new cluster
    3. Click `Connect`
    4. Give yourself command-line access to either a local terminal or a gcloud shell
4. Pull this repo to the shell that is authenticated with `kubectl`
```sh
git clone https://github.com/benrucker/cs1660
```
5. cd to the config folder
```sh
cd cs1660/Project/Kubernetes\ Configs
```
6. Run the startup script
```sh
# on windows:
./startup.ps1

# on a Unix machine:
./startup.sh
```
7. Wait for the `flask` pod to begin. This is our GUI front-end microservice that allows us to use the microservices. (Though the old terminal application still exists as `frontend`, it is not updated with full functionality and should not be used)
```sh
kubectl get pods -w
```
8. Connect to the `flask` service
    * This can be done through the GCP UI:
        1. Navigate to the Kubernetes cluster
        2. Click "Services & Ingress"
        3. Click on the external URL to the `flask` service
    * Or using `kubectl`:
        1. Run `kubectl get services`
        2. Copy the `External URL` of the `flask` service
        3. Paste it into the URL bar of your browser and append the port of the service (`5000` by default)
            * e.g. `11.11.11.11:5000`
9. Run the microservice you desire! 🎉

## Credentials

### Spark

Username: admin

Password: cs1660

### Jupyter

Password: cs1660


## Video Demo

https://user-images.githubusercontent.com/12519846/143804180-e32766de-c0e7-4660-9cc6-6067527045e0.mp4

