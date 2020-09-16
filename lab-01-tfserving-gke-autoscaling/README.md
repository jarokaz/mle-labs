## Lab Overview

TBD

TF Serving is deployed as a Kubernetes Deployment and exposed as a Kubernetes Service. 
The number of replicas in the deployment is controlled by Horizontal Pod Autoscaler based on 
the CPU utilization metrics.


## Setup and Requirements

Set the default compute zone

```
PROJECT_ID=mlops-dev-env
gcloud config set compute/zone us-central1-f
```

## Creating a Kubernetes cluster

To create a new cluster with 3 nodes in the default node pool, run the following command.


```
CLUSTER_NAME=tfserving-cluster

gcloud beta container clusters create $CLUSTER_NAME \
  --cluster-version=latest \
  --machine-type=n1-standard-4 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --num-nodes=1 
```

Check that the cluster is up and running

```
gcloud container clusters list
```

Get the credentials for you new cluster so you can interact with it using `kubectl`.

```
gcloud container clusters get-credentials $CLUSTER_NAME 
```

List the cluster's nodes.

```
kubectl get nodes
```

Notice that the cluster has only one node.


## Deploying Locust load testing tool

Build a docker image with Locust runtime, scripts, and configurations.

```
docker build -t gcr.io/$PROJECT_ID/locust locust/locust-image
```

Push the image to your project's Container Registry.

```
docker push gcr.io/$PROJECT_ID/locust
```

Update the `newName` field in the `images` section of the `locust/manifests/kustomization.yaml` file with the name of your image - `gcr.io/<YOUR_PROJECT_ID>/locust:latest`.

Deploy Locust.

```
kubectl apply -k locust/manifests
```

Retrieve the external IP address to Locust web interface.

```
kubectl get service locust-master
```
You may need to wait a couple of minutes before the IP address is available

To connect to Locust web interface navigate to 
```
http://[EXTERNAL-IP]:8089
```

## Deploying TF Serving and ResNet101 serving model.


Update and create the ConfigMap with the resnet_serving model location.

```
kubectl apply -f tf-serving/tfserving-configmap.yaml
```

Create TF Serving Deployment.

```
kubectl apply -f tf-serving/tfserving-deployment.yaml
```

Create Horizontal Pod Autoscaler.

```
kubectl apply -f tf-serving/tfserving-hpa.yaml
```

Create  TF Serving Service.

```
kubectl apply -f tf-serving/tfserving-service.yaml
```

Get the external address for the TF Serving service

```
kubectl get svc tf-serving
```

Validate that the model has been deployed.

```
curl -d @locust/locust-image/test-config/request-body.json -X POST http://[EXTERNAL_IP]:8501/v1/models/resnet_serving:predict
```

## Load test the model

```
cd locust
locust -f tasks.py --headless --users 32 --spawn-rate 1 --step-load --step-users 1 --step-time 30s --host http://[EXTERNAL_IP]:8501
```

Observe the TF Serving Deployment in GKE dashboard.

