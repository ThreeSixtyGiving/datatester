import csv
import json
from collections import defaultdict

with open('data/stats.json') as fp:
    data_json = json.load(fp)

with open('data/report.csv', 'w') as fp:
    writer = csv.DictWriter(fp, [
        'publisher_prefix', 'publisher_name', 'title', 'accessURL',
        'downloadURL', 'datetime_downloaded', 'file_type', 'downloads',
        'converts', 'valid', 'acceptable_license', 'count', 'unique_ids_count',
        'distinct_funding_org_identifier_count',
        'distinct_recipient_org_identifier_count', 'min_award_date',
        'max_award_date', 'total_amount_GBP', 'min_amount_GBP',
        'max_amount_GBP', 'count_GBP', 'total_amount_not_GBP',
        'min_amount_not_GBP', 'max_amount_not_GBP', 'count_not_GBP',
        'currencies_not_GBP',
    ])
    writer.writeheader()
    for dataset in data_json:
        if 'datagetter_metadata' not in dataset:
            continue
        stats = dataset.get('datagetter_stats', {})

        currencies = stats.get('currencies', {})
        not_GBP = defaultdict(list)
        for currency, currency_dict in currencies.items():
            if currency == 'GBP':
                continue
            for field in 'min_amount', 'max_amount', 'total_amount', 'count':
                not_GBP[field] += [str(currency_dict.get(field, ''))]
            not_GBP['currencies'] += [currency]

        writer.writerow({
            'publisher_prefix': dataset['publisher']['prefix'],
            'publisher_name': dataset['publisher']['name'],
            'title': dataset['title'],
            'accessURL': dataset['distribution'][0]['accessURL'],
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
            'max_award_date': stats.get('max_award_date'),
            'total_amount_GBP': currencies.get('GBP', {}).get('total_amount'),
            'min_amount_GBP': currencies.get('GBP', {}).get('min_amount'),
            'max_amount_GBP': currencies.get('GBP', {}).get('max_amount'),
            'count_GBP': currencies.get('GBP', {}).get('count'),
            'total_amount_not_GBP': '; '.join(not_GBP['total_amount']),
            'min_amount_not_GBP': '; '.join(not_GBP['min_amount']),
            'max_amount_not_GBP': '; '.join(not_GBP['max_amount']),
            'count_not_GBP': '; '.join(not_GBP['count']),
            'currencies_not_GBP': '; '.join(not_GBP['currencies']),
        })
