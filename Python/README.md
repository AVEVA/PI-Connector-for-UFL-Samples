# PI-Connector-for-UFL-Samples - PYTHON

These samples show how to get started with the PI Connector for UFL REST endpoint feature.

## Contents

* Details on how to use of the PI Connector for UFL REST endpoint.
* Python3 samples to create a data file and then use the a HTTP Put or Push command to send the data file to the UFL REST endpoint.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.0.0.41).
The scripts have been tested with Pyhon 3.5.1 and come in two versions. 
* piuflput.py - uses the Python requests module (instal using: pip install requests or apt-get install python-requests)
* piuflput_urllib.py - uses only Python modules that are part of a standard install of Python3.
The file [PI Connector for UFL REST samples](PI Connector for UFL REST samples.pdf) provides additional details about the samples.

## Tutorial on how to use these scripts
1. Open the PI Connector for UFL admin page by opening a browser and visiting: https://<servername>:<port>/admin/ui/
2. Create a new data source
3. Upload value.ini as the Config File and select a username and password
4. Make the following choices:
    * Select Rest as the Data Source Type
    * Leave New Line as blank
    * select UTC for Incoming TimeStamps
5. Save the data source and reopen it. The Address field will now be populate it
6. Copy the url and navigate to the folder where the Python sample code is stored
7. run the command below to send data
    `python url value.csv`
8. You can now look up in, that the tag 00-00-00-b2-11-1a:rpm was created at the utc time: 2015-11-13T04:05:54Z there is the value of 1968
9. To generate more data with current timestamps you can run the command:
    `python piuflgen.py value > morevalues.csv`
10. For an other example, you re-run the previous steps using values instead of value.

##Licensing

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
   
Please see the file named [LICENSE.md](LICENSE.md).

