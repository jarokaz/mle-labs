IPADDRESS=${1:-10.138.0.5}
DURATION=${2:-1m}
QPS=${3:-10}
CONNECTIONS=${4:-5}
CONCURRENCY=${5:-5}
TIMEOUT=1000ms
./ghz  --insecure --protoset ./tfserving.protoset --call tensorflow.serving.PredictionService.Predict -D resnet_serving_request.json \
  --timeout $TIMEOUT \
  --duration $DURATION \
  --connections $CONNECTIONS \
  --concurrency $CONCURRENCY \
  --qps $QPS \
  ${IPADDRESS}:8500