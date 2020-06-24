# Write the code to capture telemetry from the Raspberry Pi

In the [previous step](Create_IoTHub.md) you created the IoT Hub to be able to receive and send events. In this step, you will write the code for the Raspberry Pi and connect to the IoT Hub. If you don't have a raspberry pi, there is another script with simulated data provided in this tutorial.

> You can find the code for this section under the [Python Folder](Python)

## Connect to the Raspberry Pi from Visual Studio Code

To write the code for the Raspberry Pi, you will use the Remote development capabilities of Visual Studio Code.

### Install the Remote Development extension in Visual Studio Code

To enable remote development in Visual Studio Code, you will need to install the [Remote Development Extension pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack&WT.mc_id=agrohack-github-jabenn).

1. Launch Visual Studio Code

1. Select the Extensions tab from the left hand menu, or select *View > Extensions*

   ![The extensions tab in Visual Studio Code](./media/vscode_extension.png)

1. Search for `remote ssh` and install the *Remote - SSH* extension pack from Microsoft by selecting the **Install** button

   ![The remote ssh extension](./media/install_remote_ssh.png)

### Connect to the Raspberry Pi

1. From Visual Studio Code, launch the c/ommand palette

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

   ![The password entry dialog](media/enter_password.png)

> Once the connection has been established, the next time *Remote-SSH: Connect to Host* is selected a new window will be opened and the password requested, there will be no need to configure it again.

## Configure Python

The code for this device will be written in Python 3, which comes by default in the latest Raspbian releases. Before code can be written, the environment needs to be configured and some packages installed.

### Configure Visual Studio Code for Python development

Visual Studio Code can install extensions on the host device. The Python extension is needed to work with Python files.

1. Select the Extensions tab from the left hand menu, or select *View > Extensions*

1. Search for `Python` and install the *Python* extension from Microsoft by selecting **Install in SSH: raspberrypi.local**.

   ![The python extension](./media/install_python.png)

   > There are a number of Python extensions available, so ensure you install the one from Microsoft

1. A reload will be required, so select **Reload required**

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

1. Locate the new `EnvironmentMonitor` folder and select it, then select **OK**

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

   ![The terminal activating the virtual environment](media/activated_environment.png)

### Install the required python packages

Python has a package manager called `pip` that allows you to install code from other developers in packages called pip packages. You can read more about pip and see the available packages at [pypi.org](https://pypi.org). Packages can either be installed into the virtual environment one at a time using the `pip` command, or multiple packages can be listed in a file called `requirements.txt` and installed together. The advantage of using a `requirements.txt` file is that this can be checked into source code control, so that other developers can configure their environment the same way by installing the same packages from this file.

1. Create a new file inside the `EnvironmentMonitor` folder called `requirements.txt`

1. Add the following to this file

   ```sh
   azure-iot-device
   python-dotenv
   RPi.bme280
   grove.py
   smbus2
   asyncio
   ```

1. Save the file. If you don't want to have to remember to always save files in Visual Studio Code, select *File > Auto Save* to turn on automatic saving of files.

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

1. Create a new file inside the `EnvironmentMonitor` folder called `.env`

1. Add the following entries to this file:

   ```sh
   CONNECTION_STRING=<Connection String>
   ```

   Set `<Connection>` to be the value of the connection string from the device inside the IoT hub.

### Create the application code

1. Open the `app.py` file

1. Add the following code to the file:

    ```python
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
    ```

   This code connects to Azure IoT Central, and every 30 seconds will poll for data from the sensors and send it as a telemetry message. Feel free to change this.

1. Save the file

1. From the terminal, run the following command to start the app

   ```sh
   python app.py
   ```

   The app should start, connect to Azure IoT Hub, and send data. The data being sent will be printed to the terminal

   ![The app running showing telemetry in the terminal](media/terminal_data.png)

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
connectionString = os.getenv('CONNECTION_STRING')
```

This code loads the environment variables from the `.env` file, and gets the values into some fields.

```python
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
```

The `getTemperaturePressureHumidity` function reads values from the BME280 sensor. The `getMoisture` function reads data from the soil moisture sensor. The `getLight` function read data from the light sensor. Note that for the moisture and light sensors, we  their values are rounded to two decimal places. For the BME280, this is done in the `gettemeletryData` function as it has to be rounded separately for temperature, pressure, and humidity. The `getDate` function simply returns the current date and time, as will bbe used to the display graphs in PowerApps. The `getTelemetryData` function calls these four functions to get the sensor values, date and time, then formats them into a JSON document, ready to send to Azure IoT Hub.

```python
def iothub_client_init():
   client = IoTHubDeviceClient.create_from_connection_string(connectionString)
   return client
```

The `iothub_client_init` function will establish a connection with IoT Hub and return a **client**. We will be able to send data to the Hub via this client.

```python
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
```

The main function of this script is `iothub_client_telemetry_sample_run`. First, it will try to create the client object. If it is successful, it will then enter an infinity `while` loop to send the data. It first calls the `getTelemetryData` function to get the json with all the data. Then the client sends the message. Note that this process is **asynchronous**, which means we need an `await` to make sure the client has finished sending the message. After that, the raspberry pi will do nothing for **30 seconds**. There is an exception when `KeyboardInterrupt`. This will close the client when we stop the script using `Ctrl + C`.

```python
if __name__ == '__main__':
   print("IoT Hub Connection")
   # python3.7
   # asyncio.run(iothub_client_telemetry_sample_run())

   # python3.6
   loop = asyncio.get_event_loop()
   loop.run_until_complete(iothub_client_telemetry_sample_run())
```

The last part of the code will is just to tell the Raspberry Pi it should run the `iothub_client_telemetry_sample_run` function when running the script.

***Note: You should uncomment the code, depending on the python version you are using.***

## Check that the connection has been established

1. Open the IoT Hub in your portal.

1. In the **OverView** tab, scroll to the bottom. You should be able to

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

1. After a few seconds, the Raspberry Pi will reboot and resume sending telemetry to Azure IoT Hub. Check the device view to see the data.

----------------
[Next Step](Create_storage_account.md): Create the storage account to store the data received from the sensors.
