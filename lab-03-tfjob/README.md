# Distributed TensorFlow training on Kubernetes



## Setup and Requirements

### Qwiklabs setup

### Activate Cloud Shell

## Setting up your GKE cluster


Set the project ID

```
PROJECT_ID=$(gcloud config get-value project)
gcloud config set project $PROJECT_ID
gcloud config set compute/zone us-central1-f
```

### Creating a Kubernetes cluster 

Set the name and the zone for your cluster

```
CLUSTER_NAME=cluster-1

gcloud beta container clusters create $CLUSTER_NAME \
  --project=$PROJECT_ID \
  --cluster-version=latest \
  --machine-type=n1-standard-8 \
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



## Installing TensorFlow Training (TFJob)

### Get TensorFlow Training manifests

Get the manifests for TensorFlow Training from v1.1.0 of Kubeflow.
```
SRC_REPO=https://github.com/kubeflow/manifests
kpt pkg get $SRC_REPO/tf-training@v1.1.0 tf-training
```

### Create the `kubeflow` namespace

```
kubectl create namespace kubeflow
```

### Install the TFJob CRD

```
 kubectl apply  --kustomize tf-training/tf-job-crds/base
```

### Install the TFJob operator
```
kubectl apply  --kustomize tf-training/tf-job-operator/base
```

### Verify installation
```
kubectl get pods -n kubeflow
```

## Running and monitoring distributed jobs

### Copy lab files

```
SRC_REPO=https://github.com/jarokaz/mle-labs
kpt pkg get $SRC_REPO/lab-03-tfjob lab-files
cd lab-files
```

### Build a training container
```
cd train-app
IMAGE_NAME=mnist-train

docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME} .
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}
```

### Submit a training job
```
cd ..
kubectl apply -f tfjob.yaml
```

### Monitor the job
```
kubectl describe tfjob multi-worker
```

```
kubectl logs --follow multi-worker-worker-0
```

```
kubectl get pods
```


### Delete the job
```
kubectl delete tfjob multi-worker
```
