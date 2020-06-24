# Write the code to capture telemetry from the Raspberry Pi

In the [previous step](Create_app_IoTCentral.md) you created the IoT Central Application to be able to receive and send events. In this step, you will write the code for the Raspberry Pi and connect to the IoT Cental App. If you don't have a raspberry pi, there is another script with simulated data provided in this tutorial.

> You can find the code for this section under the [Python Folder](Python)

## Connect to the Raspberry Pi from Visual Studio Code

To write the code for the Raspberry Pi, you will use the Remote development capabilities of Visual Studio Code.

### Install the Remote Development extension in Visual Studio Code

To enable remote development in Visual Studio Code, you will need to install the [Remote Development Extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack&WT.mc_id=agrohack-github-jabenn).

1. Launch Visual Studio Code

1. Select the Extensions tab from the left hand menu, or select *View -> Extensions*

   ![The extensions tab in Visual Studio Code](./media/vscode_extension.png)

1. Search for `remote ssh` and install the *Remote - SSH* extension pack from Microsoft by selecting the **Install** button

   ![The remote development extension](./media/install_remote_ssh.png)

### Connect to the Raspberry Pi

1. From Visual Studio Code, launch the command palette

   * On macOS, press command+shift+p
   * On Windows or Linux, press ctrl+shift+p

1. Search for `Remote-SSH: Connect to Host` and select it

   ![The connect to host option](./media/connect_to_host.png)

1. Select *+ Add new SSH Host*

   ![The add new host option](./media/add_new_host.png)

1. Enter `pi@raspberrypi.local` or if you know the ip address of the pi `pi@yourIPAddress` as the SSH connection command

   ![The SSH connection command](./media/enter_ssh_host.png)

1. Select the SSH configuration file to update. This will store the SSH connection details to make connection easier. There will be an option in your home folder, which will vary depending on your OS and user name, so select this.

1. Once the connection has been configured, a dialog will appear saying the host is configured. Select **Connect** from this dialog.

   ![The host added dialog](./media/host_added.png)

1. A new Visual Studio Code window will open to host the connection. In the password prompt dialog, enter the password for your Raspberry Pi. The default password is `raspberry`.

> Once the connection has been established, the next time *Remote-SSH: Connect to Host* is selected a new window will be opened and the password requested, there will be no need to configure it again.

## Configure Python

The code for this device will be written in Python 3, which comes by default in the latest Raspbian releases. Before code can be written, the environment needs to be configured and some packages installed.

### Configure Visual Studio Code for Python development

Visual Studio Code can install extensions on the host device. The Python extension is needed to work with Python files.

1. Select the Extensions tab from the left hand menu, or select *View > Extensions*

1. Search for `Python` and install the *Python* extension from Microsoft by selecting **Install in SSH: raspberrypi.local**.

   ![The python extension](./media/install_python.png)

   > There are a number of Python extensions available, so ensure you install the one from Microsoft

1. A reload will be required, so select **Reload required**.

   ![Reload required for the python extension](./media/python_reload.png)

1. Visual Studio will reload the window, and you will be asked for your Raspberry Pi password again, so enter it.

### Create a folder for the code

1. When the new Visual Studio Code window is opened, the terminal should be opened by default. If not, open a new terminal by selecting *Terminal > New Terminal*.

1. From the Terminal in Visual Studio Code, create a new folder in the home folder called `EnvironmentMonitorIoT`

   ```sh
   mkdir EnvironmentMonitorIoT
   ```

1. Open this new folder in Visual Studio Code by selecting **Open folder** from the *Explorer*

   ![The open folder option](./media/open_folder.png)

1. Locate the new `EnvironmentMonitorIoT` folder and select it, then select **OK**

1. The window will reload in the selected folder, and you will be asked for your Raspberry Pi password again, so enter it.

### Configure a virtual environment

Python comes in various versions, and Python apps can use external code in packages installed via a tool called `pip`. This can lead to problems if different apps need different package versions, or different Python versions. To make it easier to avoid issues with package or Python versions, it is best practice to use *virtual environments*, self-contained folder trees that contain a Python installation for a particular version of Python, plus a number of additional packages.

1. When the new Visual Studio Code window is opened, the terminal should be opened by default. If not, open a new terminal by selecting *Terminal -> New Terminal*.

1. Ensure that the Python 3 virtual environment tooling is installed by running the following commands in the terminal

   ```sh
   sudo apt-get update
   sudo apt-get install python3-venv
   ```

1. Create a new file inside the `EnvironmentMonitor` folder called `app.py`. This is the file that will contain the code for the device, and by creating it the Python extension in Visual Studio Code will be activated. Select the **New File** button in the *Explorer*.

   ![The new file button](./media/new_file.png)

1. Name the new file `app.py` and press return

1. Create a new virtual environment called `.venv` using Python 3 by running the following command in the terminal

   ```sh
   python3 -m venv .venv
   ```

1. A dialog will pop up asking if you want to activate this virtual environment. Select **Yes**.

1. The existing terminal will not have the virtual environment activated. Close it by selecting the trash can button

   ![The kill terminal button](./media/kill_terminal.png)

1. Create a new terminal by selecting *Terminal -> New Terminal*. The terminal will load the virtual environment

   ![The terminal activating the virtual environment](./media/activate_venv.png)

### Install the required python packages

Python has a package manager called `pip` that allows you to install code from other developers in packages called pip packages. You can read more about pip and see the available packages at [pypi.org](https://pypi.org). Packages can either be installed into the virtual environment one at a time using the `pip` command, or multiple packages can be listed in a file called `requirements.txt` and installed together. The advantage of using a `requirements.txt` file is that this can be checked into source code control, so that other developers can configure their environment the same way by installing the same packages from this file.

1. Create a new file inside the `EnvironmentMonitorIoT` folder called `requirements.txt`

1. Add the following to this file

   ```sh
   azure-iot-device
   python-dotenv
   RPi.bme280
   grove.py
   smbus2
   ```

1. Save the file. If you don't want to have to remember to always save files in Visual Studio Code, select *File -> Auto Save* to turn on automatic saving of files.

1. From the terminal, run the following command to install these packages:

   ```sh
   pip install -r requirements.txt
   ```

The packages installed are:

| Package          | Description                                                                         |
| ---------------- | ----------------------------------------------------------------------------------- |
| azure-iot-device | Allows communication with Azure IoT services including Visual Studio Code           |
| python-dotenv    | Allows loading of environment variables from `.env` files                           |
| RPi.bme280       | Provides access to the BME280 temperature/pressure/humidity sensor                  |
| grove.py         | Provides access to the grove sensors including the Grove capacitive moisture sensor and the Light sensor |

## Write the code

### Define some environment variables

The connection details for the device ideally should not be stored in source code. They should be saved on the device and loaded as required. This is to avoid checking these details into source code control or sharing them publicly accidentally.

Python has a concept of `.env` files to store secrets such as connection details. These files are managed by the `python-dotenv` pip package, and are usually ignored when checking into git (the default `.gitignore` file created by GitHub for Python projects has these files in it by default).

1. Create a new file inside the `EnvironmentMonitorIoT` folder called `.env`

1. Add the following entries to this file:

   ```sh
   ID_SCOPE=<Id scope>
   DEVICE_ID=raspberry_pi
   PRIMARY_KEY=<primary key>
   ```

   Set `<Id scope>` to be the value of the ID Scope from the Connect dialog in Azure IoT Central. Set `<primary key>` to be the Primary key value from this dialog.

### Create the application code

1. Open the `app.py` file

1. Add the following code to the file:

    ```python
    from azure.iot.device.aio import IoTHubDeviceClient, ProvisioningDeviceClient
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
        # python3.7
        asyncio.run(main())

        # python3.6
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
    ```

   This code connects to Azure IoT Central, and every 60 seconds will poll for data from the sensors and send it as a telemetry message.

1. Save the file

1. From the terminal, run the following command to start the app

   ```sh
   python app.py
   ```

   The app should start, connect to Azure IoT Hub, and send data. The data being sent will be printed to the terminal

   ![The app running showing telemetry in the terminal](./media/terminal_data.png)

### Breakdown of the code

This Python file contains a lot of code to connect to the sensors, connect to Azure IoT Central, receive commands and send telemetry

```python
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
```

This code defines the configuration for the sensors, including what pins they are connected to. It then creates objects for the BME280 temperature, pressure and humidity sensor, including loading calibration details from the sensor, the moisture sensor and the light sensor.

```python
# Load the Azure IoT Central connection parameters
load_dotenv()
id_scope = os.getenv('ID_SCOPE')
device_id = os.getenv('DEVICE_ID')
primary_key = os.getenv('PRIMARY_KEY')
```

This code loads the environment variables from the `.env` file, and gets the values into some fields.

```python
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
```

The `getTemperaturePressureHumidity` function reads values from the BME280 sensor. The `getMoisture` function reads data from the soil moisture sensor. The `getLight` function read data from the light sensor. Note that for the moisture and light sensors,  their values are rounded to two decimal places. For the BME280, this in done the `getTemeletryData` function as it has to be rounded separately for temperature, pressure, and humidity. The `getTelemetryData` function calls these three functions to get the sensor values and formats them into a JSON document, ready to send to Azure IoT Central.

```python
async def main():
    ...

if __name__ == '__main__':
    # python3.7
    # asyncio.run(main())

    # python3.6
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

This code sets up an asynchronous `main` function using the Python `asyncio` library.

```python
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
```

This code defined an async function to register the device with Azure IoT central using the device provisioning service. This function is then called and the results of the registration are retrieved to get the connection details for the Azure IoT Central instance.

```python
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
```

This code takes the connection details, uses it to build a connection string, and creates an Azure IoT Hub device client. Azure IoT Hub is the underlying technology that provides the communication with Azure IoT Central. The device client then connects.

```python
# async loop that sends the telemetry
async def main_loop():
    while True:
        telemetry = getTelemetryData()
        print(telemetry)

        await device_client.send_message(telemetry)
        await asyncio.sleep(60)
```

This code defines a main loop that will run continuously. Each loop will get the telemetry values, then send them to Azure IoT Central. Finally the loop sleeps for 60 seconds.

```python
if __name__ == '__main__':
    # python3.7 or newer
    # asyncio.run(main())

    # python3.6
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

The last part of the code will is just to tell the Raspberry Pi it should run the `main` function when running the script.

***Note: You should uncomment the code, depending on the python version you are using.***

## Check that the connection has been established

1. Open the app in Azure IoT Central

1. From the **Devices** tab, select the `Raspberry Pi` device

1. The view will load, and there should be data visible that matches the data being sent

## Run the Python app continuously

*This step is optional.*

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

----------------
[Next Step](Create_event_hubs.md): Create Event Hubs to receive and send events.
