## Lab Overview
## Setup and Requirements

Set the project ID

```
PROJECT_ID=mlops-dev-env
gcloud config set project $PROJECT_ID
```

## Creating a Kubernetes cluster with Istio

Set the name and the zone for your cluster

```
CLUSTER_NAME=lab2-cluster
ZONE=us-central1-a
```

Create a GKE cluster with Istio enabled and with mTLS in permissive mode:

```
gcloud beta container clusters create $CLUSTER_NAME \
  --project=$PROJECT_ID \
  --addons=Istio \
  --istio-config=auth=MTLS_PERMISSIVE \
  --cluster-version=latest \
  --machine-type=n1-standard-4 \
  --num-nodes=3 \
  --zone=$ZONE

```

## Verifying the installation

Check that the cluster is up and running

```
gcloud container clusters list
```

Get the credentials for you new cluster so you can interact with it using `kubectl`.

```
gcloud container clusters get-credentials $CLUSTER_NAME --zone $ZONE
```

Ensure the following Kubernetes services are deployed: `istio-citadel`, `istio-egressgateway`, `istio-pilot`, `istio-ingressgateway`, `istio-policy`, `istio-sidecar-injector`, and `istio-telemetry`

```
kubectl get service -n istio-system
```

Ensure that the corresponding Kubernetes Pods are deployed and all containers are up and running: `istio-pilot-*`, `istio-policy-*`, `istio-telemetry-*`, `istio-egressgateway-*`, `istio-ingressgateway-*`, `istio-sidecar-injector-*`, and `istio-citadel-*`

```
kubectl get pods -n istio-system
```

## Deploying Locust load testing tool

Build a docker image with Locust runtime, scripts, and configurations.

```
docker build -t gcr.io/$PROJECT_ID/locust locust/locust-image
```

Deploy Locust to your GKE cluster

```
docker push gcr.io/$PROJECT_ID/locust
```

Update the `newName` field in the `images` section of the `locust/manifests/kustomization.yaml` file with the name of your image - `gcr.io/<YOUR_PROJECT_ID>/locust:latest`.

Deploy Locust.

```
kubectl apply -k locust/manifests
```
