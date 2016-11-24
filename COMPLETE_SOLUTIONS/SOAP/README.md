# PI-Connector-for-UFL-Samples - SOAP/Powershell

These samples show how to get started with the PI Connector for UFL REST endpoint feature.

## Contents

* Powershell sample to get data from a SOAP endpoint and create a data file and then use the a HTTP Put command to send the data file to the UFL REST endpoint.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.0.0.41).
The script to get interact with the SOAP end point and to send the data have been tested with Powershell 5.0.10586.117

## Tutorial on how to use these scripts
1. Open the PI Connector for UFL admin page by opening a browser and visiting: [https://{servername}:{port}/admin/ui/](https://{servername}:{port}/admin/ui/).
2. Specify an AF Server and create a new data source called, for example, Weather
3. Upload WeatherWithEventFrames.ini as the Config File and select a username and password.
4. Make the following choices:
    * Select Rest as the Data Source Type
    * Set NewLine to `<CurrentWeather>`
    * Select UTC for Incoming TimeStamps
5. Save the data source and reopen it. The address field will now be populated.
6. Copy the url in the address field and navigate to the folder where the Powershell sample code is stored.
7. Run the command below to send data (where the username and password are as specified above)

    `.\SendWeatherForSFO.ps1 -url addressfieldurl -userName john -password p@ssw0rd!`
8. You can now look up that several elements were created under the root element you specified. Also, several event frames have been created.

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

