import csv
import json

with open('data/data.json') as fp:
    data_json = json.load(fp)

with open('data/report.csv', 'w') as fp:
    writer = csv.DictWriter(fp, ['publisher_name', 'title', 'datetime_downloaded', 'file_type', 'converts', 'valid', 'acceptable_license'])
    writer.writeheader()
    for dataset in data_json:
        writer.writerow({
            'publisher_name': dataset['publisher']['name'],
            'title': dataset['title'],
            'file_type': dataset['datagetter_metadata']['file_type'],
            'datetime_downloaded': dataset['datagetter_metadata']['datetime_downloaded'],
            'converts': bool(dataset['datagetter_metadata']['json']),
            'valid': dataset['datagetter_metadata'].get('valid', ''),
            'acceptable_license': dataset['datagetter_metadata']['acceptable_license'],
        })
