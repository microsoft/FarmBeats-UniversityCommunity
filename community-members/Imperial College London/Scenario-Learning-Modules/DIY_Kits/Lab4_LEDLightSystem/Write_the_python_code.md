# Modify the Python Code to be able to receive commands

In the [previous step](Create_new_iotc_template.md), you have created a new template which includes commands to switch on and off the LEDs. In this step, you will modify the Python code from Lab 1 so that it can receive the commands from IoT Central.

> All the code can be found in the [Python](Python/) folder. 

## Full code

This is the full code in Python. Below is a break down explaining the functions used for listenning to commmands from IoT Central.

```python
from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
from azure.iot.device import MethodResponse, Message
import smbus2, bme280, os, asyncio, json, time
from grove.grove_moisture_sensor import GroveMoistureSensor
from dotenv import load_dotenv
from grove.grove_light_sensor_v1_2 import GroveLightSensor
import RPi.GPIO as GPIO
from threading import Thread

# Configuration parameters
bme_pin = 1
bme_address = 0x76
moisture_pin = 2
light_pin = 0

# Setting the pins used for controlling the LEDs in the raspberry pi
red_led_pin = 16 # pin 36
blue_led_pin = 26 # pin 37
violet_led_pin = 6 # pin 31

# Confiuration of the GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led_pin,GPIO.OUT)
GPIO.setup(blue_led_pin,GPIO.OUT)
GPIO.setup(violet_led_pin,GPIO.OUT)

red_light_time = None
blue_light_time = None
violet_light_time = None
red_light = False
blue_light = False
violet_light = False

# Create the sensors
bus = smbus2.SMBus(bme_pin)
calibration_params = bme280.load_calibration_params(bus, bme_address)

moisture_sensor = GroveMoistureSensor(moisture_pin)

light_sensor = GroveLightSensor(light_pin)

# Get the Connection data
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
    temp = round(getTemperaturePressureHumidity().temperature, 2)
    moisture = getMoisture()
    pressure = round(getTemperaturePressureHumidity().pressure, 2)
    humidity = round(getTemperaturePressureHumidity().humidity, 2)
    light = getLight()
    data = {
        "humidity": humidity,
        "pressure": pressure,
        "temperature": temp,
        "soil_moisture": moisture,
        "light_level": light
    }

    return json.dumps(data)

# Control function for the Red LEDs
def control_red(red_light_pin):
    start = time.perf_counter()
    print(f'Turn on red LED for {red_light_time} minutes')
    GPIO.output(red_light_pin, GPIO.HIGH)
    while red_light and start + 60*red_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*red_light_time:
            print(f'Turn off red LED')
            GPIO.output(red_light_pin, GPIO.LOW)
            break

# Control function for the Blue LEDs
def control_blue(blue_light_pin):
    start = time.perf_counter()
    print(f'Turn on blue LED for {blue_light_time} minutes')
    GPIO.output(blue_light_pin, GPIO.HIGH)
    while blue_light and start + 60*blue_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*blue_light_time:
            print(f'Turn off blue LED')
            GPIO.output(blue_light_pin, GPIO.LOW)
            break

# Control function for the Violet LEDs
def control_violet(violet_light_pin):    
    start = time.perf_counter()
    print(f'Turn on violet LED for {violet_light_time} minutes')
    GPIO.output(violet_light_pin, GPIO.HIGH)
    while violet_light and start + 60*violet_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*violet_light_time:
            print(f'Turn off violet LED')
            GPIO.output(violet_light_pin, GPIO.LOW)
            break

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

            await device_client.send_message(telemetry)
            
            print(telemetry)
            await asyncio.sleep(20)

    async def redLight(request):
        response = MethodResponse.create_from_method_request(
            request, status = 200# payload = {'description': f'Red Light for {request.payload} minutes'}
        )
        global red_light_time
        global red_light
        await device_client.send_method_response(response)  # send response
        red_light = False
        if request.payload == None or request.payload == 0:
            print('Turn off the Red LED')
        else:
            await asyncio.sleep(1)
            red_light = True
            red_light_time = request.payload
            red = Thread(target=control_red, args=(red_led_pin, ), daemon=True)
            red.start()

    async def blueLight(request):
        response = MethodResponse.create_from_method_request(
            request, status = 200# payload = {'description': f'Blue Light for {request.payload} minutes'}
        )
        global blue_light_time
        global blue_light
        await device_client.send_method_response(response)  # send response
        blue_light = False
        if request.payload == None or request.payload == 0:
            print('Turn off the Blue LED')
        else:
            await asyncio.sleep(1)
            blue_light = True
            blue_light_time = request.payload
            blue = Thread(target=control_blue, args=(blue_led_pin, ), daemon=True)
            blue.start()

    async def violetLight(request):
        response = MethodResponse.create_from_method_request(
            request, status = 200# payload = {'description': f'Violet Light for {request.payload} minutes'}
        )
        global violet_light_time
        global violet_light
        await device_client.send_method_response(response)  # send response
        violet_light = False
        if request.payload == None or request.payload == 0:
            print('Turn off the Violet LED')
        else:
            await asyncio.sleep(1)
            violet_light = True
            violet_light_time = request.payload
            violet = Thread(target=control_violet, args=(violet_led_pin, ), daemon=True)
            violet.start()


    commands = {
        'red_led': redLight,
        'blue_led': blueLight,
        'violet_led': violetLight,
    }

    # Define behavior for handling commands
    async def command_listener(device_client):
        print('command listener')
        while True:
            method_request = await device_client.receive_method_request()  # Wait for commands
            await commands[method_request.name](method_request)
   
    listeners = asyncio.gather(command_listener(device_client))

    await main_loop()

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

## Breakdown

During this section, only the new parts of the code will be explained. If you have any questions from any of the sections not explained below, please refer to [Lab 1 - Send data to IoT Central](../Lab1_MonitorYourPlan/IoTCentral/Send_data_to_IoTCentral.md).

```python
# Setting the pins used for controlling the LEDs in the raspberry pi
red_led_pin = 16 # pin 36
blue_led_pin = 26 # pin 37
violet_led_pin = 6 # pin 31

# Confiuration of the GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(red_led_pin,GPIO.OUT)
GPIO.setup(blue_led_pin,GPIO.OUT)
GPIO.setup(violet_led_pin,GPIO.OUT)

red_light_time = None
blue_light_time = None
violet_light_time = None
red_light = False
blue_light = False
violet_light = False
```

The first three lines just define the pins in the Raspberry Pi that the corresponding LEDs will be connected to. The following lines, define this pins as **outputs** to be able to turn on and off the LED lights. Finally, we define three variables to store the time we want the LED's to be on. These will be used in the a later step. The booleans will be used to exit the threads, explained later on.

```python
async def redLight(request):
    response = MethodResponse.create_from_method_request(
        request, status = 200# payload = {'description': f'Red Light for {request.payload} minutes'}
    )
    global red_light_time
    global red_light
    await device_client.send_method_response(response)  # send response
    red_light = False
    if request.payload == None or request.payload == 0:
        print('Turn off the Red LED')
    else:
        await asyncio.sleep(1)
        red_light = True
        red_light_time = request.payload
        red = Thread(target=control_red, args=(red_led_pin, ), daemon=True)
        red.start()

async def blueLight(request):
    response = MethodResponse.create_from_method_request(
        request, status = 200# payload = {'description': f'Blue Light for {request.payload} minutes'}
    )
    global blue_light_time
    global blue_light
    await device_client.send_method_response(response)  # send response
    blue_light = False
    if request.payload == None or request.payload == 0:
        print('Turn off the Blue LED')
    else:
        await asyncio.sleep(1)
        blue_light = True
        blue_light_time = request.payload
        blue = Thread(target=control_blue, args=(blue_led_pin, ), daemon=True)
        blue.start()

async def violetLight(request):
    response = MethodResponse.create_from_method_request(
        request, status = 200# payload = {'description': f'Violet Light for {request.payload} minutes'}
    )
    global violet_light_time
    global violet_light
    await device_client.send_method_response(response)  # send response
    violet_light = False
    if request.payload == None or request.payload == 0:
        print('Turn off the Violet LED')
    else:
        await asyncio.sleep(1)
        violet_light = True
        violet_light_time = request.payload
        violet = Thread(target=control_violet, args=(violet_led_pin, ), daemon=True)
        violet.start()
```

The `command_listener` function will be listenning to commands send from the Application in IoT Central. After a command is received, it is sent to the correspoding function to hadle it. For example, if a `red_led` commands is sent from IoT Central, the `command_listener` will call the function `redLight` and pass the request as a variable. This mapping of the command to the function is defined in the object `commands`, situated above the `command_listener` function.

As for the functions `redLight`,`blueLight` and `violetLight`, they send a response to tell IoT Central that it has received the command. After that, the `redLight` function, sets the global variables `red_light_time` and  `red_light` to be the time set by the user in IoT Central and an indication that a new command has arrived. Finally, a **thread** with the controller of the LED is started. A thread allows us to have multiple functions running in parallel. 

```python
# Control function for the Red LEDs
def control_red(red_light_pin):
    start = time.perf_counter()
    print(f'Turn on red LED for {red_light_time} minutes')
    GPIO.output(red_light_pin, GPIO.HIGH)
    while start + 60*red_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*red_light_time:
            print(f'Turn off red LED')
            GPIO.output(red_light_pin, GPIO.LOW)
            break

# Control function for the Blue LEDs
def control_blue(blue_light_pin):
    start = time.perf_counter()
    print(f'Turn on blue LED for {blue_light_time} minutes')
    GPIO.output(blue_light_pin, GPIO.HIGH)
    while start + 60*blue_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*blue_light_time:
            print(f'Turn off blue LED')
            GPIO.output(blue_light_pin, GPIO.LOW)
            break

# Control function for the Violet LEDs
def control_violet(violet_light_pin):    
    start = time.perf_counter()
    print(f'Turn on violet LED for {violet_light_time} minutes')
    GPIO.output(violet_light_pin, GPIO.HIGH)
    while start + 60*violet_light_time >= int(time.perf_counter()):
        if  time.perf_counter() >= start + 60*red_light_time:
            print(f'Turn off violet LED')
            GPIO.output(violet_light_pin, GPIO.LOW)
            break
```

These are the **threads** used. Each thread starts with storing the current time, to calculate the time elapsed in the **while** loop. The **time** module in python has a precision of 9 decimals more or less. Since we will be just looking at an integer, a **break** has been added to ensure the program exits the while loop after switching off the LEDs. Whenever a new command is received, the `red_light` is set to `False`, and the thread will exit. This will allow another thread to start.

The reason why we need to use threads in this case is because otherwise the whole `command_listener` function will be stuck inside the while look, until the timer is over. To make it clearer, imagine you have set the red LEDs for a whole hour. If you don't use threads, your program is not able to do anything during a whole hour, it is just waiting for the time to pass, and exit the while loop to be able to continue with its tasks.

By using different threads, the program is able to listen to new commands sent as well as wait for the time to pass and switch off the LEDs.

```python
    listeners = asyncio.gather(command_listener(device_client))

    await main_loop()

    listeners.cancel()
```

The `command_listener` function is initialize with the code above. Similarly, it stops listening to events with `listeners.cancel()`.

```python
if __name__ == '__main__':
    # python3.7 or newer
    asyncio.run(main())

    # python3.6
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
```

Finally, before running the `main` function, we need to initialize the threads. The function `control_red` takes one argument, which is passed using the `args`argument in the **Thread constructor**. Note that the thread **daemon** is set as `True`. This is just to terminate all the threads when exiting the main thread. Otherwise, after pressing `Ctrl + C`, the threads will be still running.

------------

Now you can control your LEDs from IoT Central. The [next step](Optional.md) is optional. You will try to implement and automatic system to switch on and off the LEDs depending on the sensor measurements.
