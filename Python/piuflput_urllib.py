""" piuflput.py

   Copyright 2015 OSIsoft, LLC.
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
using the UFL REST endpoint

The syntax is: python piufl.py REST-URL file

Parameters:
    rest-ufl - The Address specified in the Data Source configuration
    file - Data file to be processed by the Connector

Example:
    python piuflput.py https://<server>:<port>/connectordata/value value.csv
"""

import argparse
import getpass
import urllib
import urllib.request

# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'POST file contents to PI Connector for UFL'
parser.add_argument('resturl', help='REST endpoint address')
parser.add_argument('file', help='Data file to be Put-ed')
args = parser.parse_args()

# In the Session information, set the username and password as specified in
# the connector configuration page
# You can hard code the username and password, if not, you will be prompted to enter them
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

# set up authentification
auth_handler = urllib.request.HTTPBasicAuthHandler()
auth_handler.add_password(realm='',
                       uri=args.resturl,
                       user=username(),
                       passwd=password())
opener = urllib.request.build_opener(auth_handler)
urllib.request.install_opener(opener)

# Read the file contents and send the content to the connector
with open(args.file, 'r') as f:
    data = bytes(''.join(f.readlines()), 'utf-8')
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    req = urllib.request.Request(url=args.resturl, data=data, method='PUT')
    with urllib.request.urlopen(req) as response:
        pass
    if response.status != 200:
        print('The following error has occured:')
        print(response.status, response.reason)
    else:
        print('The data was sent successfully')
        print('If parsing errors have occured, they will be listed in the event logs')
