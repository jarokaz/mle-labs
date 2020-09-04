# Using Kubernetes to deployed a scaled-out configuration of TensorFlow Serving

### Download the ResNet101 model

```
LOCAL_DIR=/tmp/resnet_serving
mkdir $LOCAL_DIR
gsutil cp -R gs://mlops-dev-workspace/models/resnet_serving/1 $LOCAL_DIR
```


