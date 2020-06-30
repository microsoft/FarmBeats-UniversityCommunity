# Set Up a Notification System

Learn how to set up a notification system to alert the user when the plant being monitored needs to be watered. 

This lab covers how to add **Commands** to the device capabilities model in IoT Central and configure the **Rules** and **Actions** to send an email when the soil moisture is below a certain threshold. 

_Optionally a LED indicator can be integrated to indicate if the plant needs watering._

_Optional date and time last watered extension project._

## Lab Structure

- Investigate creating rules using Azure IoT Central
  - Send email or push notification when the soil moisture is below a certain threshold.

  - Optional: check if temperature/pressure/light intensity is outside the optimal range.

- Learn to use process sensor data using Azure Functions.
  - Stream data from IoT Central using Event Hubs and Stream Analytics



------

## Steps

1. [Set up your hardware](Setup_hardware.md)

1. [Create a new device template for IoT Central App](Device_Template_IoTC.md)

1. [Create a rule in IoT Central](IoT_Central_create_rule.md)

    Alternatively send email from raspberry pi.

1. [Write code for the alarm system](AlarmSystem.md) 
