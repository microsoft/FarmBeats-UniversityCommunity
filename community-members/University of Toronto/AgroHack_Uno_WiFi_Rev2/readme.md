# Implementing AgroHack on Arduino UNO WiFi Rev. 2
## University of Toronto Project Team 
## Developer
[Konstantinos Papaspyridis](https://github.com/Gostas)

## What's this about

I was inspired by the AgroHack project (https://github.com/jimbobbennett/AgroHack) and wanted to see if it can be implemented on an even smaller device than the Raspberry Pi. The Arduino Uno WiFi Rev. 2 seemed like the perfect fit to get started with since it has an onboard WiFi and BLE module and more memory than the Uno (48 KB Flash, 6.144 KB SRAM, 256 Bytes EEPROM).

The code was based on firedog1024's repository for connecting the Uno WiFi Rev. 2 to Azure IoT Central (https://github.com/firedog1024/arduino-uno-wifi-iotc).

## What's new

* Uses Arduino Uno WiFi Rev. 2, a cheaper platform than the Raspberry Pi
* New implementation of interfacing with Azure IoT Hub in order to fit Uno Wifi's limited memory.
* Identified a bug in the WiFiNINA library and raised an issue at the library's repo
* Perform the watering checks on board the Arduino in case connection to Azure breaks

## Features

* Uses the onboard u-blox NINA-W102 radio module to communicate with Azure IoT Central using WiFi
* Uses simple MQTT library to communicate with Azure IoT Central
* IoT Central features supported
    * Telemetry data - Temperature, humidity and pressure
    * Commands - Send a message to the device to turn on LED to indicate it's time to water the plant

## Installation

Run:

```
git clone https://github.com/Gostas/AgroHackUnoWiFi.git   
```

## Prerequisite

Install the Arduino IDE and the necessary drivers for the Arduino Uno WiFi Rev2 board and ensure that a simple LED blink sketch compiles and runs on the board. Follow the getting started guide here https://www.arduino.cc/en/Guide/ArduinoUnoWiFiRev2.

This code requires a couple of libraries to be installed for it to compile. To install an Arduino library open the Arduino IDE and click the "Sketch" menu and then "Include Library" -> "Manage Libraries". In the dialog filter by the library name below and install the latest version. For more information on installing libraries with Arduino see https://www.arduino.cc/en/guide/libraries.

* Install library "WiFiNINA"
* Install library "PubSubClient"
* Install library "DHT sensor library" by Adafruit


***Note*** - We need to increase the payload size limit in PubSubClient to allow for the larger size of MQTT messages from Azure IoT Hub. I have found that the crossover point where the Arduino can't connect over MQTT is somewhere between 256 and 512 bytes. Open the file at %HomePath%\Documents\Arduino\libraries\PubSubClient\src\PubSubClient.h in your favorite code editor. Change the line (line 26 in current version):

```
#define MQTT_MAX_PACKET_SIZE 128
```

to:

```
#define MQTT_MAX_PACKET_SIZE 512
```

Save the file and you have made the necessary fix.

Also, we need to create the application in Azure IoT Central and setup Azure Analytics, Storage, Maps and Functions. For that, I followed the steps provided in AgroHack, beginning with creating the creating the application (https://github.com/jimbobbennett/AgroHack/blob/master/Steps/CreateTheAppInIoTCentral.md).

## Wiring

I am using the DHT 11 sensor for humidity and temperature and a generic soil moisture sensor. I currently do *not* have a pressure sensor, so the program generates random values for pressure instead. Feel free to add a pressure sensor tho :).
![circuit diagram](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/AgroHack_circuit.png?raw=true)

## Configuration

We need to copy some values from our new IoT Central device into the configure.h file so it can connect to IoT Central. 

There is a tool called DPS KeyGen that given device and application information can generate a connection string to the IoT Hub:

```
git clone https://github.com/Azure/dps-keygen.git
```

in the cloned directory, navigate to the bin folder and choose the correct folder for your operating system (for Windows you will need to unzip the .zip file in the folder).

We now need to grab some values from our application in IoT Central. Go to your application, click on "Devices", then "Environment Sensor" and then onto your device:


![path to device in iot central](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/path_to_device_iot_central_v3.png?raw=true)


Now click on connect:


![connect button](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/connect_button_v3.png?raw=true)


You will need to use the values from "Scope id", "Device id" and "primary key":


![device connection menu](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/device_connection_menu_v3.png?raw=true)

Using the command line UX type:

cd dps-keygen\bin\windows\dps_cstr
dps_cstr <scope_id> <device_id> <primary_key>  //subsitute your values in


```
HostName=iotc-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx.azure-devices.net;DeviceId=<your device id>;SharedAccessKey=zyGZtz6r5mqta6p7QXOhlxR1ltgHS0quZPgIYiKb9aE=
```

We need to copy this value from the command line to the configure.h file and paste it into the iotConnStr[] line, the resulting line will look something like this.

```
static char iotConnStr[] = "HostName=<host name>.azure-devices.net;DeviceId=<device id>;SharedAccessKey=<shared access key>";
```

You will also need to provide the Wi-Fi SSID (Wi-Fi name) and password in the configure.h

```
// Wi-Fi information
static char wifi_ssid[] = "<replace with Wi-Fi SSID>";
static char wifi_password[] = "<replace with Wi-Fi password>";
```

Finally, fill in the following variables with your house's geographical coordinates. You can find instructions on how to do so at https://github.com/jimbobbennett/AgroHack/blob/master/Steps/CheckWeatherWithAzureMaps.md.

```
//house coordinates
const float latitude = 0.0;     //replace with your latitude
const float longitude = 0.0;    //replace with your longitude
```

## Telemetry:

If the device is working correctly you should see output like this in the serial monitor that indicates data is successfully being transmitted to Azure IoT Central:

![serial monitor displaying telemetry sent](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/arduino_telemetry_sent_v3.png?raw=true)



Also, go to your Arduino Uno WiFi device on IoT Central and check if the telemetry is received:

![iot central receives and displays telemetry](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/iot_central_environment_monitoring_v3.png?raw=true)

## Commands:

You can send a command to the Arduino from IoT Central manually:

![serial monitor displaying telemetry sent](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/iot_central_command_v2.png?raw=true)



When the NEEDS_WATERING command gets received by the Arduino, the red LED should light up if it's not already on and you should see the following output on the serial monitor:

![serial monitor displays command received](https://github.com/Gostas/AgroHack_Uno_WiFi_Rev2/blob/master/assets/arduino_command_received.png?raw=true)
