from azure.iot.device.aio import IoTHubDeviceClient
from datetime import datetime, date
import smbus2, bme280, os, asyncio, json, time
from grove.grove_moisture_sensor import GroveMoistureSensor
from dotenv import load_dotenv
from grove.grove_light_sensor_v1_2 import GroveLightSensor

# Configuration parameters
bme_pin = 1
bme_address = 0x76
moisture_pin = 2
light_pin = 0

# Create the sensors
bus = smbus2.SMBus(bme_pin)
calibration_params = bme280.load_calibration_params(bus, bme_address)

moisture_sensor = GroveMoistureSensor(moisture_pin)

light_sensor = GroveLightSensor(light_pin)

load_dotenv()
connectionString = os.getenv('CONNECTION_STRING')

def getTemperaturePressureHumidity():
    return bme280.sample(bus, bme_address, calibration_params)

def getMoisture():
    return round(moisture_sensor.moisture, 2)

def getLight():
    return round(light_sensor.light, 2)/10

def getDate():
    now = datetime.now()
    return now.strftime("%Y/%m/%d"), now.strftime("%H:%M:%S")

def getTelemetryData():
    temp = round(getTemperaturePressureHumidity().temperature, 2) # degrees Celsius
    moisture = getMoisture() # voltage in mV
    pressure = round(getTemperaturePressureHumidity().pressure, 2)/1000 # kPa
    humidity = round(getTemperaturePressureHumidity().humidity, 2) # % relative Humidity
    light = getLight() # % Light Strenght
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
    client = IoTHubDeviceClient.create_from_connection_string(connectionString)
    return client

async def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("Conected, press Ctrl + C to exit")

        while True:
            message = getTelemetryData()

            print(message)
            await client.send_message(message)

            # sleep 30 seconds
            await asyncio.sleep(30)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")
        await client.disconnect()

if __name__ == '__main__':
    print("IoT Hub Connection")
    # python3.7
    asyncio.run(iothub_client_telemetry_sample_run())

    # python3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(iothub_client_telemetry_sample_run())
    