""" putJSONdata.py

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


Call: 
    python putJSONdata.py rest-ufl rest-external

Parameters:
    rest-ufl - The Address specified in the Data Source configuration
    rest-external - A third party data source which returns JSON data when receving a get request from this URL.

Example:
    python putJSONdata.py https://localhost:5460/connectordata/currency http://api.fixer.io/latest?base=USD
"""

import argparse
import getpass
import json
import sys
from functools import lru_cache

import requests

# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'POST file contents to PI Connector for UFL'
parser.add_argument('restufl', help='The UFL rest endpoint address')
parser.add_argument('restexternal', help='The external data source rest end point')
args = parser.parse_args()

@lru_cache(maxsize=1)
def password():
    return getpass.getpass()


@lru_cache(maxsize=1)
def username():
    return getpass.getpass('Username: ')


s = requests.session()
# To hardcode the username and password, specify them below
# To use anonymous login, use: ("", "")
s.auth = (username(), password())

def getData(url):
    # Being very careful when checking for failure when accessing the external site
    try:
        response = requests.get(url=url)
        if response.status_code != requests.codes.ok:
            print("The url {0} did not return the expected value back.".format(response.url))
            print("Response: {0} {1}".format(response.status_code, response.reason))
            sys.exit(0)
        try:
            return json.dumps(response.json(), indent=4, sort_keys=True)
        except ValueError as e:
            print(e)
            sys.exit(0)
    except requests.exceptions.Timeout:
        # Maybe set up for a retry, or continue in a retry loop
        print("Connection timed out")
        sys.exit(0)
    except requests.exceptions.TooManyRedirects:
        # Tell the user their URL was bad and try a different one
        print("Too many redirects")
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        print("There was an issue with requesting the data:")
        print(e)
        sys.exit(0)


data = getData(args.restexternal)

# remove verify=False if the certificate used is a trusted one
response = s.put(args.restufl, data=data, verify=False)
# If instead of using the put request, you need to use the post request
# use the function as listed below
# response = s.post(args.resturl + '/post', data=data, verify=False)
if response.status_code != 200:
    print("Sending data to the UFL connect failed due to error {0} {1}".format(response.status_code, response.reason))
else:
    print('The data was sent successfully over https.')
    print('Check the PI Connectors event logs for any further information.')
