import sense_hat   # Used for controlling the Sense Hat
import datetime    # Used for getting the timestamp
import time        # Used for inserting pauses (sleeps)
import requests    # Used to send the data requests
import json        # Used to parse geolocation JSON
import sys         # Used to parse error messages
import os          # Used to sync the internal clock
import socket      # Used to get the current host name
import webcolors   # Used to allow easily referencing colors by name
# Install a missing library 'XXX' via the terminal command 'pip3 install XXX'

# --------------------------------------------

# Specify the name of this device (use the host name, or hard-code in a name)
#deviceName = "Raspberry PI Sensor Hat Module"
deviceName = socket.gethostname()
# Specify the target URL where data should be sent, along with login creds 
targetURL = "https://changethistoyourservername:5460/connectordata/RaspberryPISenseHatData/"
_u = "changethistoyourusername"
_p = "changethistoyourpassword"

# Define the how often data will be collected and sent
SAMPLE_INTERVAL_SECONDS = 2

# Specify whether the lights should turn off at night;
# if set to true, LEDs will be disabled between 10 PM - 7 AM
NIGHT_MODE_ENABLED = True

# --------------------------------------------

# Define the color bar that will be used for each row of LEDs
RED_TO_GREEN_COLOR_BAR = [
    webcolors.name_to_rgb('MAGENTA'),
    webcolors.name_to_rgb('RED'),
    webcolors.name_to_rgb('ORANGE'),
    webcolors.name_to_rgb('YELLOW'),
    webcolors.name_to_rgb('YELLOWGREEN'),
    webcolors.name_to_rgb('GREEN'),
    webcolors.name_to_rgb('LightSeaGreen'),
    webcolors.name_to_rgb('BLUE')
]
# Specify a default background color for LEDs
DEFAULT_BACKGROUND_COLOR = webcolors.name_to_rgb('navy')

# --------------------------------------------

# Initialize a global array for holding the most recent 8 readings
recentReadings = [1, 1, 1, 1, 1, 1, 1, 1]

# --------------------------------------------

# Begin!
print ("Waiting 10 seconds for sensors to warm up...")
time.sleep(10)
print ("Program beginning...")

# Sync the time on this device to an internet time server
try:
    os.system('sudo service ntpd stop')
    time.sleep(1)
    os.system('sudo ntpd -gq')
    time.sleep(1)
    os.system('sudo service ntpd start')
except:
    print('Error syncing time!')
    
# Initialize the sensor hat object
sense = sense_hat.SenseHat()
print("Sensor hat initialized...")

# Activate the compass, gyro, and accelerometer
sense.set_imu_config(True, True, True)
sense.show_message("Ready!")
print("Gyro initialized...")

# --------------------------------------------

print("Now beginning infinite loop...")
print("This device is called: " + deviceName + "...")
print("Data will be sent to " + targetURL + " every " + str(SAMPLE_INTERVAL_SECONDS) + " seconds...")

while (True):

    # Get the current time
    currentTime = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    # --------------------------------------------

    # Initialize environmental variables to 0
    humidityPercent = 0
    temperatureCelsius = 0
    temperatureFahrenheit = 0
    pressureMillibars = 0
    pitch = 0
    roll = 0
    yaw = 0
    degreesToNorth = 0
    accelerationx = 0
    accelerationy = 0
    accelerationz = 0
    
    # Get environmental data
    try:
        humidityPercent = sense.get_humidity()
        temperatureCelsius = sense.get_temperature_from_humidity()
        temperatureFahrenheit = temperatureCelsius * 9/5 + 32
        pressureMillibars = sense.get_pressure()
        pitch, roll, yaw = sense.get_orientation_degrees().values()
        degreesToNorth = sense.get_compass()
        accelerationx, accelerationy, accelerationz = sense.get_accelerometer_raw().values()
    except:
        print("Error getting sensor data!")
        
    # --------------------------------------------

    # Initialize position variables to 0
    latitudeDegrees = 0
    longitudeDegrees = 0

    # Get position data
    try:
        geolocationServiceURL = 'http://ip-json.rhcloud.com/json'
        geolocationRequest = requests.get(geolocationServiceURL, timeout=5)
        jsonData = json.loads(geolocationRequest.text)
        latitudeDegrees = jsonData['latitude']
        longitudeDegrees = jsonData['longitude']
    except:
        print("Error getting position!")
    
    # --------------------------------------------

    # Append the most recent value to end of the recent values array
    recentReadings.append(accelerationx)
    # Remove the oldest value from bin 0 of the recent values array
    removedValue = recentReadings.pop(0)
    # Get the max and min values of the recent values array
    maxReading = max(recentReadings)
    minReading = min(recentReadings)

    # Scale all values in the recent values array using the max
    # and the range (max - min); values now range from 0 to 7
    scaledRecentReadings = []
    for i in range(0, len(recentReadings), 1):
        scaledRecentReading = int(round(7 * abs(recentReadings[i] - minReading)/abs(maxReading - minReading)))
        # Subtract the scaled value from 7, to 'invert' the value,
        # since the LED display is mounted upside-down
        scaledRecentReadings.append(7 - scaledRecentReading)

    # --------------------------------------------
    
    # Test the hour of day; if it's too late or early, don't show the lights
    currentHour = datetime.datetime.now().hour
    if (NIGHT_MODE_ENABLED and ((currentHour > 22) or (currentHour < 7))):
        # If it's too late or early, sleep 1 second, then turn off the lights
        time.sleep(1)
        sense.clear()
    else:
        # Otherwise, turn on the LEDs!
        # Loop through the array, right to left (7 to 0);
        # This lights up LEDs on the display one column at a time
        for LEDcolumnIndex in range(7, -1, -1):
            # Loop through all 8 LEDs in this column of LEDs
            for LEDrowIndex in range(0, 8, 1):
                # Determine the color for this LED by
                # comparing the row (0-7) that this LED is in
                # to the corresponding scaled recent reading
                if LEDrowIndex >= scaledRecentReadings[LEDcolumnIndex]:
                    # In this case, the row number determines the LED color
                    # Higher row numbers will get "warmer" colors
                    sense.set_pixel(LEDcolumnIndex,LEDrowIndex,
                        RED_TO_GREEN_COLOR_BAR[LEDrowIndex])
                else :
                    # Otherwise, by default, set this LED to the background color
                    sense.set_pixel(LEDcolumnIndex,LEDrowIndex,
                        DEFAULT_BACKGROUND_COLOR)
        
    # --------------------------------------------
    
    # Compose the message in a form suitable for sending
    messageString = (
        deviceName + ":" + "Humidity," + currentTime + "," +  str(humidityPercent) + "\n" +
        deviceName + ":" + "Temperature," + currentTime + "," + str(temperatureCelsius * 9/5 + 32) + "\n" +
        deviceName + ":" + "Pressure," + currentTime + "," + str(pressureMillibars) + "\n" +
        deviceName + ":" + "Heading," + currentTime + "," + str(degreesToNorth) + "\n" +
        deviceName + ":" + "Pitch," + currentTime + "," + str(pitch) + "\n" +
        deviceName + ":" + "Roll," + currentTime + "," + str(roll) + "\n" +
        deviceName + ":" + "Yaw," + currentTime + "," + str(yaw) + "\n" +
        deviceName + ":" + "Latitude," + currentTime + "," + str(latitudeDegrees) + "\n" +
        deviceName + ":" + "Longitude," + currentTime + "," + str(longitudeDegrees) + "\n" +
        deviceName + ":" + "AccelerationX," + currentTime + "," + str(accelerationx) + "\n" +
        deviceName + ":" + "AccelerationY," + currentTime + "," + str(accelerationy) + "\n" +
        deviceName + ":" + "AccelerationZ," + currentTime + "," + str(accelerationz) + "\n"
    )

    # Send the message to the target URL, using the specified creds,
    # containing the above message; use verify=False to allow
    # self-signed certificates, and use a timeout of 5 seconds
    try: 
        request = requests.put(targetURL,
            auth=(_u, _p),
            data=messageString,
            verify=False,
            timeout=5)
        # Notify the user if the request isn't successful
        if (request.status_code != 200):
             print("Error: web request did not return 200!")
    except: 
        print("An error ocurred during the web request: " + str(sys.exc_info()[0]))
    
    # Sleep until the next loop
    time.sleep(SAMPLE_INTERVAL_SECONDS)

