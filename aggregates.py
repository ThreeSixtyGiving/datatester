import json
from cove_360.lib.threesixtygiving import get_grants_aggregates

def none_keys_to_str(x):
    '''
    Walk a dict or list and replace any `None` keys with `'None'`.

    Replacement is done in place.

    '''
    if hasattr(x, 'items'):
        for key, value in x.items():
            if key is None:
                del x[key]
                x[str(key)] = value
            none_keys_to_str(value)
    elif isinstance(x, str):
        return
    elif hasattr(x, '__iter__'):
        for item in x:
            none_keys_to_str(item)

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
    none_keys_to_str(dataset)
    stats.append(dataset)
    with open('data/status.json', 'w') as fp:
        json.dump(stats, fp, indent='  ', sort_keys=True)
