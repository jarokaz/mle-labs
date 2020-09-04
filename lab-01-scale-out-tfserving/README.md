# Using Kubernetes to deployed a scaled-out configuration of TensorFlow Serving

### Download the ResNet101 model

```
cd ~/mle-labs/lab-01-scale-out-tfserving/serving-images
SOURCE_DIR=gs://mlops-dev-workspace/models/resnet_serving/1
LOCAL_DIR=resnet_serving
mkdir $LOCAL_DIR
gsutil cp -R $SOURCE_DIR $LOCAL_DIR
```

### Build the serving image

```
PROJECT_ID=mlops-dev-env
IMAGE=gcr.io/${PROJECT_ID}/lab-01-tfserving
docker build -t ${IMAGE} .
docker push
```

