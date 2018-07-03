import csv
import json

with open('data/stats.json') as fp:
    data_json = json.load(fp)

with open('data/report.csv', 'w') as fp:
    writer = csv.DictWriter(fp, [
        'publisher_name', 'title', 'downloadURL', 'datetime_downloaded',
        'file_type', 'downloads', 'converts', 'valid', 'acceptable_license',
        'count', 'unique_ids_count', 'distinct_funding_org_identifier_count',
        'distinct_recipient_org_identifier_count', 'min_award_date',
        'max_award_date',
    ])
    writer.writeheader()
    for dataset in data_json:
        if 'datagetter_metadata' not in dataset:
            continue
        stats = dataset.get('datagetter_stats', {})
        writer.writerow({
            'publisher_name': dataset['publisher']['name'],
            'title': dataset['title'],
            'downloadURL': dataset['distribution'][0]['downloadURL'],
            'file_type': dataset['datagetter_metadata'].get('file_type'),
            'datetime_downloaded': dataset['datagetter_metadata']['datetime_downloaded'],
            'downloads': dataset['datagetter_metadata']['downloads'],
            'converts': bool(dataset['datagetter_metadata']['json']) if 'json' in dataset['datagetter_metadata'] else '',
            'valid': dataset['datagetter_metadata'].get('valid', ''),
            'acceptable_license': dataset['datagetter_metadata'].get('acceptable_license'),
            'count': stats.get('count'),
            'unique_ids_count': stats.get('unique_ids_count'),
            'distinct_funding_org_identifier_count': stats.get('distinct_funding_org_identifier_count'),
            'distinct_recipient_org_identifier_count': stats.get('distinct_recipient_org_identifier_count'),
            'min_award_date': stats.get('min_award_date'),
            'max_award_date': stats.get('min_award_date'),
        })
