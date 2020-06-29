# Set up your hardware

Before starting with this set of labs, you will need to verify that you have the required hardware setup as described in this lab sheet.

## Preparation

- Complete the steps to [assemble your hardware](../../Lab0_SetUp/1b_Assemble_your_FarmBeats_Student_Kit_Hardware.md) as covered in Lab 0

- Verify that the Capacitive Soil Moisture Sensor is plugged into socket A2 of the Grove Base Hat

- Verify that the Temperature, Humidity and Barometer Sensor (BME280) is plugged into the bottom left I2C socket of the Grove Base Hat.

![finished assembly](media/HardwareSetup.png)

## Optional LED Setup - Grove LED Module

For this lab, you have the option to set up an LED to light up when your soil moisture is below the optimal level for your plant.

If you wish to do this, you will need the [Grove - Red LED](https://wiki.seeedstudio.com/Grove-Red_LED/) module. You are able to connect the Red LED to any GPIO Port on the Grove base.

![Grove Red LED](media/GroveLEDRed.jpg)

## Optional LED Setup - LED Component

Alternatively, you can use a standard LED component, a breadboard, a 330Ohm resistor, and some jumper breadboard wires. The parts you will need are listed below:

![LED component](media/led.jpg)

LED Module

![breadboard](media/breadboard.jpg)

Breadboard

A solderless breadboard is a construction base for prototyping of electronics. You will need this to connect all your components together.

![male female wires](media/mf_wires.jpg)

Male to Female Jumper Wires. You will need at least two of these.

![male female wires](media/resistor.jpg)

A resistor (220 Ohms - 1 kOhm)

You always need a resistor when connecting an LED to a Raspberry Pi GPIO (General Purpose Input Output) port. This is necessary to limit current and avoid blowing your LED.



![circuit diagram](media/led_diagram.png)

 - Please arrange your components as per the circuit diagram above. You may use any of the [GPIO ports](https://pinout.xyz/#) on your Raspberry Pi for this, but make sure that this is reflected in the code.

## Additional Notes

You will not need a light sensor for this scenario. You may disconnect it from your sensor device, if you wish.


------------------

Next step: [Create a new device template for IoT Central App](Device_Template_IoTC.md)
