# Connector-Live-Weather

This sample will show how to use the PI Connector for UFL to get and parse live weather data from the [Openweathermap.org](http://openweathermap.org/) API. In this specific example, we are reading the JSON file. You can request a free API key from the site, and make up to 60 calls/hour. We can easily get by making 1-2 calls per hour to the API.

# Contents 
- A Python script which is designed to get the publicly available data and send it to the Connector’s REST endpoint. 
- A sample INI file which shows how to parse the JSON file
- A sample data file from the Connector's directory in %programdata%
- A BAT file designed for easy deployment of the Python script with Windows Task Scheduler.
 
# Getting Started
You will need the PI Connector for UFL and a PI System (Including PI Data archive and PI AF). The INI file is used to parse weather data. In this case, we will be looking at the [Current Weather](http://openweathermap.org/current) option. 

#Requirements
- PI Connector for UFL – Version 1.0.0.41
- Python – Version 3.5.2
- Requests Python Module – 2.9.1

#Tutorial on how to use these scripts
- Open the PI Connector for UFL admin page (https://{servername}:{port}/admin/ui/)
-	Specify a PI Data Archive and create a new data source
-	Upload Montreal - Weather.ini as the configuration file, put the username/password as (pi,pi) 
-	Make the following choices:
-	Select REST as a data type
-	Leave new line as blank
- Select LOCAL for incoming timestamps 
-	Run the command below to send the data:

`Python putJSONdata_mtl_weather_service.py https://{servername}:{port}/connectordata/MTL_Live_Weather`
- You can now see the PI Points created in the PI Data Archive, such as the temperature, weather status, and humidity. 
 
# Notes the Parsing of JSON data
The original JSON data file arrives unformatted and it is not straightforward for the Connector to parse it. 
`{"coord":{"lon":-73.59,"lat":45.51},"sys":{"type":1,"id":3829,"message":0.0052,"country":"CA","sunrise":1472206191,"sunset":1472254907},"weather":[{"id":801,"main":"Clouds","description":"few clouds","icon":"02d"}],"base":"stations","main":{"temp":26.1,"pressure":1014,"humidity":73,"temp_min":25,"temp_max":27.78},"visibility":48279,"wind":{"speed":6.7,"deg":260,"gust":11.8},"clouds":{"all":20},"dt":1472225914,"id":6077243,"name":"Montreal","cod":200}`

Using the Pretty Print Method, we can split this up into a much more usable form:
```
{
    "base": "cmc stations",
    "clouds": {
        "all": 20
    },
    "cod": 200,
    "coord": {
        "lat": 45.51,
        "lon": -73.59
    },
    "dt": 1472226054,
    "id": 6077243,
    "main": {
        "humidity": 73,
        "pressure": 1014,
        "temp": 25.86,
        "temp_max": 28.33,
        "temp_min": 24
    },
    "name": "Montreal",
    "sys": {
        "country": "CA",
        "id": 3829,
        "message": 0.0034,
        "sunrise": 1472206188,
        "sunset": 1472254856,
        "type": 1
    },
    "weather": [
        {
            "description": "few clouds",
            "icon": "02d",
            "id": 801,
            "main": "Clouds"
        }
    ],
    "wind": {
        "deg": 260,
        "gust": 11.8,
        "speed": 6.7
    }
}
```



# Automation
This data is updated every hour or so, so you may want to run the script that often. In order to automate password requests, the username/password were hardcoded in the script. We can call it repetitively using Windows Task Scheduler. In this case, we are launching the script in a BAT file to include all necessary arguments. 

# PI Square
This data source isn't explicitly mentioned in a PI Square post. However, interesting reading would include [this post on creating PI AF elements with the Connector](https://pisquare.osisoft.com/community/all-things-pi/pi-interfaces/blog/2016/08/19/building-a-pi-af-hierarchy-using-the-pi-connector-for-ufl) and [this post on sending JSON data to the connector silently](https://pisquare.osisoft.com/community/all-things-pi/pi-interfaces/blog/2016/08/19/mtl-intern-project-smart-cities-bike-shares-using-the-pi-connector-for-ufl-and-pi-af)


# Licensing 
Copyright 2016 OSIsoft, LLC.
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at
   http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.

Please see the file named LICENSE.md.
