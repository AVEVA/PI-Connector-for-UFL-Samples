# PI-Connector-for-UFL-Samples - JSON

This sample shows how to get started with the PI Connector for UFL and in particular how to use the REST endpoint of the connector and how to handle JSON files.

## Contents

* A Python script that is designed to get data from a publically available data source and send the collected data to the UFL REST endpoint.
* A sample ini file to show how to parse a simple JSON file.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.0.0.41).
The python script to send data have been tested with Pyhon 3.5.1 and require the use of the request module.
The example ini file parses currency data that is public available at [http://fixer.io/](fixer.io), in particular it used to parse data from URLs such as: 
[http://api.fixer.io/latest?base=USD](http://api.fixer.io/latest?base=USD)

## Requirements

The script and ini file were tested only with the following versions.

* PI connector for UFL - Version 1.0.0.41
* Python - 3.5.1
* Requests Python module - 2.9.1

## Tutorial on how to use these scripts

1. Open the PI Connector for UFL admin page by opening a browser and visiting: [https://{servername}:{port}/admin/ui/](https://{servername}:{port}/admin/ui/).
1. Specify a PI Data Archive and create a new data source and name it, say with currency.
1. Upload fixer.ini as the Config File and select a User Name and Password.
1. Make the following choices:
* Select REST as the Data Source Type
* Leave New Line as blank
* Select UTC for Incoming TimeStamps
1. Save the data source and reopen it. The Address field will now be populated.
1. Copy the url in the Address field and navigate to the folder where the Python sample code is stored.
1. Run the command below to send data.

    `python putJSONdata.py https://{servername}:{port}/connectordata/currency http://api.fixer.io/latest?base=USD`
1. Enter the specified user name and password.
1. You can now look up, for example, that the ufl.USD_to_JPY was created with today's currency exchange rate.
1. If you also register a PI Asset Server, this will also create an element with name the base currency and each other currency rate will be stored as attributes.
1. You can track several different currencies by requesting data using different URL parameters, such as: [http://api.fixer.io/latest?base=JPY](http://api.fixer.io/latest?base=USD)

## Note on the parsing of the JSON data

The web service, [http://api.fixer.io/latest?base=USD](http://api.fixer.io/latest?base=USD) returns data as follows:

    {"base":"USD","date":"2016-03-24","rates":{"AUD":1.3321,"BRL":3.7041,"CAD":1.3288,"BGN":1.7535,[...],"EUR":0.89654}}

So, one long line of data containing a single JSON object. This is tricky, but not impossible to parse using UFL. To simplify things, we can use the python json module to "pretty print" the JSON data, this is on [Line 54](https://github.com/osisoft/PI-Connector-for-UFL-Samples/blob/master/JSON/Currency/putJSONdata.py#L69) of the script. The output is now as below and much easier to parse.

    {
        "base": "USD",
        "date": "2016-03-24",
        "rates": {
            "AUD": 1.3321,
            "BGN": 1.7535,
            [...],
            "ZAR": 15.497
        }
    }

To see a full example of the data, please see the `example_dat.dat` file.

## Maintainers

* [Jerome Lefebvre](https://github.com/jeromelefebvre)

## PI Square

You discuss and post feedback on this project on the associated [PI Square Blog post](https://pisquare.osisoft.com/people/jlefebvre/blog/2016/03/30/get-public-json-data-into-pi-using-the-pi-connector-for-ufl)

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
