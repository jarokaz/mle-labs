# Using Kubernetes to deploy a scaled-out configuration of TensorFlow Serving

### Add a node pool to host TF Serving Deployment
```
NAME=tf-serving
CLUSTER=lab1-cluster
ZONE=us-central1-a
MACHINE_TYPE=n1-standard-4
NUM_NODES=2

gcloud container node-pools create $NAME \
--cluster $CLUSTER \
--zone $ZONE \
--machine-type $MACHINE_TYPE \
--num-nodes $NUM_NODES

```


