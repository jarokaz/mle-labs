IPADDRESS=${1:-10.138.0.5}
DURATION=${2:-1m}
QPS=${3:-1}
CONNECTIONS=${4:-1}
CONCURRENCY=${5:-1}
TIMEOUT=1000ms
./ghz  --insecure --protoset ./tfserving.protoset --call tensorflow.serving.PredictionService.Predict -D resnet_serving_request.json \
  --timeout $TIMEOUT \
  --duration $DURATION \
  --connections $CONNECTIONS \
  --concurrency $CONCURRENCY \
  --qps $QPS \
  ${IPADDRESS}:8500