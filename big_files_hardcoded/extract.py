import os
import json

data_all = json.load(open('data/status.json')) 
status_dict = {}

for dataset in data_all:
    if dataset['datagetter_metadata'].get('file_size', 0) >= 10 * 1024 * 1024:
        status_dict[dataset['identifier']] = dataset

with open(os.path.join(os.path.dirname(__file__), 'status_dict.json'), 'w') as fp:
    json.dump(status_dict, fp, indent='  ', sort_keys=True)
