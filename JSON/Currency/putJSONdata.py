""" piuflput.py

   Copyright 2016 OSIsoft, LLC.
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

This python example sends a file's contents to the PI Connector
using the UFL REST endpoint.
This script requeries the Python requests module:
http://docs.python-requests.org/en/master/
Which can be installed using the following command:
    pip install requests
or, depending on your environement:
    apt-get install python-requests

The syntax is: python piufl.py REST-URL file

Parameters:
    rest-ufl - The Address specified in the Data Source configuration
    file - Data file to be processed by the Connector

Example:
    python piuflput.py https://<server>:<port>/connectordata/value value.csv
"""

import argparse
import getpass
import json

import requests

# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
# Remove if targetting trusted targets
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'POST file contents to PI Connector for UFL'
parser.add_argument('resturl', help='REST endpoint address')
parser.add_argument('externalendpoit', help='Data to be fetched and then to be Put-ed')
args = parser.parse_args()


def requestJSONdata(url):
    response = requests.get(url=url)
    return json.dumps(response.json(), indent=4, sort_keys=True)
    
s = requests.session()
# In the Session information, set the username and password as specified in
# the connector configuration page
# You can hard code the credentials, if not, you will be prompted to enter them
# If anonymous authentification is used, then use an emptry string for both
_username = None
_password = None

def password():
    global _password
    if _password is None:
        # Store the password so that this method is only called once
        _password = getpass.getpass('please type in your password: ')
    return _password


def username():
    global _username
    if _username is None:
        # Store the username so that this method is only called once
        _username = getpass.getpass('please type in your username: ')
    return _username

s.auth = (username(), password())

# Read the file contents and send the content to the connector
data = requestJSONdata(args.externalendpoit)

print(data)
print(args.resturl)
# remove verify=False if the certificate was replaced
response = s.put(args.resturl, data=data, verify=False)
# If instead of using the put request, you need to use the post request
# use the function as listed below
# response = s.post(args.resturl + '/post', data=data, verify=False)
if response.status_code != 200:
    print('The following error has occured:')
    print(response.status_code, response.reason)
else:
    print('The data was sent successfully')
    print('Check the event logs for any parsing errors')

