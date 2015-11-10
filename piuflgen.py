""" piuflgen.py

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

Generate sample data to publish to the PI Connector for UFL REST endpoint

The syntax is: python piuflgen.py file

Parameters:
    file - Output file for sample data
	
Example:
    python piuflgen.py

	"""
import argparse
import datetime
import random

### Check for a valid argument

def checker(x):
    return {
        '1': 1,
        '2': 2,
    }.get(x, 1)

parser = argparse.ArgumentParser(description='Create sample data for use with PI Connector for UFL')
parser.add_argument("-s","--selectsample",
                        help='specify sample to generate')
args = parser.parse_args()

### define devices and sensors for sample dataset

devices = ["00-00-00-b2-11-1a",
		   "00-00-00-b2-11-1b",
		   "00-00-00-b2-11-1c",
		   "00-00-00-b2-11-1d"]

sensors = ["rpm", "temperature", "vibration"]

### Get the time a minute ago

timestamp = datetime.datetime.utcnow()
timestamp = timestamp - datetime.timedelta(minutes=1)

### Process optional arguments

if not (args.selectsample):
	sample = 1

sample = checker(args.selectsample)


### print out sample records - one record per asset
	
if sample == 1:
	for device in devices:
		print("{},{},{},{},{}".format(device,
							timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
							random.randint(1000, 3450),
							random.randint(35, 120),
							random.randint(1000, 3450)))

### print out sample records - one record per sensor value
							
if sample == 2:
	for device in devices:
		for sensor in sensors:
			print("{}:{},{},{}".format(device,
							sensor,
							timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
							random.randint(1000, 3450)))
		timestamp = timestamp + datetime.timedelta(seconds=1)
