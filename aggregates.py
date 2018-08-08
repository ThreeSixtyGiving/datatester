import json
from cove_360.lib.threesixtygiving import get_grants_aggregates

def replace_none_keys(nested_data):
    '''
    Walk a dict or list and replace any `None` keys with `'None'`.

    Replacement is done in place.

    '''
    if hasattr(nested_data, 'items'):
        for key, value in nested_data.items():
            if key is None:
                del nested_data[key]
                nested_data[str(key)] = value
            replace_none_keys(value)
    elif isinstance(nested_data, str):
        return
    elif hasattr(nested_data, '__iter__'):
        for item in nested_data:
            replace_none_keys(item)

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
    replace_none_keys(dataset)
    stats.append(dataset)
    with open('data/status.json', 'w') as fp:
        json.dump(stats, fp, indent='  ', sort_keys=True)
