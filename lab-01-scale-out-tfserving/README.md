# Using Kubernetes to deployed a scaled-out configuration of TensorFlow Serving

### Download the ResNet101 model

```
LOCAL_DIR=/tmp/resnet101/1
mkdir $LOCAL_DIR
gsutil cp -R gs://mlops-dev-workspace/models/resnet_serving/ $LOCAL_DIR
```


