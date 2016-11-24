# PI-Connector-for-UFL-Samples - Arduino Yun

These samples show how to get started with getting data off of an Arduino Yun using the PI Connector for UFL REST endpoint feature.

The Arduino Yun can optionally be equiped with a SparkFun Weather Shield for collecting even more data.

More about the Arduino Yun: https://www.arduino.cc/en/Main/ArduinoBoardYun
More about the SparkFun Weather Shield: https://www.sparkfun.com/products/12081

## Contents

* An Arduino sketch (.ino file) that reads data from the Arduino Yun OpenWRT CPU and SparkFun Weather Shield. The sketch serializes the data as JSON and writes text files to the OpenWRT filesystem.
* A Python sample to read the JSON files and then use an HTTP POST command to send the JSON contents of each data file to the UFL REST endpoint.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL. There are three files included:
* Yun_PI_Client_WX.ino - An Arduino sketch that collects data from the OpenWRT CPU and Weather Sheild, then serializes the data as JSON and writes to text files.
* uflpost.py - A python script that will scan the JSON directory and send the contents of each file to the UFL Connector REST endpoint.
* GenericJSON.ini - A UFL ini file that is used to parse generic JSON output.

## Requirements

The script and ini file were tested only with the following versions:
* [PI connector for UFL](https://techsupport.osisoft.com/Products/PI-Interfaces-and-PI-Connectors/PI-Connector-for-UFL/) - Version 1.0.0.41
* [Python](https://docs.python.org/2.7/) - 2.7.3
* [Requests Python module](https://pypi.python.org/pypi/requests) - 2.9.1
* [Arduino IDE] (https://www.arduino.cc/en/Main/Software) - 1.6.9
* [ArduinoJSON] (https://github.com/bblanchon/ArduinoJson) - 5.2.0
* [SparkFunMPL3115A2.h] (https://github.com/sparkfun/MPL3115A2_Breakout) - Commit 428d1a4
* [SparkFunHTU21D.h] (https://github.com/sparkfun/HTU21D_Breakout) - Commit 263c6ee

We're assuming you've already completed the following:
1. Powered up your Arduino Yun, connected to it via Putty and/or SCP, and installed the latest Linino (OpenWRT) distribution.
2. Installed the SparkFun Weather Shield on the GPIO headers of the Arduino Yun. (https://learn.sparkfun.com/tutorials/weather-shield-hookup-guide?_ga=1.136692528.1646002290.1463004260)
3. Connected your Arduino Yun to an available Wi-Fi or wired network.
4. Downloaded and installed the latest Arduino IDE and all supporting libraries (see above).
5. Installed the Python Requests library. To install Python Requests on OpenWRT from a terminal:
	* opkg update
	* opkg install distribute
	* opkg install python-openssl
	* opkg install python-bzip2
	* easy_install pip
	* pip install requests

## Configure the PI UFL Connector
1. Open the PI Connector for UFL admin page by opening a browser and visiting: [https://{servername}:{port}/admin/ui/](https://{servername}:{port}/admin/ui/).
2. Specify a PI Data Archive, PI Asset Server, select an AF database, and specify a root element.
3. Create a new data source, for example "GenericJSON"
4. Upload GenericJSON.ini as the Config File and select a username and password.
5. Make the following choices:
    * Select Rest as the Data Source Type
    * Leave New Line as blank
    * Select UTC for Incoming TimeStamps
6. Save the data source and reopen it. The address field will now be populated. Make note of the endpoint URL.

## Load the Arduino Sketch onto the Arduino Yun
1. Open the Arduino IDE and connect to your Arduino Yun.
2. Load the Yun_PI_Client_WX.ino file.
3. Scroll to line 91 of the sketch and enter your unique device name.
4. Compile and download the sketch onto your Arudino Yun.
5. When both the blue and green LED on the Weather Shield are lit, the sketch is initializing.
6. When the blue and green LED alternately flash, the sketch is writing JSON files to the '/JSON/' directory.

## Load the Python script onto the Arduino Yun
1. Navigate to the folder where the Python sample code is stored.
2. Edit the uflpost.py file and change the following to match your UFL configuration:
	`url = 'https://{myuflhost}:{myport}/connectordata/{myendpoint}/post'
	`un = '{myusername}'
	`pw = '{mypassword}'
3. Save uflpost.py, then copy it onto the Arduino Yun to the /usr/sbin directory.
4. If you want to ensure the uflpost.py file runs at each startup, navigate to /etc/rc.local and add the following line:
	`python /usr/sbin/uflpost.py
5. To run from a terminal, enter the command below to begin sending data.
    `python uflpost.py

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
