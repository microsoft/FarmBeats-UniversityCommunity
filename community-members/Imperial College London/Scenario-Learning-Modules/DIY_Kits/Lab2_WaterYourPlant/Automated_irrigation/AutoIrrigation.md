# Automated irrigation

In the previous step, you have sent an email with a notification either from [IoT Central rule](../Alarm_system/IoT_Central_create_rule.md) or [your Raspberry Pi](../Alarm_system/AlarmSystem.md). In this step, you will modify the code to implement a water pump to water the plant.

## Connection details

1. Remember to change the connection details for the device you have just created in IoT Central.

   ```sh
   ID_SCOPE=<Id scope>
   DEVICE_ID=raspberry_pi
   PRIMARY_KEY=<primary key>
   ```

   Set `<Id scope>` to be the value of the ID Scope from the **Connect** dialog in Azure IoT Central. Set `<primary key>` to be the **Primary key** value from this dialog.

## Modify the Python Code

1. Create a new file.

1. Add the following code to the file:

```python
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
```

If you want to use a LED to indicate if the plant needs to be watered, uncomment the code according to the LED you are using.

### Breakdown of the code

During this section, only the new parts of the code will be explained. If you have any questions from any of the sections not explained below, please refer to [Lab 1 - Send data to IoT Central](../Lab1_MonitorYourPlan/IoTCentral/Send_data_to_IoTCentral.md).

```python
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
```

This code defines the configuration for the sensors, including what pins they are connected to. It then creates objects for the BME280 temperature, pressure and humidity sensor, including loading calibration details from the sensor, the moisture sensor and the light sensor. Aditionally, you can uncomment the code to switch on and off a LED light.

```python
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
```

This code defines the `command_listener` function to listen to commands from Azure IoT Central, It continuously polls for a command by waiting for method requests - commands are implemented as methods on the device that are called. If a command is called, the payload is retrieved to see if the plant needs watering. Depending on the value of this, the LED is turned on or off and drive the water pump to do auto-irrigation. Finally a response is sent with an HTTP success code of 200 to say the command was handled.

```python
listeners = asyncio.gather(command_listener(device_client))

await main_loop()

# Cancel listening
listeners.cancel()

# Finally, disconnect
await device_client.disconnect()
```

This code starts the command listener and the main loop. Once the main loop exits, the command listener is cancelled and the device disconnects.

### Verify the data in Azure IoT Central

1. Open the app in Azure IoT Central
1. From the **Devices** tab, select the `Raspberry Pi` device
1. The view will load, and there should be data visible that matches the data being sent
1. Select the **Needs Watering** command. It will open as a new tab next to the view.
1. Try checking and unchecking the *Needs watering* value and selecting **Run**. The LED should light when *Needs watering* is checked, and turn off when it is unchecked. The motor in water pump will also run and stop while checking.

## Run the Python app continuously

The Python app will only run as long as the terminal is connected. Ideally we want the software running as soon as the Raspberry Pi boots up. This saves having to log in and run the Python file each time the device is turned on. The easiest way to do this is via a `cron` job that is run on reboot. Cron is a task scheduler that runs commands at specific times.

1. Stop the Python app by pressing ctrl+c in the terminal

1. From the terminal run the following command to edit the crontab. This is a file that contains jobs for cron to run.

    ```sh
    sudo crontab -e
    ```

    If you are asked to select and editor, select `nano`. This will open the file inside the terminal in the nano editor.

1. Add the following line to the end of the file:

    ```sh
    @reboot /home/pi/EnvironmentMonitor/.venv/bin/python3 /home/pi/EnvironmentMonitor/app.py
    ```

1. Press ctrl+x to close nano. Press Y to save the file when asked if you want to save the modified buffer, then press return to select the default file name.

1. From the terminal, run the following command to restart the Raspberry Pi

   ```sh
   sudo reboot
   ```

1. Close the Visual Studio Code window

1. After a few seconds, the Raspberry Pi will reboot and resume sending telemetry to Azure IoT central. Check the device view to see the data.

--------------

Next Step: [Create an Azure Function](Create_Azure_function.md)
