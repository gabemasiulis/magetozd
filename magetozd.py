import csv # we're taking a CSV input
import json # we're outputting JSON...
import requests # ... to an API endpoint

session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = '{EMAIL}', '{PASSWORD}'
url = 'https://{DOMAIN}.zendesk.com/api/v2/users/create_many.json'


# change the importFile for your path. TODO: make this interactive.
importFile = open('C:/path/to/customers.csv')

dataParser = csv.reader(importFile)
users_dict = {'users': []} # creates a users dictionary
payloads = [] # creates a dictionary of users dictionaries, max length will be 100

for row in dataParser:
    if dataParser.line_num != 1: # skip the header
        if list(row)[4]:
            users_dict['users'].append(
                {
                    'name': list(row)[1],
                    'email': list(row)[2],
                    'phone': list(row)[4]
                }
            )
            if len(users_dict['users']) == 100: # if we hit the max length
                payloads.append(json.dumps(users_dict))
                users_dict = {'users': []}

if users_dict['users']: # append any remaining users below max length
    payloads.append(json.dumps(users_dict))
    
for payload in payloads:
    response = session.post(url, data=payload)
    if response.status_code != 200:
        print('Import failed with status {}'.format(response.status_code))
        break
    print('Successfully imported a batch of users')
