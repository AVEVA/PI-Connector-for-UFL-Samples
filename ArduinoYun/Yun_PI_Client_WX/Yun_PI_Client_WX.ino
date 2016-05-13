#include <Wire.h>
#include <FileIO.h>
#include <Bridge.h>
#include <Process.h>
#include <ArduinoJson.h>            //ArduinoJSON serialization library
#include <SparkFunMPL3115A2.h>      //Library for Pressure sensor on SparkFun Weather Shield
#include <SparkFunHTU21D.h>         //Library for Humidity sensor on SparkFun Weather Shield

//Pin definitions
const byte REFERENCE_3V3 = A3;      //Reference voltage 3.3 on analog pin 3
const byte LIGHT = A1;              //Light level sensor on analog pin 1
const byte BlueLED = 7;             //Blue LED on SparkFun Weather Shield is digital pin 7
const byte GreenLED = 8;            //Green LED on SparkFun Weather Shield is digital pin 8

//Global variables
String unixTimeStamp;               //Unix time used for file naming and JSON data
Process p;                          //Process object used to run Linux commands on OpenWRT

//Setup routine
void setup()
{
  //Set pin modes for status LEDs
  pinMode(BlueLED, OUTPUT);         //Status LED Blue
  pinMode(GreenLED, OUTPUT);        //Status LED Green

  //Turn on both LEDs for startup
  digitalWrite(BlueLED, HIGH);
  digitalWrite(GreenLED, HIGH);
 
  //Open Bridge, Console, and FileSystem
  Bridge.begin();
  Console.begin();
  FileSystem.begin();
  
  //Startup complete. Turn off LEDs.
  digitalWrite(BlueLED, LOW);
  digitalWrite(GreenLED, LOW);
}

//Loop routine
void loop()
{  
  //Turn on green LED during data read
  digitalWrite(GreenLED, HIGH);

  //Create JSON buffer and root JSON object
  StaticJsonBuffer<128> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();

  //Gather all data and serialize to JSON
  systemData(root);
  weatherData(root);

  //Data read complete. Turn off green LED.
  digitalWrite(GreenLED, LOW);

  //Initatie file stream and save. Turn on blue LED.
  digitalWrite(BlueLED, HIGH);

  //Build file path to new JSON file (always 26 chars + null terminator), using Unix timestamp
  char filePath[27];
  String filePathStr;
  filePathStr = "/json/json_" + unixTimeStamp + ".json";
  filePathStr.toCharArray(filePath, 27);

  //Check for existance of /json directory and create if not
  FileSystem.mkdir("/json");

  //Write formated JSON to file stream
  File dataFile = FileSystem.open(filePath, FILE_WRITE);
  if (dataFile) {
    root.prettyPrintTo(dataFile);
    dataFile.close();
  }

  //File save complete. Turn off blue LED.
  digitalWrite(BlueLED, LOW);
}

void systemData(JsonObject& root)
{
  //Get the Yun system timestamp
  unixTimeStamp = getUnixTimestamp();

  //Get the Yun cpu load
  char cpu[5];
  getSystemCpu(cpu);

  //Add key-value pairs for system data to JSON buffer
  root["time"]            = unixTimeStamp;
  root["device"]          = "ArduinoYun_00F9";    //Enter your unique device name here.
  root["cpu_1min_avg"]    = (float)atof(cpu);
  root["sketch_uptime_s"] = millis()/1000;
}

void weatherData(JsonObject& root)
{
  MPL3115A2 mpl;        //Create an instance of the pressure sensor
  HTU21D htu;           //Create an instance of the humidity sensor
  mpl.begin();          //Start the pressure sensor
  htu.begin();          //Start the humidity sensor

  //Add key-value pairs for ambient conditions data to JSON buffer
  root["relative_humidity"] = (htu.readHumidity());
  root["temperature_C"]     = (htu.readTemperature());
  root["pressure_kPa"]      = (mpl.readPressure()/1000);
  root["light_lux"]         = (3.3 / analogRead(REFERENCE_3V3) * analogRead(LIGHT) * 3000 / 4.6);
}

String getUnixTimestamp()
{
  //This method gets system time as a unix timestampfrom OpenWRT
  //Returns a String
  char unixtime[11];
  int i = 0;
  p.begin("date");
  p.addParameter("+%s");
  p.run();
  
  while (p.available() > 0) {
    unixtime[i] = p.read();
    i++;
  }
  unixtime[10] = '\0';
  return String(unixtime);
}

void getSystemCpu(char cpu[5])
{
  //This method gets CPU 1min avg load information from OpenWRT 
  //using the Process class (which is a global variable, 'p').
  //Output format from /proc/loadavg (we want only the first 4 chars):
  //1.43 0.80 0.74 2/57 7617
  
  int j = 0;            //Loop counter

  //Initiate call to cat /proc/loadavg
  p.begin("cat");       
  p.addParameter("/proc/loadavg"); 
  p.run();

  //Loop through results, take the first 4 chars, discard the rest
  while(p.available() > 0){
    if(j < 4)
      cpu[j] = p.read();
    else
      p.read();
    j++;
  }
  
  //Add the c-string null terminator
  cpu[4] = '\0';
}

