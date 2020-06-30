'''
 Script to send data to FarmBeats using azure-eventhub v1.3.3
 It is uses fake data to test the connection with FarmBeats.
 Once a connection is stablished, you can just modify
 the code to send the data obtained from your sensors.
 '''

import azure, json
from azure.eventhub import EventHubClient, Sender, EventData, Receiver, Offset

EVENTHUBCONNECTIONSTRING = "<CONNECTION STRING TO STORAGE ACCOUNT (ENDS WITH l2qqk)>"
EVENTHUBNAME = "<EVENTHUB NAME>"

write_client = EventHubClient.from_connection_string(EVENTHUBCONNECTIONSTRING, debug=False)
sender = write_client.add_sender(partition="0")
write_client.run()
message = {
    "deviceid":"<DEVICE ID>",
    "timestamp":"2020-05-25T12:52:32.3155488Z",
    "version":"1",
    "sensors":[
        {
            "id":"<SENSOR ID FOR SOIL MOISTURE SENSOR>",
            "sensordata":[
                {
                    "timestamp":"2020-05-25T12:52:32.3155488Z",
                    "capacitive_soil_moisture":79.0
                }
            ]
        },
        {
            "id":"<SENSOR ID FOR LIGHT SENSOR>",
            "sensordata":[
                {
                    "timestamp":"2020-05-25T12:52:32.3155488Z",
                    "grove_light_sensor":90.0
                }
            ]
        },
        {
            "id":"<SENSOR ID OF BME280 SENSOR>",
            "sensordata":[
                {
                    "timestamp":"2020-05-25T12:52:32.3155488Z",
                    "grove_temperature":18.0
                },
                {
                    "timestamp":"2020-05-25T12:52:32.3155488Z",
                    "grove_humidity":56.0
                },
                {
                    "timestamp":"2020-05-25T12:52:32.3155488Z",
                    "grove_barometer":97.0
                }
            ]
        }
    ]
}

message = json.dumps(message)

# This for loop send the same message 5 times.
for i in range(5):
    telemetry = message
    print("Sending telemetry: " + telemetry)
    sender.send(EventData(telemetry))

write_client.stop()
