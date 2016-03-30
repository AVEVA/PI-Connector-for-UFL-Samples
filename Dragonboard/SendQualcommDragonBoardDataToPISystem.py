#!/usr/bin/env python

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

This python example sends various statistics on the state of a Qualcomm Dragonboard to the PI Connector
using the UFL REST endpoint.
This script requeries the Python requests module:
http://docs.python-requests.org/en/master/
Which can be installed using the following command:
    pip install requests
or, depending on your environement:
    apt-get install python-requests

The syntax is: python SendQualcommDragonBoardDataToPISystem.py REST-URL DeviceName Sampling

Parameters:
    rest-ufl - The Address specified in the Data Source configuration
    DeviceName - The name of the data device
    sampling - The frequency that you want data to be collected

Example:
    python SendQualcommDragonBoardDataToPISystem.py https://<server>:<port>/connectordata/dragonboard "Qualcomm DragonBoard 1701" 10
"""

from datetime import datetime
import time
import json
import sys
import argparse
import getpass

import requests
import linux_metrics as lm

# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'Collect data from your Dragonboard and send it to PI Connector for UFL Rest End point'
parser.add_argument('restufl', help='REST endpoint address')
parser.add_argument('device', help='The name of the device encoded in quotes')
parser.add_argument('sampling', help='The sampling rate in seconds')
args = parser.parse_args()


# --------------------------------------------

# Define the sampling interval
SAMPLE_INTERVAL_SECONDS = int(args.sampling)

# Define the name of this device
DEVICE_NAME = args.device

# --------------------------------------------

# Define the target URL where data should be posted 
TARGET_URL = args.restufl

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

# --------------------------------------------

# Begin!
print("Program beginning...")
print("Data will be collected every " + str(SAMPLE_INTERVAL_SECONDS) + " seconds...")
print("\nData will be sent to " + TARGET_URL)
print("\nThis device is called: " + DEVICE_NAME + "...")

# --------------------------------------------

print("\nNow beginning infinite loop...")
print ("\n")
while (True):
    try:
        # --------------------------------------------
        
        # Get sensor data
        cpuPercentagesArray = lm.cpu_stat.cpu_percents(sample_duration=1)
        cpuUsage = (100 - cpuPercentagesArray['idle'])
        diskBusyTime = lm.disk_stat.disk_busy('mmcblk0', sample_duration=1)
        memoryUsed, totalMemory, _, _, _, _ = lm.mem_stat.mem_stats()
        WiFiRxBits, WiFiTxBits = lm.net_stat.rx_tx_bits('wlan0')  

        # Get position
        geolocationServiceURL = 'http://ip-json.rhcloud.com/json'
        geolocationRequest = requests.get(geolocationServiceURL)
        geolocationJSONData = json.loads(geolocationRequest.text)
        latitudeDegrees = geolocationJSONData['latitude']
        longitudeDegrees = geolocationJSONData['longitude']

        # Get the current time
        currentTime = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # --------------------------------------------
        
        # Compose the message in a JSON form suitable for POSTing
        # The data will be of the form
        # {"d":"cRIO9068","t":"2016-03-08T07:03:29Z","v1":0.5,"v2":0,"v3":0,"v4":0}
        # Where the first item, d, is the device identifier, the second item is the timestamp, 
        # in format yyyy-MM-ddThh:mm:ss.nnn, and the next four items, v1 through v4, are sensor names and sensor readings

        d = {'d': DEVICE_NAME, 't': currentTime, 'Latitude': str(latitudeDegrees), 'Longitude': str(longitudeDegrees), 'CPU Usage': str(cpuUsage), 'Disk Busy Time':str(diskBusyTime),
        'RAM In Use':str(memoryUsed), 'RAM Total': str(totalMemory), 'Wi-Fi Card Bits Received': str(WiFiRxBits), 'Wi-Fi Card Bits Sent':  str(WiFiTxBits)}
        
        data = 'H ' + ','.join(sorted(d.keys())) + '\r'
        data += ','.join(d[key] for key in sorted(d.keys()))
        print(data)
        
        # Print the message, for debugging purposes, if desired
        #print(JSONMessageStringForPOSTing)
        
        # You should remove verify=False if the certificate used is a trusted one.
        response = s.put(args.resturl, data=JSONMessageStringForPOSTing, verify=False)
        # To use the Post method instead, replace the line above with the one below.
        # response = s.post(args.resturl + '/post', data=data, verify=False)
        
        # Print a debug message, just to signify the loop is done
        print(currentTime + " Send status: " + str(request.status_code))
        
    except:
        # Catch any errors that occur
        e = sys.exc_info()[0]
        print(currentTime + " Error ocurred: " + str(e))

    # --------------------------------------------

    finally: 
    
        # Sleep until the next sample
        time.sleep(SAMPLE_INTERVAL_SECONDS)
