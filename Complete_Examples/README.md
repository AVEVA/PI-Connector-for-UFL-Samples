# PI-Connector-for-UFL-Samples -- INI_FILE_EXAMPLES

This sample shows how to send data to the PI Data Archive and PI Asset Framework

## Contents

piuflput.py - Send data to the PI Connector for UFL - REST endpoint
piuflgen.py - Create data to send using piuflput.py
Example6_SimpleTimeSeries_with_AF_Elements.ini - PI Connector for UFL config. script

## Getting Started

You will need:
i.  a development/test PI System
ii. the PI Connector for UFL (the samples were tested with version 1.0.0.41)
iii. python (version 3.x)

Note:
The UFL connector will automatically create point and elements, thus care must be taken when using these examples against a production system.
The UFL connector specifies which PI Asset Framwork database(s) to use. Also, a point prefix can be added if required.

## Usage

1. Configure a data source using the PI Connector for UFL Web Interface
   Use the included .ini file
   Take note of the following for use in step 4.
      -  the REST Address
      -  username and password
2. Create some sample data using the python
   python3 piuflgen.py values > values.csv
3. Get usage information for piuflput.py
   python3 piuflput.py
4. Send data to the PI Connector for UFL REST endpoint where Address was obtained in step 1
   python3 piuflput.py <Address> values.csv
5. Verify the data flowed into the PI System as per configured in the PI Connector for UFL

## Licensing

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
   
Please see the file named [LICENSE.md](LICENSE.md).
