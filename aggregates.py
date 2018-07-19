import json
from cove_360.lib.threesixtygiving import get_grants_aggregates

data_all = json.load(open('data/data_all.json')) 
stats = []

for dataset in data_all:
    json_filename = dataset['datagetter_metadata'].get('json')
    if json_filename:
        with open(json_filename) as fp:
            aggregates = get_grants_aggregates(json.load(fp))
        # replace sets with counts
        for k, v in list(aggregates.items()):
            if isinstance(v, set):
                aggregates[k+'_count'] = len(v)
                if k == 'distinct_funding_org_identifier':
                    aggregates[k] = sorted(list(aggregates[k]))
                else:
                    del aggregates[k]
        aggregates = {k:sorted(list(v)) if isinstance(v, set) else v for k,v in aggregates.items()}
        dataset['datagetter_aggregates'] = aggregates
    stats.append(dataset)
    with open('data/status.json', 'w') as fp:
        json.dump(stats, fp, indent='  ', sort_keys=True)
