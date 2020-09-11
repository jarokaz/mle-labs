# Using Kubernetes to deploy a scaled-out configuration of TensorFlow Serving

### Add a node pool to host TF Serving Deployment
```
NAME=tf-serving
CLUSTER=lab1-cluster
ZONE=us-central1-a
MACHINE_TYPE=n1-standard-8
MIN_NODES=1
MAX_NODES=3
NUM_NODES=1

gcloud container node-pools create $NAME \
--cluster $CLUSTER \
--zone $ZONE \
--machine-type $MACHINE_TYPE \
--enable-autoscaling \
--min-nodes $MIN_NODES \
--max-nodes $MAX_NODES \
--num-nodes $NUM_NODES

gcloud container node-pools create $NAME \
--cluster $CLUSTER \
--zone $ZONE \
--machine-type $MACHINE_TYPE \
--num-nodes 1
```



