/*  AgroHack on Arduino Uno WiFi Rev. 2
    with additions:
        * On board watering check for redundancy (in case connection to Azure breaks)
*/

#include <SPI.h>
#include <WiFiNINA.h>
#include <WiFiUdp.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>

/*  You need to go into this file and change this line from:
      #define MQTT_MAX_PACKET_SIZE 128
    to:
      #define MQTT_MAX_PACKET_SIZE 512
*/
#include <PubSubClient.h>

#include "./sha256.h"
#include "./base64.h"
#include "./utils.h"
#include "./config.h"   //use different config file to store secret data ;) - delete line when download
//#include "./configure.h"  //uncomment when download

bool wifiConnected = false;
bool mqttConnected = false;

String iothubHost;
String deviceId;
String sharedAccessKey;

String url;
char *devKey;
long expire;
String sasToken;
String username;

WiFiSSLClient wifiClient1;
PubSubClient *mqtt_client = NULL;

#define TELEMETRY_SEND_INTERVAL 10000 //600000  // telemetry data sent every 10'' or 10'
#define SENSOR_READ_INTERVAL 5000 //595000     // read sensors every 5'' or 9' 55'' 
#define WATERING_CHECK_INTERVAL 20000 //900000  //check if watering needed every 20'' or 15'

long lastTelemetryMillis = 0;
long lastSensorReadMillis = 0;

long lastWateringCheck = 0;

//telemetry data
float temperature = 27, 
    humidity = 50,
    soilMoisture = 50,
    pressure = 101;

//Sensors
DHT dht(11, DHT11); //temperature and humidity sensor

#define SOIL_MOISTURE_SENSOR_PIN A0

#define WATERING_PIN 13     //plant watering indicator LED

// IoT Hub MQTT publish topics
static const char IOT_EVENT_TOPIC[] = "devices/{device_id}/messages/events/";
static const char IOT_DIRECT_METHOD_RESPONSE_TOPIC[] = "$iothub/methods/res/{status}/?$rid={request_id}";

// IoT Hub MQTT subscribe topics
static const char IOT_DIRECT_MESSAGE_TOPIC[] = "$iothub/methods/POST/#";


// Grab the current time from internet time service
unsigned long getNow()
{
    IPAddress address(129, 6, 15, 28); // time.nist.gov NTP server
    const int NTP_PACKET_SIZE = 48;
    byte packetBuffer[NTP_PACKET_SIZE];
    WiFiUDP Udp;
    
    Udp.begin(2390);

    memset(packetBuffer, 0, NTP_PACKET_SIZE);
    packetBuffer[0] = 0b11100011;     // LI, Version, Mode
    packetBuffer[1] = 0;              // Stratum, or type of clock
    packetBuffer[2] = 6;              // Polling Interval
    packetBuffer[3] = 0xEC;           // Peer Clock Precision
    packetBuffer[12]  = 49;
    packetBuffer[13]  = 0x4E;
    packetBuffer[14]  = 49;
    packetBuffer[15]  = 52;
    
    Udp.beginPacket(address, 123);
    Udp.write(packetBuffer, NTP_PACKET_SIZE);
    Udp.endPacket();

    // wait to see if a reply is available
    int waitCount = 0;
    while (waitCount < 20)
    {
        delay(500);
        waitCount++;
        if (Udp.parsePacket() )
        {
            Udp.read(packetBuffer, NTP_PACKET_SIZE);
            
            unsigned long highWord = word(packetBuffer[40], packetBuffer[41]);
            unsigned long lowWord = word(packetBuffer[42], packetBuffer[43]);
            unsigned long secsSince1900 = highWord << 16 | lowWord;

            Udp.stop();
            
            Serial.println("Got current time!");
            
            return (secsSince1900 - 2208988800UL);
        }
    }
    Serial.println("Failed to get current time. :(");
    return 0;
}

//Split the connection string into it's composite pieces
void splitConnectionString()
{
    String connStr = (String)iotConnStr;
    int hostIndex = connStr.indexOf("HostName=");
    int deviceIdIndex = connStr.indexOf(";DeviceId=");
    int sharedAccessKeyIndex = connStr.indexOf(";SharedAccessKey=");
    
    iothubHost = connStr.substring(hostIndex + 9, deviceIdIndex);
    deviceId = connStr.substring(deviceIdIndex + 10, sharedAccessKeyIndex);
    sharedAccessKey = connStr.substring(sharedAccessKeyIndex + 17);
}

//Process direct method requests
void handleDirectMethod(String topicStr, String payloadStr)
{
    String msgId = topicStr.substring(topicStr.indexOf("$RID=") + 5);
    String methodName = topicStr.substring(topicStr.indexOf("$IOTHUB/METHODS/POST/") + 21, topicStr.indexOf("/?$"));
    
    Serial_printf("Direct method call:\n\tMethod Name: %s\n\tParameters: %s\n", methodName.c_str(), payloadStr.c_str());
    
    if (strcmp(methodName.c_str(), "NEEDS_WATERING") == 0)
    {
        // acknowledge receipt of the command
        String response_topic = (String)IOT_DIRECT_METHOD_RESPONSE_TOPIC;
        
        response_topic.replace("{request_id}", msgId);
        response_topic.replace("{status}", "200");  //OK
        mqtt_client->publish(response_topic.c_str(), "");

        lastWateringCheck = millis();
        
        //time to water plant!
        if(payloadStr == "true")
            digitalWrite(WATERING_PIN, HIGH);
        else
            digitalWrite(WATERING_PIN, LOW);
        
    }
}

//Callback for MQTT subscriptions
void callback(char* topic, byte* payload, unsigned int length)
{
    String topicStr = (String)topic;
    topicStr.toUpperCase();
    payload[length] = '\0';
    String payloadStr = (String)((char*)payload);

    if (topicStr.startsWith("$IOTHUB/METHODS/POST/")) // direct method callback
        handleDirectMethod(topicStr, payloadStr);
        
    else // unknown message
        Serial_printf("Unknown message arrived [%s]\nPayload contains: %s", topic, payloadStr.c_str());
}

//Connect to Azure IoT Hub via MQTT
void connectMQTT(String deviceId, String username, String password)
{
     if(mqttConnected)
    {
        mqtt_client->disconnect();
        mqttConnected = false;
    }

    Serial.println("\nStarting IoT Hub connection");
    
    int retry = 0;
    
    while(retry < 10 && !mqtt_client->connected())
    {     
        if (mqtt_client->connect(deviceId.c_str(), username.c_str(), password.c_str()))
        {
                Serial.println("===> mqtt connected");
                mqttConnected = true;
        }
        else
        {
            Serial.print("---> mqtt failed, rc=");
            Serial.println(mqtt_client->state());
            delay(2000);
            retry++;
        }
    }
}

//Create an IoT Hub SAS token for authentication
String createIotHubSASToken(char *key, String url, long expire)
{
    url.toLowerCase();
    String stringToSign = url + "\n" + String(expire);
    int keyLength = strlen(key);

    int decodedKeyLength = base64_dec_len(key, keyLength);
    char decodedKey[decodedKeyLength];

    base64_decode(decodedKey, key, keyLength);

    Sha256 *sha256 = new Sha256();
    sha256->initHmac((const uint8_t*)decodedKey, (size_t)decodedKeyLength);
    sha256->print(stringToSign);
    char* sign = (char*) sha256->resultHmac();
    int encodedSignLen = base64_enc_len(HASH_LENGTH);
    char encodedSign[encodedSignLen];
    base64_encode(encodedSign, sign, HASH_LENGTH);
    delete(sha256);

    Serial.println("SAS Token created!");

    //this works
    return "SharedAccessSignature sr=" + url + "&sig=" + urlEncode((const char*)encodedSign) + "&se=" + String(expire);
    
    //SharedAccessSignature sig={signature-string}&se={expiry}&sr={URL-encoded-resourceURI}  (From https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-mqtt-support#using-the-mqtt-protocol-directly-as-a-device)
    //the above format doesn't work for some reason
    //return "SharedAccessSignature sig=" + url + "&se=" + String(expire) + "&sr=" + urlEncode((const char*)encodedSign);
}

//read sensor data
void readSensors()
{
    soilMoisture = analogRead(SOIL_MOISTURE_SENSOR_PIN);
    soilMoisture = 100 - soilMoisture * 100 / 1023;   //sensor value: 0-1023; we want percentage

    temperature = dht.readTemperature();

    humidity = dht.readHumidity();

    pressure = random(60, 250);
}

 //Establish connection to IoT Hub server
void connectToIoTHub()
{
    Serial.print("Connecting to IoT Hub server...");

   if(wifiConnected)
    {    
        wifiClient1.stop();
        wifiConnected = false;
    }
    if(mqttConnected)
    {
        mqtt_client->disconnect();
        mqttConnected = false;
    }
    
    delay(1000);

    while(!wifiClient1.connect(iothubHost.c_str(), 8883))
    {
        Serial.println("--");
        delay(1000);
    }

    delay(1000);

    wifiConnected = true;
    // Serial.println(wifiClient1.status());
    // Serial.println(wifiClient1.remotePort());

    Serial.println("Connected!");
    // Serial.println(wifiClient1.status());
    // Serial.println(wifiClient1.remotePort());
    
    mqtt_client = new PubSubClient(iothubHost.c_str(), 8883, wifiClient1);
    
    connectMQTT(deviceId, username, sasToken);
    
    mqtt_client->setCallback(callback);

    // add subscriptions - direct messages
    mqtt_client->subscribe(IOT_DIRECT_MESSAGE_TOPIC);
}

//Check to see if plant needs watering
void checkWatering()
{
    if(soilMoisture < 40)
        digitalWrite(WATERING_PIN, HIGH);
    else
        digitalWrite(WATERING_PIN, LOW);
}

// arduino setup function: called once at device startup
void setup()
{
    Serial.begin(115200);

    while(!Serial) ;    //wait for serial monitor to open

    dht.begin();

    pinMode(WATERING_PIN, OUTPUT);

    if (WiFi.status() == WL_NO_MODULE)
    {
        Serial.println("Communication with WiFi module failed!");
        while (true);
    }
    
    // attempt to connect to Wifi network:
    Serial.print("WiFi Firmware version is ");
    Serial.println(WiFi.firmwareVersion());

    Serial_printf("Attempting to connect to Wi-Fi SSID: %s ", wifi_ssid);

    int status = WiFi.begin(wifi_ssid, wifi_password);
    
    while (status != WL_CONNECTED)
    {
         Serial.print(".");
        delay(1000);
        status = WiFi.begin(wifi_ssid, wifi_password);
    }

    Serial.println("\nConnected!\n");

    splitConnectionString();
    // create SAS token and user name for connecting to MQTT broker
    url = iothubHost + urlEncode(String("/devices/" + deviceId).c_str());
    devKey = (char *)sharedAccessKey.c_str();
    expire = getNow() + 864000; //expire in 10 days
    sasToken = createIotHubSASToken(devKey, url, expire);
    username = iothubHost + "/" + deviceId + "/api-version=2016-11-14";
    //username = iothubHost + "/" + deviceId + "/?api-version=2018-06-30";

    connectToIoTHub();

    lastTelemetryMillis = millis();
    lastSensorReadMillis = millis();
}

// arduino message loop - do not do anything in here that will block the loop
void loop()
{
    if(!wifiClient1.connected())
    {
        //  this might block the loop, so don't do it
        //  Serial.println("Connection to IoT Central disrupted - Closing and restarting connection");
        //  connectToIoTHub();

        if(lastWateringCheck < WATERING_CHECK_INTERVAL)
        {
            checkWatering();
            lastWateringCheck = millis();
        }
    }
    if (mqtt_client->connected())
    {
        // give the MQTT handler time to do it's thing
        mqtt_client->loop();

        if (millis() - lastSensorReadMillis > SENSOR_READ_INTERVAL)
        {
            readSensors();
            lastSensorReadMillis = millis();
        }
        
        if (millis() - lastTelemetryMillis > TELEMETRY_SEND_INTERVAL)
        {
            Serial.println("Sending telemetry ...");

            String topic = (String)IOT_EVENT_TOPIC;
            topic.replace("{device_id}", deviceId);

            String payload = "{\"temperature\": {temp}, \"humidity\": {hum}, \"soil_moisture\": {moist}, \"pressure\": {p}}";

            payload.replace("{temp}", String(temperature));
            payload.replace("{hum}", String(humidity));
            payload.replace("{moist}", String(soilMoisture));
            payload.replace("{p}", String(pressure));
            
            Serial_printf("\t%s\n", payload.c_str());

            mqtt_client->publish(topic.c_str(), payload.c_str());

            lastTelemetryMillis = millis();
        }
    }
}