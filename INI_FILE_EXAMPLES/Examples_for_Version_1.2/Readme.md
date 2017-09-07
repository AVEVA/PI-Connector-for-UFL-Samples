These samples show how to create the INI configuration file logic for structured inputs - 
csv and json using the new ForEach(), JsonGetItem() and JsonGetValue() constructs.

Examples 20-24 consist of two files:
•INI configuration file
•Data file (you can use this file as a source of data during the test)

Example 25 uses the REST Client channel; hence, consists only of the INI logic
(the parameterized REST address example is on the top of the INI file)

Contents
•Example20 - csv input matrix with 20 columns. More columns can be added without modifying the INI logic
•Example21 - Shows how to iterate through a json array
•Example22 - Nested loops for more complex json structures
•Example23 - Built in variables - __ITEM_NAME, __ITEM, __MESSAGE,..
•Example24 - Json data types mapped to types UFL and PI support
•Example25 - Example for the REST Client data channel. The final result are AF elements with attributes

Getting Started

You will need a development/test PI System and the PI Connector for UFL (the samples were tested with version 1.2.0). The UFL connector will automatically create tags and elements, thus care must be taken when using these examples against a production system.
