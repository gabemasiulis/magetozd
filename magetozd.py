# Python 2.7
import csv # we're taking a CSV input
import json # we're outputting JSON...
import requests # ... to an API endpoint
import re # we'll format phone numbers with some regex

session = requests.Session()
session.headers = {'Content-Type': 'application/json'}
session.auth = '{EMAIL}', '{PASSWORD}'
url = 'https://{DOMAIN}.zendesk.com/api/v2/users/create_many.json'

importFile = open('{PATH TO FILE}')

dataParser = csv.reader(importFile)
users_dict = {'users': []}
payloads = [] # creates a dictionary of users dictionaries, max length will be 100

for row in dataParser:
    if dataParser.line_num != 1: # skip the header
        if list(row)[4]: # we're only importing users with phone numbers
            phoneNumber = '+1' + re.sub(r"\D", "", list(row)[4]) # format the number
            users_dict['users'].append(
                {
                    'name': list(row)[1],
                    "identities": [
                        {
                            "type": "email",
                            "value": list(row)[2],
                            "verified": True
                        },
                        {
                            "type": "phone_number",
                            "value": phoneNumber,
                            "verified": True
                        }
                    ]
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
