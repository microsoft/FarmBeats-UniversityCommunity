# simulated random data.
import asyncio, os, json
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse
import random

id_scope = "0ne00110FA0"
device_id = "raspberry_pi"
primary_key = "Ol6FChRJn5RQ2I6DDIxOzXtiYZgkeVfHGHoonaueGTQ="

temp = 19.0 # celsius
pressure = 95.0 # kPa
moisture = 62.0 # Percent
humidity = 32.0 # percent

def getTemperature():
    return temp + random.randint(-10, 10)/10

def getPressure():
    return pressure + random.randint(-10, 10)/10

def getMoisture():
    return moisture + random.randint(-10, 10)/5

def getHumidity():
    return humidity + random.randint(-10, 10)/5


def getTelemetryData():
    temp = getTemperature()
    moisture = getMoisture()
    pressure = getPressure()
    humidity = getHumidity()

    data = {
        "humidity": humidity,
        "pressure": pressure,
        "temperature": temp,
        "soil_moisture": moisture,
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

    # listen for commands
    async def command_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request('needs_watering')
            needs_watering = method_request.payload
            print('Needs watering:', needs_watering)
            payload = {'result': True}

            # if needs_watering:
            #     led.on()
            # else:
            #     led.off()

            method_response = MethodResponse.create_from_method_request(
                method_request, 200, payload
            )
            await device_client.send_method_response(method_response)

    # async loop that sends the telemetry
    async def main_loop():
        while True:            
            telemetry = getTelemetryData()
            print(telemetry)

            await device_client.send_message(telemetry)
            await asyncio.sleep(60)

    listeners = asyncio.gather(command_listener(device_client))

    await main_loop()

    # Cancel listening
    listeners.cancel()

    # Finally, disconnect
    await device_client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())