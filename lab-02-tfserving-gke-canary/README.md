# Progressive delivery of TF Serving deployments  with GKE and Istio

## Introduction

Istio is an open source framework for connecting, securing, and managing microservices, including services running on Google Kubernetes Engine (GKE). It lets you create a network of deployed services with load balancing, service-to-service authentication, monitoring, and more, without requiring any changes in service code.

This lab shows you how to use Istio on Kubernetes Engine to facilitate progressive delivery of TensorFlow machine learning model served through TF Serving.




## Setup and Requirements

### Qwiklabs setup

### Activate Cloud Shell

## Set up your GKE cluster


Set the project ID

```
PROJECT_ID=jk-mlops-dev
gcloud config set project $PROJECT_ID
gcloud config set compute/zone us-central1-f
```

### Creating a Kubernetes cluster with Istio

Set the name and the zone for your cluster

```
CLUSTER_NAME=lab2-cluster
```

Create a GKE cluster with Istio enabled and with mTLS in permissive mode:

```
gcloud beta container clusters create $CLUSTER_NAME \
  --project=$PROJECT_ID \
  --addons=Istio \
  --istio-config=auth=MTLS_PERMISSIVE \
  --cluster-version=latest \
  --machine-type=n1-standard-4 \
  --num-nodes=3 

```

### Verifying the installation

Check that the cluster is up and running

```
gcloud container clusters list
```

Get the credentials for you new cluster so you can interact with it using `kubectl`.

```
gcloud container clusters get-credentials $CLUSTER_NAME
```

Ensure the following Kubernetes services are deployed: `istio-citadel`, `istio-egressgateway`, `istio-pilot`, `istio-ingressgateway`, `istio-policy`, `istio-sidecar-injector`, and `istio-telemetry`

```
kubectl get service -n istio-system
```

Ensure that the corresponding Kubernetes Pods are deployed and all containers are up and running: `istio-pilot-*`, `istio-policy-*`, `istio-telemetry-*`, `istio-egressgateway-*`, `istio-ingressgateway-*`, `istio-sidecar-injector-*`, and `istio-citadel-*`

```
kubectl get pods -n istio-system
```

## Deploying ResNet models

Update and create the ConfigMap with the location of ResNet50 and ResNet101 SavedModels

```
kubectl apply -f tf-serving/tfserving-configmap.yaml
```

Create deployments for ResNet101 and ResNet50 models.

```
kubectl apply -f tf-serving/tfserving-deployment.yaml
```

Create the service that load balances between both models

```
kubectl apply -f tf-serving/tfserving-service.yaml
```

Verify that the services load balances between both ResNet50 and ResNet101 pods
```
TBD
```

Get the external address for the image classifier service.

```
kubectl get svc image-classifier
```

Submit the request to the service

```
curl -d @locust/request-body.json -X POST http://[EXTERNAL_IP]:8501/v1/models/image_classifier:predict
```

Repeat a few times. Notice that not all the responses are the same. This is due to load balancing between different models.


