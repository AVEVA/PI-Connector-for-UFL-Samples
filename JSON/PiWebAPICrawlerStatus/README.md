# PI-Connector-for-UFL-Samples - PI Web API Crawler

This samples show how to get started with the PI Connector for UFL REST endpoint feature and displays a particular application of minotoring the status of the PI Web API Crawler.

## Contents

* A Powershell script that is designed to get data from the PI Web API service and send the collected data a folder to be read by the PI Connector for UFL.
* A sample ini file to parse the UFL connector.

## Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.0.0.41).
The PowerShell script will need to be modified to point to a particular installation of a PI Web API installation and the output file path.
The example ini file parses crawler status data from a PI Web API Service [https://{piwebapiservice}/piwebapi/search/sources](https://{piwebapiservice}/piwebapi/search/sources).

You can actively discuss the example on [PI Square](https://pisquare.osisoft.com/people/jlefebvre/blog/2016/03/30/get-public-json-data-into-pi-using-the-pi-connector-for-ufl) as well.

## Requirements

The script and ini file were tested only with the following versions.

* PI connector for UFL - Version 1.0.0.41
* PowerShell - 5.0.10586.117

## Tutorial on how to use these scripts

1. Open the PI Connector for UFL admin page by opening a browser and visiting: [https://{servername}:{port}/admin/ui/](https://{servername}:{port}/admin/ui/).
1. Specify a PI Data Archive and create a new data source and name it, say with CrawlerStatus.
1. Upload PIWebAPICrawlerStatus.ini as the Config File
1. Make the following choices:
* Select File as the Data Source Type, specify a path (this path needs to be the same as the PowerShell script)
* Leave New Line as blank
* Select UTC for Incoming TimeStamps
1. Run the command below to send data.

    `.\PIWebAPICrawlerStatusDownloader.ps1`
1. You can now look up, for example, that the tags starting with "ufl.Coresight.Crawler" have been created and contains information regarding the status of the PI Web API Crawler.
1. If you also register a PI Asset Server, this will also create an element with name the base currency and each other currency rate will be stored as attributes.


## Note on the parsing of the JSON data

The PI Web API always returns data in a JSON format, but this can sometime be tricky to parse. Thus, we use the PowerShell method `ConvertTo-JSON` to format the data in a consitent way.


{
    "Links":  {

              },
    "Errors":  [

               ],
    "Items":  [
                  {
                      "Name":  "pi:DFAPACPI1",
                      "ID":  0,
                      "LastCrawl":  "2016-08-04T05:17:32.4930706Z",
                      "CrawlerHost":  "DFAPACPI1.DFAPAC.int",
                      "State":  2,
                      "ItemCount":  9699,
                      "PercentCrawled":  100,
                      "LastErrorMessage":  null,
                      "GenerateAllPaths":  true,
                      "IsAttemptingToCalculateMultiplePaths":  false,
                      "CrawlerVersion":  "1.4.0.1379"
                  },
                  {
                      "Name":  "af:\\\\DFAPACPI1\\Water World",
                      "ID":  6,
                      "LastCrawl":  "2016-08-04T05:14:03.2927532Z",
                      "CrawlerHost":  "DFAPACPI1.DFAPAC.int",
                      "State":  2,
                      "ItemCount":  49,
                      "PercentCrawled":  100,
                      "LastErrorMessage":  null,
                      "GenerateAllPaths":  true,
                      "IsAttemptingToCalculateMultiplePaths":  false,
                      "CrawlerVersion":  "1.4.0.1379"
                  }
              ]
}

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
