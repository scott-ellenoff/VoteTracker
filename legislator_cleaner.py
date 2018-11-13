import pandas as pd
import json

# Convert json to a list of legislators
# Current legislator dump from https://github.com/unitedstates/congress-legislators
cur_legislators = json.loads(open('full_legislators.json').read())

clean_legislators = []

for legislator in cur_legislators:
    legislator_dict = {}
    legislator_dict['LID'] = legislator['id']['bioguide']
    legislator_dict['Name'] = legislator['name']['official_full']

    if legislator['terms'][-1]['type'] == 'sen':
        legislator_dict['Senator?'] = 1
    else:
        legislator_dict['Senator?'] = 0

    legislator_dict['Affiliation'] = legislator['terms'][-1]['party']
    legislator_dict['URL'] = legislator['terms'][-1]['url']
    legislator_dict['DWNominate'] = 0

    clean_legislators.append(legislator_dict)

with open('clean_legislators.json', 'w') as outfile:
    json.dump(clean_legislators, outfile, ensure_ascii=True)

# new_legislators = json.loads(open('clean_legislators.json').read())
#
# for legislator in new_legislators:
#     if legislator['LID'] == 'C001072':
#         print(legislator)