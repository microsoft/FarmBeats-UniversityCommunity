# Send Historical Business Kit Data

Telemetry is an automated communications process where data is collected at a remote location and transmitted to receiving equipment for monitoring or analysis.  The FarmBeats Business Kit sensor data is transmitted to an IoT dashboard by default, but the data can be ingested into Azure FarmBeats.  Now that you have created a telemetry client that can access your FarmBeats deployment, and device and sensor metadata, you can send telemetry messages from the FarmBeats Business Kit to Azure FarmBeats.

After a connection is established as an Event Hubs client, you can send messages to the Event Hub as JSON.

## Send a Telemetry Message as the Client

For this part, you will need to install the latest version of the [azure-eventhub](https://pypi.org/project/azure-eventhub/) library in python if you haven't done so before. You can easily do this with the following command:

```bash
pip3 install azure-eventhub
```

For the version 5.1.0 of this library, the event hub connection string has the following format:  

`Endpoint=sb://<yournamespace>.servicebus.windows.net/;SharedAccessKeyName=<yoursharedaccesskeyname>;SharedAccessKey=<yoursharedaccesskey>`

### Python Script

Create a new file `telemetry.py` and copy the following code.

```python
import asyncio, json
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData

EVENTHUBCONNECTIONSTRING = "<EVENT HUB CONNECTION STRING>"
EVENTHUBNAME = "<EVENT HUB NAME>"

message = {
    "deviceid": "<id of the Device created>",
    "timestamp": "<timestamp in ISO 8601 format>",
    "version" : "1",
    "sensors": {
        {
          "id": "<id of the sensor created>",
          "sensordata": [
            {
              "timestamp": "< timestamp in ISO 8601 format >",
              "<sensor measure name (as defined in the Sensor Model)>": <value>
            },
            {
              "timestamp": "<timestamp in ISO 8601 format>",
              "<sensor measure name (as defined in the Sensor Model)>": <value>
            }
          ]
        }
     ]
}

message = json.dumps(message)

async def run():
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=EVENTHUBCONNECTIONSTRING, eventhub_name=EVENTHUBNAME)

    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(message))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)
        print("Message sent.")


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
```

*Note: the instance **sensors** is an array. You can add as many elements as you want. Recall that we defined the values to be doubles.*

--------
*See also: [How to send data from IoT Central to FarmBeats](./Send_data_IoTCentral.md)
