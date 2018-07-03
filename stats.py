import json
from cove_360.lib.threesixtygiving import get_grants_aggregates

data_all = json.load(open('data/data_all.json')) 
stats = []

for dataset in data_all:
    json_filename = dataset['datagetter_metadata'].get('json')
    if not json_filename:
        continue
    with open(json_filename) as fp:
        aggregates = get_grants_aggregates(json.load(fp))
    # replace sets with counts
    for k, v in aggregates.items():
        if isinstance(v, set):
            aggregates[k+'_count'] = len(v)
            del aggregates[k]
    aggregates = {k:sorted(list(v)) if isinstance(v, set) else v for k,v in aggregates.items()}
    stats.append(aggregates)
    with open('data/stats.json', 'w') as fp:
        json.dump(stats, fp, indent='  ')
        
