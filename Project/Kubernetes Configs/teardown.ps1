kubectl delete deployment/historyserver

kubectl delete pod/datanode
kubectl delete pod/datanode2
kubectl delete pod/flask
kubectl delete pod/frontend
kubectl delete pod/jupyter
kubectl delete pod/namenode
kubectl delete pod/nodemanager
kubectl delete pod/resourcemanager
kubectl delete pod/sonar
kubectl delete pod/spark
kubectl delete pod/spark-worker

kubectl delete pvc/datanode
kubectl delete pvc/datanode2
kubectl delete pvc/hadoop-historyserver
kubectl delete pvc/namenode

kubectl delete service/datanode
kubectl delete service/datanode2
kubectl delete service/flask
kubectl delete service/frontend
kubectl delete service/historyserver
kubectl delete service/jupyter
kubectl delete service/namenode
kubectl delete service/nodemanager
kubectl delete service/resourcemanager
kubectl delete service/sonar
kubectl delete service/spark
