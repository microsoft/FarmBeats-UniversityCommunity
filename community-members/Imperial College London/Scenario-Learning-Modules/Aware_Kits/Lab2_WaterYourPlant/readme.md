# **Scenario 2: Self-irrigation**

## **Description**

The main goal for this scenario is to learn how to implement an automated irrigation system.
The scenario it self is divided into three different parts:

- [Set up an alarm system.](#1-set-up-an-alarm-system)

- [Automated irrigation.](#2-automated-irrigation)

- [Azure Maps for weather prediction.](#3-azure-maps-for-weather-prediction)

## **Breakdown of the scenario**

### **1. Set up an alarm system**

#### **Objective**

Set up a system to alert the user when the plant needs to be watered.

#### **Learning outcomes**

- Investigate creating rules using Azure IoT Central
  - Send email or push notification when the soil moisture is below a certain threshold.

  - Optional: check if temperature/pressure/light intensity is outside the optimal range.

- Learn to use Azure Events Hub, Azure Stream Analytics and Azure Functions to process data.
  - Determine the date and time that the plant was last watered.

#### **Key areas to teach**

IoT Azure Services, Data, Microcontroller Programming, AI.

_Optionally a LED indicator can be integrated to indicate if the plant needs watering._

### **2. Automated irrigation**

#### Objective

To set up a simple automated irrigation system.

_**Additional equipment:** Relay module, water pump._

#### Learning Outcomes

- Practical application of previous knowledge that links to digital farming.

  - Option 1: Setup the water pump with existing device
  
  - Option 2: Register a separate device to control the water pump.

### 3. Azure Maps for weather prediction

#### Objective

Use Azure Maps to determine whether irrgation is needed depending on weather conditions.

#### Learning Outcomes

- Learn to interface with other Azure Services.

- Become confortable with more complex data processing.

### **Azure Services Integration**

![AzureServiceS1](Alarm_system/media/AzureServices_Scenario2.png)

--------------
