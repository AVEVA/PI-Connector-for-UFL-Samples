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
import sys

import requests
# this line is not required if a trusted certificated
# is used to replace the self signed certificate generated
# by the PI connector for UFl
requests.packages.urllib3.disable_warnings()

# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'POST file contents to PI Connector for UFL'
parser.add_argument('resturl', help='REST endpoint address')
parser.add_argument('file', help='Data file to be Put-ed')
args = parser.parse_args()

s = requests.session()
# In the Session information, one needs to set the username and password
# as specified in the connector configuration page
# You can hard code the credentials in the variables below.
# If not, you will be prompted to enter them at run time.
# If anonymous authentification is used, then use can use emptry strings for both
_username = None
_password = None

def username():
    global _username
    if _username is None:
        _username = getpass.getpass('Username: ')
    return _username
   

def password():
    global _password
    if _password is None:
        _password = getpass.getpass()
    return _password


s.auth = (username(), password())

# Read the file contents and send the content to the connector.
with open(args.file, 'r') as f:
    data = ''.join(f.readlines())
    # You should remove verify=False if the certificate used is a trusted one.
    response = s.put(args.resturl, data=data, verify=False)
    # To use the Post method instead, replace the line above with the one below.
    # response = s.post(args.resturl + '/post', data=data, verify=False)
    if response.status_code != 200:
        print('The following error has occured:', file=sys.stderr)
        print(response.status_code, response.reason, file=sys.stderr)
    else:
        print('The data was sent successfully to the PI Connector for UFL.')
        print('Check the "PI Connectors" event logs for any other errors processing the sent data.')
