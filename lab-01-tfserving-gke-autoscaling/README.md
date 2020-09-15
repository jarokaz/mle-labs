## Lab Overview
## Setup and Requirements

Set the project ID

```
PROJECT_ID=mlops-dev-env
gcloud config set project $PROJECT_ID
```

## Creating a Kubernetes cluster 

Set the name and the zone for your cluster

```
CLUSTER_NAME=lab1-cluster
ZONE=us-central1-a
```

Create a GKE cluster with a default node pool.

```
gcloud beta container clusters create $CLUSTER_NAME \
  --project=$PROJECT_ID \
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

### Create a GKE node pool for TF Serving. 

The node pool is configured with cluster autoscaling.

```
NODE_POOL_NAME=tf-serving

gcloud container node-pools create $NODE_POOL_NAME \
--cluster $CLUSTER_NAME \
--zone $ZONE \
--machine-type n1-standard-4 \
--enable-autoscaling \
--min-nodes 1 \
--max-nodes 3 \
--num-nodes 1
```

Verify that the node pool has been provisioned. 

```
kubectl get nodes
```
You should see one node where the name starts with the prefix `gke-lab1-cluster-tf-serving`.

### Deploy TF Serving

TF Serving is deployed as a Kubernetes Deployment and exposed as a Kubernetes Service. 
The number of replicas in the deployment is controlled by Horizontal Pod Autoscaler based on 
the CPU utilization metrics.

To create TF Serving Deployment.

```
kubectl apply -f tf-serving/tfserving-deployment.yaml
```

To create  TF Serving Service.

```
kubectl apply -f tf-serving/tfserving-service.yaml
```

To create Horizontal Pod Autoscaler.

```
kubectl apply -f tf-serving/tfserving-hpa.yaml
```



