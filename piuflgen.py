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

The syntax is: python piuflgen.py format

Parameters:
    format - Specify the sample format to generate. Valid formats are: value or values.
	
Example:
    python piuflgen.py values

	"""
import argparse
import datetime
import random

### Check for a valid argument

def checker(x):
    return {
        'value': "value",
        'values': "values"
    }.get(x, 0)

parser = argparse.ArgumentParser(description='Create sample data for use with PI Connector for UFL')
parser.add_argument("format",
                        help='specify sample format to generate. select one of: value, values')
args = parser.parse_args()

### check for valid format argument

if not(args.format):
	parser.print_help()
	parser.exit(status=1)
	
sample = checker(args.format)
if sample == 0:
	parser.print_help()
	parser.exit(status=1)
	
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


### print out sample records - one record per sensor value
							
if sample == "value":
	for device in devices:
		for sensor in sensors:
			print("{}:{},{},{}".format(device,
							sensor,
							timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
							random.randint(1000, 3450)))
		timestamp = timestamp + datetime.timedelta(seconds=1)
		
### print out sample records - one record per asset
	
if sample == "values":
	for device in devices:
		print("{},{},{},{},{}".format(device,
							timestamp.strftime("%Y-%m-%dT%H:%M:%SZ"),
							random.randint(1000, 3450),
							random.randint(35, 120),
							random.randint(1000, 3450)))


