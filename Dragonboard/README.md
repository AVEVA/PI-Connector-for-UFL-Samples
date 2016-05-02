# PI-Connector-for-UFL-Samples - Dragonboard

These samples show how to get started with getting data off of a Qualcomm Dragonboard the PI Connector for UFL REST endpoint feature.

## Contents

* A Python sample to read some data off the Dragonboard use the a HTTP put command to send the data file to the UFL REST endpoint.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL. There are two files included:
* SendDragonBoardData.py - A python script that will collect data from a Dragonboard, package it as JSON file and send it to the UFL connector.
* DragonBoard.ini - A UFL ini file that is used to parse the JSON output.

## Requirements
The script and ini file were tested only with the following versions.

* [PI connector for UFL](https://techsupport.osisoft.com/Products/PI-Interfaces-and-PI-Connectors/PI-Connector-for-UFL/) - Version 1.0.0.41
* [Python](https://docs.python.org/3.5/) - 3.5.1
* [Requests Python module](https://pypi.python.org/pypi/requests) - 2.9.1
* [Linux Metrics Python module](https://pypi.python.org/pypi/linux-metrics) - 0.1.4

## Tutorial on how to use these scripts
1. Open the PI Connector for UFL admin page by opening a browser and visiting: [https://{servername}:{port}/admin/ui/](https://{servername}:{port}/admin/ui/).
2. Specify a PI Data Archive and create a new data source, say dragonboad
3. Upload DragonBoard.ini as the Config File and select a username and password.
4. Make the following choices:
    * Select Rest as the Data Source Type
    * Leave New Line as blank
    * Select UTC for Incoming TimeStamps
5. Save the data source and reopen it. The address field will now be populated.
6. Copy the url in the address field and navigate to the folder where the Python sample code is stored.
7. Run the command below to send data. Where the second to last argument is the name of the device and the final argument is the sampling rate.

    `python SendDragonBoardData.py https://uflserver:5460/connectordata/dragonboard "Smaug" 10`
7. Enter the specified username and password.
8. You can now look up, for example, that the tag "UFL.Smaug_CPU Usage".

##Licensing

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
