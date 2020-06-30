'''
 Script to send data to FarmBeats using azure-eventhub v5.1.0
 It is uses fake data to test the connection with FarmBeats.
 Once a connection is stablished, you can just modify
 the code to send the data obtained from your sensors.
 '''

import asyncio, json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

EVENTHUBCONNECTIONSTRING = "<CONNECTION STRING TO STORAGE ACCOUNT (ENDS WITH l2qqk)>"
EVENTHUBNAME = "<EVENTHUB NAME>"

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

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
 	    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=EVENTHUBCONNECTIONSTRING, eventhub_name=EVENTHUBNAME)
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(message))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("Message sent.")


# python3.7 or newer
asyncio.run(run())

# python3.6
# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
