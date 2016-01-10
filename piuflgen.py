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
    format - Specify the sample format to generate.
    Valid formats are: value or values.

Example:
    python piuflgen.py values
"""

import argparse
import datetime
import random


# Verify that the format is either value or values
class CheckArgumentAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values not in ('value', 'values'):
            parser.print_help()
            parser.exit(status=1)
        setattr(namespace, self.dest, values)

parser = argparse.ArgumentParser()
parser.description = 'Create sample data for use with PI Connector for UFL'
parser.add_argument('format',
                    help='specify sample format to generate. '
                         'Select one of: value, values',
                    action=CheckArgumentAction)
sample = parser.parse_args().format

# all devices and sensors for sample dataset
devices = ('00-00-00-b2-11-1a',
           '00-00-00-b2-11-1b',
           '00-00-00-b2-11-1c',
           '00-00-00-b2-11-1d',
           '00-00-00-b2-11-1e')

sensors = ('rpm', 'temperature', 'vibration')

timestamp = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)

# specify the newline character, by default the connector expects
# the CLRF style, that is the ascii character 13 followed by ascii chracter 10
newline = chr(13) + chr(10)
# output sample records - either one record per sensor or one record per device
timeFormat = '%Y-%m-%dT%H:%M:%SZ'
with open(sample + 'test.csv', 'w') as f:
    if sample == 'value':
        for device in devices:
            for sensor in sensors:
                f.write('{}:{},{},{}'.format(device,
                                             sensor,
                                             timestamp.strftime(timeFormat),
                                             random.randint(1000, 3450)))
                f.write(newline)
            timestamp += datetime.timedelta(seconds=1)
    elif sample == 'values':
        for device in devices:
            print('{},{},{},{},{}'.format(device,
                                          timestamp.strftime(timeFormat),
                                          random.randint(1000, 3450),
                                          random.randint(35, 120),
                                          random.randint(1000, 3450)))
