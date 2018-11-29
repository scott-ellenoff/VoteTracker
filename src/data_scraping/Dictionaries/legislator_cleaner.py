import pandas as pd
import json

# Convert json to a list of legislators
# Current legislator dump from https://github.com/unitedstates/congress-legislators
cur_legislators = json.loads(open('Raw/legislators.json').read())

clean_legislators = []

for legislator in cur_legislators:
    legislator_dict = {}
    print(legislator)
    legislator_dict['LID'] = legislator['id']['bioguide']
    legislator_dict['State'] = legislator['terms'][-1]['state']

    if legislator['terms'][-1]['type'] == 'sen':
        legislator_dict['isSenator'] = 1
        legislator_dict['District'] = 0
    else:
        legislator_dict['isSenator'] = 0
        legislator_dict['District'] = legislator['terms'][-1]['district']

    if 'official_full' in legislator['name']:
        legislator_dict['FullName'] = legislator['name']['official_full']
    else:
        legislator_dict['FullName'] = legislator['name']['first'] + ' ' + legislator['name']['middle'] +\
                                      ' ' + legislator['name']['last']

    legislator_dict['Affiliation'] = legislator['terms'][-1]['party']

    legislator_dict['DWNominate'] = 0

    if 'url' in legislator['terms'][-1]:
        legislator_dict['URL'] = legislator['terms'][-1]['url']
    else:
        legislator_dict['URL'] = 'URL Not Present Yet'


    clean_legislators.append(legislator_dict)

with open('Clean/clean_legislators.json', 'w') as outfile:
    json.dump(clean_legislators, outfile, ensure_ascii=True)
