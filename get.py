import requests
import json
import flattentool
import os
import tempfile
import shutil
import traceback

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
    try:
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
    except Exception:
        print("Unflattening failed for file {}".format(input_path))
        traceback.print_exc()
        #raise

#r = requests.get('http://data.threesixtygiving.org/data.json')
#with open('data/data.json', 'w') as fp:
#    fp.write(r.text)
#data_json = r.json()
data_json = json.load(open('data/data.json')) 

for dataset in data_json:
    if not dataset['license'] in acceptable_licenses + unacceptable_licenses:
        raise ValueError('Unrecognised license '+dataset['license'])

    url = dataset['distribution'][0]['downloadURL']
    file_type = url.split('.')[-1]
    r = requests.get(url)
    if len(file_type) > 5 and 'content-disposition' in r.headers:
        file_type = r.headers.get('content-disposition').split('.')[-1]
    file_name = 'data/source/'+dataset['identifier']+'.'+file_type
    with open(file_name, 'wb') as fp:
        fp.write(r.content)

    print(file_type)
    convert_spreadsheet(
        file_name,
        'data/converted/{}.json'.format(dataset['identifier']),
        file_type)
