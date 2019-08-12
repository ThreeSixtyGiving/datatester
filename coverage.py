import os
import json
import collections

os.environ['DJANGO_SETTINGS_MODULE'] = 'cove_360.settings'

from libcove.lib.common import get_fields_present, fields_present_generator
from cove_360.lib.schema import Schema360


def unique_fields_present_generator(json_data):
    if not isinstance(json_data, dict):
        return
    if 'grants' not in json_data:
        return
    for grant in json_data['grants']:
        # Flatten the key,val pairs so we can make a unique list of fields
        field_list = [field for field, value in fields_present_generator(grant)]
        for field in set(field_list):
            yield '/grants' + field


def get_unique_fields_present(*args, **kwargs):
    counter = collections.Counter()
    counter.update(unique_fields_present_generator(*args, **kwargs))
    return dict(counter)


data_all = json.load(open('data/status.json'))
stats = []

schema_obj = Schema360()
schema_fields = schema_obj.get_release_pkg_schema_fields()


for dataset in data_all:
    json_filename = dataset['datagetter_metadata'].get('json')
    if json_filename:
        with open(json_filename) as fp:
            json_data = json.load(fp)
            fields_present = get_fields_present(json_data)
            unique_fields_present = get_unique_fields_present(json_data)
        dataset['datagetter_coverage'] = {}
        for field in fields_present:
            dataset['datagetter_coverage'][field] = {
                'total_fields': fields_present[field],
                'grants_with_field': unique_fields_present.get(field),
                'standard': field in schema_fields,
            }
    stats.append(dataset)
    with open('data/coverage.json', 'w') as fp:
        json.dump(stats, fp, indent='  ', sort_keys=True)
