import requests
import json
import flattentool
import os
import tempfile
import shutil
import traceback
from jsonschema import validate, ValidationError

acceptable_licenses = [
    'http://www.opendefinition.org/licenses/odc-pddl',
    'https://creativecommons.org/publicdomain/zero/1.0/',
    'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/',
    'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
    'https://creativecommons.org/licenses/by/4.0/',
    'https://creativecommons.org/licenses/by-sa/4.0/',
]

unacceptable_licenses = [
    '',
    'https://creativecommons.org/licenses/by-nc/4.0/',
]

schema = json.loads(requests.get('https://raw.githubusercontent.com/ThreeSixtyGiving/standard/master/schema/360-giving-package-schema.json').text)

def convert_spreadsheet(input_path, converted_path, file_type):
    encoding = 'utf-8'
    if file_type == 'csv':
        tmp_dir = tempfile.mkdtemp()
        destination = os.path.join(tmp_dir, 'grants.csv')
        shutil.copy(input_path, destination)
        try:
            with open(destination, encoding='utf-8') as main_sheet_file:
                main_sheet_file.read()
        except UnicodeDecodeError:
            try:
                with open(destination, encoding='cp1252') as main_sheet_file:
                    main_sheet_file.read()
                encoding = 'cp1252'
            except UnicodeDecodeError:
                encoding = 'latin_1'
        input_name = tmp_dir
    else:
        input_name = input_path
    flattentool.unflatten(
        input_name,
        output_name=converted_path,
        input_format=file_type,
        root_list_path='grants',
        root_id='',
        schema='https://raw.githubusercontent.com/ThreeSixtyGiving/standard/master/schema/360-giving-schema.json',
        convert_titles=True,
        encoding=encoding
    )

r = requests.get('http://data.threesixtygiving.org/data.json')
with open('data/data_original.json', 'w') as fp:
    fp.write(r.text)
data_json = r.json()
#data_json = json.load(open('data/data_original.json')) 

for dataset in data_json:
    metadata = {}

    if not dataset['license'] in acceptable_licenses + unacceptable_licenses:
        raise ValueError('Unrecognised license '+dataset['license'])

    url = dataset['distribution'][0]['downloadURL']
    file_type = url.split('.')[-1]
    r = requests.get(url)
    if len(file_type) > 5 and 'content-disposition' in r.headers:
        file_type = r.headers.get('content-disposition').split('.')[-1]
    file_name = 'data/original/'+dataset['identifier']+'.'+file_type
    with open(file_name, 'wb') as fp:
        fp.write(r.content)

    print(file_type)
    json_file_name = 'data/json/{}.json'.format(dataset['identifier'])
    if file_type == 'json': 
        os.link(file_name, json_file_name)
        metadata['json'] = json_file_name
    else:
        try:
            convert_spreadsheet(
                file_name,
                json_file_name,
                file_type)
        except:
            print("Unflattening failed for file {}".format(file_name))
            traceback.print_exc()
            metadata['json'] = None
        else:
            metadata['json'] = json_file_name


    
    metadata['acceptable_license'] = dataset['license'] in acceptable_licenses
    if metadata['json'] and metadata['acceptable_license']:
        os.link(json_file_name, 'data/json_acceptable_license/{}.json'.format(dataset['identifier']))

    if metadata['json']:
        try:
                with open(json_file_name, 'r') as fp:
                    validate(json.load(fp), schema)
        except ValidationError:
            metadata['valid'] = False
        else:
            metadata['valid'] = True
            os.link(json_file_name, 'data/json_valid/{}.json'.format(dataset['identifier']))
            if metadata['acceptable_license']:
                os.link(json_file_name, 'data/json_acceptable_license_valid/{}.json'.format(dataset['identifier']))

    dataset['datagetter_metadata'] = metadata

with open('data/data.json', 'w') as fp:
    json.dump(data_json, fp, indent=4)
