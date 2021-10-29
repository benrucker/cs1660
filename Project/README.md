# Project (Option 1 - Kubernetes Cluster)

## Docker Image Info:

* Terminal app:
    * https://hub.docker.com/repository/docker/brucker/frontend
    * [frontend/](frontend/)
* Spark:
    * https://hub.docker.com/repository/docker/brucker/spark
    * [spark/](spark/)
* Hadoop:
    * https://hub.docker.com/repository/docker/brucker/hadoop
    * [hadoop/](hadoop/)
* Jupyter Notebook:
    * https://hub.docker.com/repository/docker/brucker/datascience-notebook
    * [jupyternb/](jupyternb/)
* SonarQube & SonarScanner
    * https://hub.docker.com/r/sonarsource/sonar-scanner-cli
    * [sonar/](sonar/)

## Screenshot

![screenie](Containers%20Active.png)

## Steps

## Steps to make this happen

1. Activate GKE
2. Make a default cluster
3. Authenticate a cloud shell to the cluster
4. Pull this repo to the shell
5. cd to the config folder
```sh
cd cs1660/Project/Kubernetes\ Configs
```
6. use kubectl to make the pods
```sh
kubectl apply -f pod-frontend.yaml
kubectl apply -f pod-hadoop.yaml
kubectl apply -f pod-jupyter.yaml
kubectl apply -f pod-sonar.yaml
kubectl apply -f pod-spark.yaml
```
7. Wait for the pods to begin
```sh
watch kubectl get all
```
8. Connect to the frontend pod
```sh
kubectl exec --stdin --tty pod/frontend -- /bin/sh
```
9. Run the terminal app
```sh
python app.py
```
10. Done! 🎉