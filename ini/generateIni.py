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

Generate sample ini files to use as data sources for the PI Connector for UFL

The syntax is: python generateini.py tag1 tag2 [...]

Parameters:
    tag1 tag2 [...] a list of tag used

Example:
    python piuflgen.py values

Data Source is in the following format:
TimeStamp,tag1,tag2
2016-01-01 00:00:00.000,2.467,61.976
2016-01-01 00:00:01.000,137.240,96.393
2016-01-01 00:00:02.000,77.590,37.885
2016-01-01 00:00:03.000,96.024,34.707
2016-01-01 00:00:04.000,135.508,90.674
2016-01-01 00:00:05.000,122.303,62.433
2016-01-01 00:00:06.000,124.219,60.076
"""

import argparse


parser = argparse.ArgumentParser()
parser.description = 'Create sample ini file for use with PI Connector for UFL'

parser.add_argument('tags', metavar='N', type=str, nargs='+',
                    help='an tag used in the ini')
parser.add_argument('--style', dest='styling', action='store_const',
                    const=2, default=1,
                    help='pick a style for the formating')

args = parser.parse_args()

'''
parser.description = 'Create sample ini file for use with PI Connector for UFL'
parser.add_argument('format',
                    help='specify sample format to generate. '
                         'Select one of: value, values',
                    action=CheckArgumentAction)
sample = parser.parse_args().format
'''

print('[FIELD]')

# Timestamp in standard UTC format
print('Field(1).NAME = "Timestamp"')
print('Field(1).TYPE = "DateTime"')
print('Field(1).FORMAT = "yyyy-MM-dd hh:mm:ss.nnn"')

print()
offset = 2
for index, tag in enumerate(args.tags):
    print("' Field for the tag {0}".format(tag))
    print('Field({0}).NAME = "{1}"'.format(index + offset, tag))
    print('Field({0}).TYPE = "String"'.format(index + offset))
    print()

offset += index + 1

for index, tag in enumerate(args.tags):
    print("' Field for the tag {0}".format(tag))
    print('Field({0}).NAME = "{1}_value"'.format(index + offset, tag))
    print('Field({0}).TYPE = "Number"'.format(index + offset))
    print()


print('[MSG]')
print('MSG(1).NAME = "Tag_Defintion"')
print('MSG(2).NAME = "Values"')

l = len(args.tags)
print()
print('[Tag_Defintion]')
print('Tag_Defintion.FILTER= C1 == "Time*"')
for index, tag in enumerate(args.tags):
    print('{0}=["{1}(*){2}"]'.format(tag, '*,'*(index+1), ',*'*(l-index-1)))

print()
print('[Values]')
# This filter depends on the particular choice of the datetimeformat
print('Values.FILTER = C1=="*-*-*"')
print('Timestamp=["(*),*"]')

for index, tag in enumerate(args.tags):
    print('{0}=["{1}(*){2}"]'.format(tag+'_value',
                                     '*,'*(index+1),
                                     ',*'*(l-index-1)))

print()
for index, tag in enumerate(args.tags):
    print("StoreEvent({0}, , Timestamp, {1}, , )".format(tag, tag+'_value'))
