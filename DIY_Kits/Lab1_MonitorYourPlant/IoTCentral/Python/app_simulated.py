from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
import os, asyncio, json, time, random
from dotenv import load_dotenv

load_dotenv()
id_scope = os.getenv('ID_SCOPE')
device_id = os.getenv('DEVICE_ID')
primary_key = os.getenv('PRIMARY_KEY')

# Initial
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

def getTelemetryData():
    temp = getTemperature()
    moisture = getMoisture()
    pressure = getPressure()
    humidity = getHumidity()
    light = getLight()
    data = {
        "humidity": humidity,
        "pressure": pressure,
        "temperature": temp,
        "soil_moisture": moisture,
        "light": light
    }

    return json.dumps(data)

async def main():
    # provision the device
    async def register_device():
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host='global.azure-devices-provisioning.net',
            registration_id=device_id,
            id_scope=id_scope,
            symmetric_key=primary_key)

        return await provisioning_device_client.register()

    results = await asyncio.gather(register_device())
    registration_result = results[0]

    # build the connection string
    conn_str='HostName=' + registration_result.registration_state.assigned_hub + \
                ';DeviceId=' + device_id + \
                ';SharedAccessKey=' + primary_key

    # The client object is used to interact with Azure IoT Central.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    # connect the client.
    print('Connecting')
    await device_client.connect()
    print('Connected')

    # async loop that sends the telemetry
    async def main_loop():
        while True:
            telemetry = getTelemetryData()
            print(telemetry)

            await device_client.send_message(telemetry)
            await asyncio.sleep(30)

    await main_loop()

    # Finally, disconnect
    await device_client.disconnect()

if __name__ == '__main__':
    # python3.7 or newer
    asyncio.run(main())

    # python3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())