# Microservices Matrix (Project Option 1 - Kubernetes Cluster)

## Steps

1. Activate GKE
2. Make a default cluster
3. Authenticate a cloud shell to the Kubernetes cluster
    * i.e. grant access to using `kubectl` on either a local terminal or on a cloud shell
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
7. Wait for the `flask` pod to begin
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


## Video Demo

https://user-images.githubusercontent.com/12519846/143804180-e32766de-c0e7-4660-9cc6-6067527045e0.mp4

