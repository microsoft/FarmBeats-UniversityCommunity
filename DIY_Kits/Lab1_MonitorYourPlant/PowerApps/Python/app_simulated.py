# simulated random data.
import time, json, asyncio, random
from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime, date
from dotenv import load_dotenv

load_dotenv()
connectionString = os.getenv('CONNECTION_STRING')

temp = 19.0 # celsius
pressure = 95.0 # kPa
moisture = 62.0 # Percent
humidity = 32.0 # percent
light = 50.0 # percent

def getTemperature():
    return temp + random.randint(-10, 10)/10

def getPressure():
    return pressure + random.randint(-10, 10)/10

def getMoisture():
    return moisture + random.randint(-10, 10)/5

def getHumidity():
    return humidity + random.randint(-10, 10)/5

def getLight():
    return light + random.randint(-10, 10)/5

def getDate():
    now = datetime.now()
    return now.strftime("%Y/%m/%d"), now.strftime("%H:%M:%S")

def getTelemetryData():
    temp = getTemperature()
    moisture = getMoisture()
    pressure = getPressure()
    humidity = getHumidity()
    light = getLight()
    date, time = getDate()
    data = {
        "date": date,
        "time": time,
        "humidity": humidity,
        "pressure": pressure,
        "temperature": temp,
        "soil_moisture": moisture,
        "light": light
    }

    return json.dumps(data)

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

async def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("Conected, press Ctrl + C to exit")

        while True:
            message = getTelemetryData()

            print(message)
            await client.send_message(message)

            # sleep 10 secons
            await asyncio.sleep(30)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")
        await client.disconnect()

if __name__ == '__main__':
    print("IoT Hub Connection")
    # python3.7 or newer
    asyncio.run(iothub_client_telemetry_sample_run())

    # python3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(iothub_client_telemetry_sample_run())
