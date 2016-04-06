#!/usr/bin/env python

""" SendDragonBoardData.py

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

The syntax is: 
    python SendDragonBoardData.py REST-UFL DeviceName Sampling

Parameters:
    rest-ufl - The Address specified in the Data Source configuration
    DeviceName - The name of the data device
    sampling - The frequency that you want data to be collected

Example:
    python SendDragonBoardData.py https://<server>:<port>/connectordata/dragonboard "Qualcomm DragonBoard 1701" 10
"""


import time
import json
import argparse
import sys
import getpass
from datetime import datetime
from functools import lru_cache

import requests
import linux_metrics as lm

# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
# Remove if targetting trusted targets
requests.packages.urllib3.disable_warnings()


# Process arguments
parser = argparse.ArgumentParser()
parser.description = 'Collect data from your Dragonboard and send it to PI Connector for UFL Rest End point'
parser.add_argument('restufl', help='REST endpoint address')
parser.add_argument('device', help='The name of the device encoded in quotes')
parser.add_argument('sampling', help='The sampling rate in seconds')
args = parser.parse_args()


s = requests.session()
# In the Session information, set the username and password as specified in
# the connector configuration page
# You can hard code the credentials, if not, you will be prompted to enter them
# If anonymous authentification is used, then use an emptry string for both
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

# Begin!
print("Program beginning...")
print("Data will be collected every " + args.sampling + " seconds")
print("Data will be sent to: " + args.restufl)
print("This device is called: " + args.device)
print()
print("Now sending data, hit control-c to stop collecting and sending data")
print()

def getData():
    cpuPercentagesArray = lm.cpu_stat.cpu_percents(sample_duration=1)
    cpuUsage = (100 - cpuPercentagesArray['idle'])
    diskBusyTime = lm.disk_stat.disk_busy('mmcblk0', sample_duration=1)
    memoryUsed, totalMemory = lm.mem_stat.mem_stats()[0:2]
    WiFiRxBits, WiFiTxBits = lm.net_stat.rx_tx_bits('wlan0')  

    # Get position
    geolocationServiceURL = 'http://ip-json.rhcloud.com/json'
    geolocationRequest = requests.get(geolocationServiceURL)
    geolocationJSONData = json.loads(geolocationRequest.text)
    
    sensors = {'!device': args.device, 
               '!time': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
               'Latitude': str(geolocationJSONData['latitude']), 
               'Longitude': str(geolocationJSONData['longitude']), 
               'CPU Usage': str(100 - cpuPercentagesArray['idle']),
               'Disk Busy Time':str(lm.disk_stat.disk_busy('mmcblk0', sample_duration=1)),
               'RAM In Use':str(memoryUsed), 
               'RAM Total': str(totalMemory), 
               'Wi-Fi Card Bits Received': str(WiFiRxBits), 
               'Wi-Fi Card Bits Sent':  str(WiFiTxBits)}
    
    return sensors
    
while True:
    try:
        sensorData = getData()
        data = json.dumps(sensorData, indent=4, sort_keys=True)
        # You should remove verify=False if the certificate used is a trusted one.
        response = s.put(args.restufl, data=data, verify=False)
        print(str(datetime.now()) + " Send status: " + str(response.status_code) + ' ' + str(response.reason))
    except KeyboardInterrupt:
        print("Finished sampling data.")
        sys.exit(1)
    except Exception as e:
        print("An error has ocurred: " + str(e))
        sys.exit(1)
    finally:    
        # Sleep until the next sample
        time.sleep(int(args.sampling))
