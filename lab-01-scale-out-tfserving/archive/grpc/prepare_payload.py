import json
import tensorflow as tf
from tensorflow.python.framework import tensor_util
from tensorflow_serving.apis import predict_pb2
from google.protobuf import json_format

IMAGE_PATH = 'images/grace_hopper.jpg'
MODEL_NAME = 'resnet_serving'
MODEL_SIGNATURE = 'serving_preprocess'
JSON_REQUEST_PATH = 'resnet_serving_request.json'

def _get_image_bytes(image_path):
    """
    Reads image bytes from a file.
    """

    with open(image_path, 'rb') as f:
        image_content = f.read()

    return image_content

def _prepare_predict_request(image_path):
    """
    Prepares a JSON representation of TF Serving
    GRPC Predict request.
    """

    image_bytes = _get_image_bytes(image_path)
    predict_request = predict_pb2.PredictRequest()
    predict_request.model_spec.name = MODEL_NAME
    predict_request.model_spec.signature_name = MODEL_SIGNATURE
    predict_request.inputs['raw_images'].CopyFrom(
        tensor_util.make_tensor_proto( [image_bytes], tf.string))

    return json_format.MessageToJson(predict_request) 


if __name__ == '__main__':
    predict_request = _prepare_predict_request(IMAGE_PATH)
    print(type(predict_request))
    
    with open(JSON_REQUEST_PATH, 'w') as f:
        f.write(predict_request)