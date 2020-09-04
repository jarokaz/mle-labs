# Using Kubernetes to deployed a scaled-out configuration of TensorFlow Serving

### Download the ResNet101 model

```
SOURCE_DIR=gs://mlops-dev-workspace/models/resnet_serving/1
LOCAL_DIR=/tmp/resnet_serving
mkdir $LOCAL_DIR
gsutil cp -R $SOURCE_DIR $LOCAL_DIR
```


