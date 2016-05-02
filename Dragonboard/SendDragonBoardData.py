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

# Install these additional libraries using pip install
import requests
import linux_metrics

# Suppress insecure HTTPS warnings, if an untrusted certificate is used by the target endpoint
# Remove if targetting trusted targets
requests.packages.urllib3.disable_warnings()


# Process arguments that were passed in, such as the end point, sample rate, etc.
parser = argparse.ArgumentParser()
parser.description = 'Collect data from your Dragonboard and send it to PI Connector for UFL Rest End point'
parser.add_argument('restufl', help='REST endpoint address')
parser.add_argument('device', help='The name of the device encoded in quotes')
parser.add_argument('sampling', help='The sampling rate in seconds')
args = parser.parse_args()

# Create an HTTP request session object, which will hold the basic authentication credentials
# that are needed to send data to this particular endpoint; those credentials should match the ones
# that were entered in when the UFL Connector Data Source was created
currentHTTPRequestSession = requests.session()
# In the session information, set the username and password as specified in
# the connector configuration page
# You can hard-code the credentials into this file by entering them in below;
# if you do not, you will be prompted to enter them when you call this script
# If anonymous authentification is used, then use an emptry string for both
_username = None
_password = None

# Define two functions to return the username and password, if hard-coded, or to
# prompt the user for the credentials if they aren't hard-coded into this file
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

# Apply the username and password, however they were obtained, to the HTTP request session object
currentHTTPRequestSession.auth = (username(), password())

# Begin!
print("Program beginning...")
print("Data will be collected every " + args.sampling + " seconds")
print("Data will be sent to: " + args.restufl)
print("This device is called: " + args.device)
print()
print("Now sending data, hit control-c to stop collecting and sending data")
print()

# This function queries sensors for values and then assembles the values into an object
def getData():

    # Initialize the sensor data variables
    latitude,longitude,cpuUsage,diskBusyTime,memoryUsed,totalMemory,WiFiBitsReceived,WiFiBitsTransmitted = 0,0,0,0,0,0,0,0

    # Get position using a third-party geolocation service
    # Use a try-except statement in case any sensor readings fail
    try:
        geolocationServiceURL = 'http://ip-json.rhcloud.com/json'
        geolocationRequest = requests.get(geolocationServiceURL, timeout=5)
        geolocationJSONData = json.loads(geolocationRequest.text)
        latitude = geolocationJSONData['latitude']
        longitude = geolocationJSONData['longitude']
    except Exception as e:
        # Log any error, if it occurs
        print(str(datetime.now()) + " An error has ocurred getting position: " + str(e))		

    # Get performance information for this device
    try:
        cpuPercentagesArray = linux_metrics.cpu_stat.cpu_percents(sample_duration=1)
        cpuUsage = (100 - cpuPercentagesArray['idle'])
        diskBusyTime = linux_metrics.disk_stat.disk_busy('mmcblk0', sample_duration=1)
        memoryUsed, totalMemory = linux_metrics.mem_stat.mem_stats()[0:2]
        WiFiBitsReceived, WiFiBitsTransmitted = linux_metrics.net_stat.rx_tx_bits('wlan0')  
    except Exception as e:
        # Log any error, if it occurs
        print(str(datetime.now()) + " An error has ocurred getting performance data: " + str(e))

    
    # Assemble an object that contains the variable names and values
    sensorDataObject = {'!device': args.device, 
        '!time': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"), 
        'Latitude': str(latitude), 
        'Longitude': str(longitude), 
        'CPU Usage': str(cpuUsage),
        'Disk Busy Time':str(diskBusyTime),
        'RAM In Use':str(memoryUsed), 
        'RAM Total': str(totalMemory), 
        'Wi-Fi Card Bits Received': str(WiFiBitsReceived), 
        'Wi-Fi Card Bits Sent':  str(WiFiBitsTransmitted)}

    # Return the sensor data object
    return sensorDataObject

while True:
    try:
        # Call the getData function to obtain the sensor data object
        sensorDataObject = getData()
        # Convert the sensor data object into JSON, so that it can be sent via an HTTP request
        sensorDataJSON = json.dumps(sensorDataObject, indent=4, sort_keys=True)
        # Send the HTTP request! You should remove verify=False if the certificate used is a trusted one.
        response = currentHTTPRequestSession.put(args.restufl, data=sensorDataJSON, verify=False)
        print(str(datetime.now()) + " Send status: " + str(response.status_code) + ' ' + str(response.reason))
    except KeyboardInterrupt:
        # When a user cancels via the keyboard, exit with status 1
        print("Finished sampling data.")
        sys.exit(1)
    except Exception as e:
        # Log any error, if it occurs
        print(str(datetime.now()) + " An error has ocurred: " + str(e))
        sys.exit(1)
    finally:    
        # Sleep until the next sample
        time.sleep(int(args.sampling))
