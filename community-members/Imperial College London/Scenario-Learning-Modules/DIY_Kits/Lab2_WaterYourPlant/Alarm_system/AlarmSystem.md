# **2. Set up an alarm system**

## Start with a email account

1. Register a new microsoft email account

![Image](media/newemail.png)

2. Check for information about **Outlook mail SMTP**

- SMTP server name: smtp.office365.com
- SMTP Port TLS: 587

![Image](media/SMTP.png)

## Write the code

This is the full code in python to send an email using the `smtplib` and `MIMEText` modules. There is a breakdown of the code in the next section.

```python
import smtplib
from email.mime.text import MIMEText
# import libraries for SMTP and email related functions

import smbus2, bme280, os, asyncio, json
from dotenv import load_dotenv
from grove.grove_moisture_sensor import GroveMoistureSensor, GroveLightSensor
from grove.grove_led import GroveLed
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse

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

    # set up the email credentials
    from_email_addr = 'sender_email@outlook.com'
    from_email_password = 'sender_email_password'
    to_email_addr = 'receiver_email@outlook.com'
    # set email message
    body = 'Farmbeats Alert: Your plants are thirsty!!'
    msg = MIMEText(body)
    # set sender and recipient
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = 'FARMBEATS ALERT!!!'

    
    # listen for commands
    async def command_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request('needs_watering')
            needs_watering = method_request.payload
            print('Needs watering:', needs_watering)
            payload = {'result': True}

            if needs_watering:
                # Uncomment this if you are using the grove LED module
                # led.on()

                # Uncomment this if you are using a normal LED
                # GPIO.output(led_pin, GPIO.HIGH)

                server = smtplib.SMTP('smtp.outlook.com', 587)
                # connect to server and get ready to send email
                # edit above lines with your email provider's SMTP server details
                server.starttls()
                # comment out this line if provider does not use TLS
                server.login(from_email_addr, from_email_password)
                server.sendmail(from_email_addr, to_email_addr, msg.as_string())
                server.quit()
                print('Email sent')         

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
The monitor email account will send alarm directly to receiver as it reaches the water threshold.

### Breakdown the code

During this section, only the new parts of the code will be explained. If you have any questions from any of the sections not explained below, please refer to [Lab 1 - Send data to IoT Central](../Lab1_MonitorYourPlan/IoTCentral/Send_data_to_IoTCentral.md).

```python
    # set up the email credentials
    from_email_addr = 'sender_email@outlook.com'
    from_email_password = 'sender_email_password'
    to_email_addr = 'receiver_email@outlook.com'
    # set email message
    body = 'Farmbeats Alert: Your plants are thirsty!!'
    msg = MIMEText(body)
    # set sender and recipient
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = 'FARMBEATS ALERT!!!'
```
Here you set up the credentials for email sender and receiver. Editting alarm message and its subject title in **body** and **msg[subject]** respectively.

```python
    async def command_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request('needs_watering')
            needs_watering = method_request.payload
            print('Needs watering:', needs_watering)
            payload = {'result': True}

            if needs_watering:
                server = smtplib.SMTP('smtp.outlook.com', 587)
                # connect to server and get ready to send email
                # edit above lines with your email provider's SMTP server details
                server.starttls()
                # comment out this line if provider does not use TLS
                server.login(from_email_addr, from_email_password)
                server.sendmail(from_email_addr, to_email_addr, msg.as_string())
                server.quit()
                print('Email sent')        

            method_response = MethodResponse.create_from_method_request(
                method_request, 200, payload
            )
            await device_client.send_method_response(method_response)
```
In this part of the code, the function waits for `needs_watering` command from IoT Central. Recall that `needs_watering` was set to be a boolean in IoT Central. If the command received is `True`, the raspberry pi will send an email with an alarm message as defined in the code. 

```python
listeners = asyncio.gather(command_listener(device_client))

await main_loop()

# Cancel listening
listeners.cancel()

# Finally, disconnect
await device_client.disconnect()
```

This code starts the command listener and the main loop. Once the main loop exits, the command listener is cancelled and the device disconnects.

------------------

Next Step: [Implement an autoirrigation system](../Automated_irrigation)
