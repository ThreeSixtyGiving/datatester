import ijson
import json
import os
import traceback


# We assmue that there are no one-to-many relationships besides location
def one_to_one_assumption(l):
    for x in l:
        if type(x) == list:
            assert len(x) <= 1
            if x:
                one_to_one_assumption(x[0])
        if type(x) == dict:
            one_to_one_assumption(x.values())

# We assume that all of a funder's grants are from the same publisher.
publisher_by_funder = {}
def funders_grants_same_publisher(grant, publisher):
    funder = grant['fundingOrganization'][0]['id']
    if funder in publisher_by_funder:
        try:
            assert publisher['prefix'] == publisher_by_funder[funder]
        except:
            print(publisher['prefix'], publisher_by_funder[funder])
            raise
    else:
        publisher_by_funder[funder] = publisher['prefix']
        

def check_grant_assumptions(grant, dataset):
    one_to_one_assumption(grant.values())
    funders_grants_same_publisher(grant, dataset['publisher'])


publisher_access_urls = {}
with open('data/data_valid.json') as fp:
    data_json = json.load(fp)
for dataset in data_json:
    # We assume that all publishers have a non-empty prefix 
    prefix = dataset['publisher']['prefix']
    assert prefix
    # We assume that each dataset has one distribution
    assert len(dataset['distribution'])
    distribution =  dataset['distribution'][0]
    # We assume that all datasets from one publisher have the same:
    #   - accessURL
    if prefix in publisher_access_urls:
        assert distribution['accessURL'] == publisher_access_urls[prefix]
    else:
        publisher_access_urls[prefix] = distribution['accessURL']

    print('Checking {} {}'.format(dataset['title'], dataset['identifier']))
    try:
        with open(os.path.join('data/json_all/{}.json'.format(dataset['identifier']))) as fp:
            stream = ijson.items(fp, 'grants.item')
            for grant in stream:
                try:
                    grant['beneficiaryLocation'] = None
                    check_grant_assumptions(grant, dataset)
                except:
                    print(grant)
                    raise
    except:
        traceback.print_exc()
        continue


# TODO: check that grant ids start with prefixes
