import requests
import json
import flattentool
import os
import sys
import tempfile
import shutil
import traceback
import strict_rfc3339
import datetime
import argparse
import rfc6266  # (content-disposition header parser)
from jsonschema import validate, ValidationError, FormatChecker

parser = argparse.ArgumentParser()
parser.add_argument('--no-download', dest='download', action='store_false')
parser.add_argument('--no-convert', dest='convert', action='store_false')
parser.add_argument('--no-convert-big-files', dest='convert_big_files', action='store_false')
parser.add_argument('--no-validate', dest='validate', action='store_false')
args = parser.parse_args()

acceptable_licenses = [
    'http://www.opendefinition.org/licenses/odc-pddl',
    'https://creativecommons.org/publicdomain/zero/1.0/',
    'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/2/',
    'http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/',
    'https://creativecommons.org/licenses/by/4.0/',
    'https://creativecommons.org/licenses/by-sa/3.0/',
    'https://creativecommons.org/licenses/by-sa/4.0/',
]

unacceptable_licenses = [
    '',
    # Not relicenseable as CC-BY
    'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/1/', 
    'https://creativecommons.org/licenses/by-nc/4.0/',
    'https://creativecommons.org/licenses/by-nc-sa/4.0/',
]

CONTENT_TYPE_MAP = {
    'application/json': 'json',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'xlsx',
    'text/csv': 'csv'
}

schema = json.loads(requests.get('https://raw.githubusercontent.com/ThreeSixtyGiving/standard/master/schema/360-giving-package-schema.json').text)


def convert_spreadsheet(input_path, converted_path, file_type):
    encoding = 'utf-8-sig'
    if file_type == 'csv':
        tmp_dir = tempfile.mkdtemp()
        destination = os.path.join(tmp_dir, 'grants.csv')
        shutil.copy(input_path, destination)
        try:
            with open(destination, encoding='utf-8-sig') as main_sheet_file:
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
        encoding=encoding,
        metatab_schema='https://raw.githubusercontent.com/ThreeSixtyGiving/standard/master/schema/360-giving-package-schema.json',
        metatab_name='Meta',
        metatab_vertical_orientation=True,
    )

if args.download:
    r = requests.get('http://data.threesixtygiving.org/data.json')
    with open('data/data_original.json', 'w') as fp:
        fp.write(r.text)
    data_all = r.json()
else:
    data_all = json.load(open('data/data_all.json')) 

data_valid = []
data_acceptable_license = []
data_acceptable_license_valid = []

for dataset in data_all:
    ## Skip big lottery for testing
    #if dataset['identifier'] == 'a002400000Z58cqAAB':
    #    continue

    metadata = dataset.get('datagetter_metadata', {})
    dataset['datagetter_metadata'] = metadata

    if not dataset['license'] in acceptable_licenses + unacceptable_licenses:
        raise ValueError('Unrecognised license '+dataset['license'])

    url = dataset['distribution'][0]['downloadURL']

    if args.download:
        metadata['datetime_downloaded'] = strict_rfc3339.now_to_rfc3339_localoffset()
        try:
            r = requests.get(url, headers={'User-Agent': 'datagetter (https://github.com/ThreeSixtyGiving/datagetter)'})
            r.raise_for_status()
        except KeyboardInterrupt:
            raise
        except:
            print("\n\nDownload failed for dataset {}\n".format(dataset['identifier']))
            traceback.print_exc()
            metadata['downloads'] = False
        else:
            metadata['downloads'] = True
        content_type = r.headers.get('content-type', '').split(';')[0].lower()
        if content_type and content_type in CONTENT_TYPE_MAP:
            file_type = CONTENT_TYPE_MAP[content_type]
        elif 'content-disposition' in r.headers:
            file_type = rfc6266.parse_requests_response(r).filename_unsafe.split('.')[-1]
        else:
            file_type = url.split('.')[-1]
        if file_type not in CONTENT_TYPE_MAP.values():
            print("\n\nUnrecognised file type {}\n".format(file_type))
            continue
        metadata['file_type'] = file_type
        file_name = 'data/original/'+dataset['identifier']+'.'+file_type
        with open(file_name, 'wb') as fp:
            fp.write(r.content)
    else:
        file_type = metadata['file_type']
        file_name = 'data/original/'+dataset['identifier']+'.'+file_type

    json_file_name = 'data/json_all/{}.json'.format(dataset['identifier'])

    metadata['file_size'] = os.path.getsize(file_name)

    if args.convert and (
            args.convert_big_files or
            metadata['file_size'] < 10 * 1024 * 1024
            ):
        if file_type == 'json': 
            os.link(file_name, json_file_name)
            metadata['json'] = json_file_name
        else:
            try:
                convert_spreadsheet(
                    file_name,
                    json_file_name,
                    file_type)
            except KeyboardInterrupt:
                raise
            except:
                print("\n\nUnflattening failed for file {}\n".format(file_name))
                traceback.print_exc()
                metadata['json'] = None
            else:
                metadata['json'] = json_file_name

    metadata['acceptable_license'] = dataset['license'] in acceptable_licenses

    # We can only do anything with the JSON if it did successfully convert.
    if metadata.get('json'):
        format_checker = FormatChecker()
        if args.validate:
            try:
                with open(json_file_name, 'r') as fp:
                    validate(json.load(fp), schema, format_checker=format_checker)
            except (ValidationError, ValueError):
                metadata['valid'] = False
            else:
                metadata['valid'] = True
        
        if metadata['valid']:
            os.link(json_file_name, 'data/json_valid/{}.json'.format(dataset['identifier']))
            data_valid.append(dataset)
            if metadata['acceptable_license']:
                os.link(json_file_name, 'data/json_acceptable_license_valid/{}.json'.format(dataset['identifier']))
                data_acceptable_license_valid.append(dataset)

        if metadata['acceptable_license']:
            os.link(json_file_name, 'data/json_acceptable_license/{}.json'.format(dataset['identifier']))
            data_acceptable_license.append(dataset)


    # Output data.json after every dataset, to help with debugging if we fail
    # part way through
    with open('data/data_all.json', 'w') as fp:
        json.dump(data_all, fp, indent=4)
    with open('data/data_valid.json', 'w') as fp:
        json.dump(data_valid, fp, indent=4)
    with open('data/data_acceptable_license.json', 'w') as fp:
        json.dump(data_acceptable_license, fp, indent=4)
    with open('data/data_acceptable_license_valid.json', 'w') as fp:
        json.dump(data_acceptable_license_valid, fp, indent=4)
