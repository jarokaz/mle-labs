import os
import json


#tf_config = os.environ.get('TF_CONFIG')
#print(tf_config)
#tf_config_dict = json.loads(tf_config)
#print(tf_config_dict)

TF_CONFIG='{"cluster": {"worker": ["localhost:12345", "localhost:23456"]}, "task": {"type": "worker","index": 1}}'

print(TF_CONFIG)