import os
import json

status_in = json.load(open('data/status.json')) 
status_out = []
bigdata_status_dict = json.load(open(os.path.join(os.path.dirname(__file__), 'status_dict.json')))

for dataset in status_in:
    if dataset['datagetter_metadata'].get('file_size', 0) >= 10 * 1024 * 1024:
        dataset = bigdata_status_dict[dataset['identifier']]
    status_out.append(dataset)

with open('data/status.json', 'w') as fp:
    json.dump(status_out, fp, indent='  ', sort_keys=True)
