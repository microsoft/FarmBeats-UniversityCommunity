# Microsoft FarmBeats Student Kit

Developed by:

* Lulwa AlKhalifa

* Raj Jain

* Ata Yardimci

* Jie Yechen

* Jingwei Wu

We would like to thank Dr. Christos Bouganis, Reader in Intelligent Systems in the Department of Electrical and Electronic Engineering at Imperial College London, for his invaluable support and continued engagement during the project. We would also like to thank our Industrial Supervisors from Microsoft, Mr. Lee Stott, Mr. Jim Bennett and Ms. Stacey Wood, for their valuable insights and suggestions for our project along with regular meetings. We would also like to express our sincere gratitude towards them for giving us a great opportunity to present our work on the the FarmBeats learning resource to the Microsoft FarmBeats Engineering Team based in Redmond, Washington, U.S.

## About Microsoft FarmBeats

It is a venture of Microsoft Research currently in its public preview. Launched in 2015, by Dr. Ranveer Chandra, it aims to democratize Artificial Intelligence and Internet of Things technologies to farmers globally.

These technologies usually comprise low-cost sensors, drones, vision, white space and Machine Learning algorithms. Together these can be used to tackle very little or no power and internet in farms which are some common problems faced in the rural areas.

### FarmBeats Student Kit

To promote the concept of FarmBeats among universities, Microsoft has collaborated with educational institutions and universities around the world. This involves teaching IoT concepts with Azure Cloud Services to students.

Hence, the FarmBeats student kit includes a Raspberry Pi as a microcontroller with preconfigured Microsoft Azure Cloud services with the following sensors:

- [Temperature, Humidity and Pressure Sensor (BME280)](https://wiki.seeedstudio.com/Grove-Barometer_Sensor-BME280/)

- [Light sensor](https://wiki.seeedstudio.com/Grove-Light_Sensor/)

- [Capacitive Soil Moisture Sensor](https://wiki.seeedstudio.com/Grove-Capacitive_Moisture_Sensor-Corrosion-Resistant/)

This GitHub repository is a one-stop-shop resource to learn about state-of-the-art digital agriculture and precision farming techniques. The user will learn how to build complex IoT products using Raspberry Pi and Microsoft Azure Cloud Computing Services. No prior experience is required.

### Lesson Plan

This github repo includes instructions for both: Aware kits and DIY kits. Even if you do not have a Raspberry Pi, you can find some python scripts with simulated data for each of the scenarios. This way, you will be able to learn more about Azure Services and IoT by using just a computer.

#### Scenario 1: Monitor your plant

This is a simple experiment to begin collecting data from all the sensors. Learn how to set up the hardware and interact with azure services. 
You will be learn to create an application in IoT Central and PowerApps to display your sensor data. 

##### IoT Central

![Azure services iotc](Aware_Kits/Lab1_MonitorYourPlant/IoTCentral/media/AzureServices_iotc.png)

##### PowerApps

![Azure services powerapps](Aware_Kits/Lab1_MonitorYourPlant/PowerApps/media/AzureServices_powerapps.png)

#### Scenario 2: Water your plant

The main goal for this scenario is to learn how to implement an automated irrigation system. This will allow you to have a better understanding of how to efficiently use water, as there are a lot of contries facing water scarcity.

![AzureServiceS1](Aware_Kits/Lab2_WaterYourPlant/Alarm_system/media/AzureServices_Scenario2.png)

#### Scenario 3: Predict the weather

In scenario 3, you will try to predict the probability of rainfall using Azure Machine Learning. You will be using the data stored in the Azure Storage Account, which is gathered using your own Raspberry Pi. You can extend this and try to predict other metheorological events.

![Ml Diagram](Aware_Kits/Lab3_PredictTheWeather/media/ML-Diagram.png)

#### Scenario 4: LED Light System

Light is another important factor affecting plant growth. In this scenario, you will learn how to build a LED Light System to optimize plant growth. In addition, you can understand how light different wavelenghts affect your plant and try to use this to improve the plant growth.

Wavelenght composition of sunlight

![sunlight composition](Aware_Kits/Lab4_LEDLightSystem/media/sunlight.png)
