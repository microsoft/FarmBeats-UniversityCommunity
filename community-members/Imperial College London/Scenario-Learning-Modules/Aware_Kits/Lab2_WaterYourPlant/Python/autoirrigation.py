import smbus2, bme280, os, asyncio, json
from dotenv import load_dotenv
from grove.grove_moisture_sensor import GroveMoistureSensor, GroveLightSensor
from grove.grove_led import GroveLed
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse

# Raspberry pi control
import RPi.GPIO as GPIO
import time

# Configuration parameters
bme_pin = 1
bme_address = 0x76
moisture_pin = 2
led_pin = 16
light_pin = 0

MOTOR_PIN = 17      
GPIO.setmode(GPIO.BCM)
# Set moisture input pin to be an output
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Create the sensors
bus = smbus2.SMBus(bme_pin)
calibration_params = bme280.load_calibration_params(bus, bme_address)

moisture_sensor = GroveMoistureSensor(moisture_pin)

light_sensor = GroveLightSensor(light_pin)

# Create the LED
# # Uncomment this if you are using the grove LED module
# led = GroveLed(led_pin)

# # Uncomment this if you are using a normal LED
# GPIO.setup(led_pin, GPIO.OUT)

# Load the Azure IoT Central connection parameters
load_dotenv()
id_scope = os.getenv('ID_SCOPE')
device_id = os.getenv('DEVICE_ID')
primary_key = os.getenv('PRIMARY_KEY')

def getTemperaturePressureHumidity():
    return bme280.sample(bus, bme_address, calibration_params)

def getMoisture():
    return round(moisture_sensor.moisture, 2)

def getLight():
    return round(light_sensor.light, 2)/10

def getTelemetryData():
    temp = round(getTemperaturePressureHumidity().temperature, 2) # degrees Celsius
    moisture = getMoisture() # voltage in mV
    pressure = round(getTemperaturePressureHumidity().pressure, 2)/1000 # kPa
    humidity = round(getTemperaturePressureHumidity().humidity, 2) # % relative Humidity
    light = getLight() # % Light Strenght
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

    # listen for commands
    async def command_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request('needs_watering')
            needs_watering = method_request.payload
            print('Needs watering:', needs_watering)
            payload = {'result': True}

            if needs_watering:
                # # Uncomment this if you are using the grove LED module
                # led.on()

                # # Uncomment this if you are using a normal LED
                # GPIO.output(led_pin, GPIO.HIGH)

                GPIO.output(MOTOR_PIN, GPIO.HIGH)
                asyncio.sleep(10) # water plant for 10 seconds
                GPIO.output(MOTOR_PIN, GPIO.LOW)


                # # Uncomment the code below for using the Raspberry Pi to send the Email
                # server = smtplib.SMTP('smtp.outlook.com', 587)
                # # connect to server and get ready to send email
                # # edit above lines with your email provider's SMTP server details
                # server.starttls()
                # # comment out this line if provider does not use TLS
                # server.login(from_email_addr, from_email_password)
                # server.sendmail(from_email_addr, to_email_addr, msg.as_string())
                # server.quit()
                # print('Email sent')        


            else:
                # # Uncomment this if you are using the grove LED module
                # led.off()

                # # Uncomment this if you are using a normal LED
                # GPIO.output(led_pin, GPIO.LOW)
                pass

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
    # python3.7 or newer
    asyncio.run(main())

    # python3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())