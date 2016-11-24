# PI-Connector-for-UFL-Samples -- INI_FILE_EXAMPLES

These samples show how to create and INI configuration file for diffrents kinds of data. Every example is set of three files:

* INI configuration file (including comments)
* Data file (you can use this file as a source of data during the test)

## Contents

* Example1 - Batch data (set of tagname,timestamp,value)
* Example2 - Line data with hardcoded columns, SECONDS_GMT + miliseconds
* Example3 - Structured matrix, bad data handling, ISNUMBER() function
* Example4 - Structured matrix with tagnames in multiple rows, combination of DATE and TIME
* Example5 - Multiple columns with varying number of columns, modifying the whole MESSAGE
* Example6 - Simple time series with AF Elements (static and dynamic attributtes)
* Example7 - Simple time series with AF Elements created by connector in advance
* Example8 - Process XML data into timeseries
* Example9 - Process XML data into timeseries and AF Elements
* Example10 - Process XML data into timeseries, AF Elements and conditional Event Frames
* Example11 - Adjusting Timestamp based on timezone information

## Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.0.0.41).
The UFL connector will automatically create tags and elements, thus care must be taken when using these examples against a production system.

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
