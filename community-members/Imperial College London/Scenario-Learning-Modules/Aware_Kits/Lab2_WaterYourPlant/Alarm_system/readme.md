# Set Up a Notification System

Learn how to set up a notification system to alert the user when the plant being monitored needs to be watered. 

This lab covers how to add **Commands** to the device capabilities model in IoT Central and configure the **Rules** and **Actions** to send an email when the soil moisture is below a certain threshold. 

## Lab Structure

- Investigate creating rules using Azure IoT Central
  - Send email or push notification when the soil moisture is below a certain threshold.

  - Optional: check if temperature/pressure/light intensity is outside the optimal range.

  - Learn to use Azure Events Hub, Azure Stream Analytics and Azure Functions to process data.
  - Determine the date and time that the plant was last watered.

_Optionally a LED indicator can be integrated to indicate if the plant needs watering._

_Optional date and time last watered extension project_

------

## Steps

1. [Set up your hardware](Setup_hardware.md)

1. [Create a new device template for IoT Central App](Device_Template_IoTC.md)

1. [Create a rule in IoT Central](IoT_Central_create_rule.md)

1. [Create an Azure Function](Create_Azure_Function.md)

1. [Create a Stream Analytics Job](Create_stream_analytics.md)

1. [Execute IoT Command](Execute_IoT_Command.md)

1. [Write code for the alarm system](AlarmSystem.md) 

