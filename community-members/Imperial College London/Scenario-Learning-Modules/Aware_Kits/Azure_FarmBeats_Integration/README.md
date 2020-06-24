# Azure FarmBeats

## FarmBeats Components

The FarmBeats application has 2 components, the Datahub and the Accelerator.

The **FarmBeats Datahub** is an API layer used to aggregate, normalize, and contextualize agriculture data sets (from sensors, drones, satellites, etc.) in the context of a farm.

The **FarmBeats accelerator**    is a user interface application built on top of the API layer.  Farmers can use this to create and view maps of their farm and apply AI and machine learning to the data collected in the Datahub.

The unique value of FarmBeats for the intended end user, the farmer, is in this data aggregation.  Previously farmers might have access to separate sets of data, for example data coming from their tractor, sensors in their fields, and weather data.  FarmBeats lets them pull together data from lots of different sources, apply AI and machine learning models against it, and receive actionable insights about their farm.

Most farmers do not have the background to create their own machine learning models.  They rely on researchers, agronomists, or agriculture companies to provide those models for them.  FarmBeats is the platform that allows that work to happen.  Data stored in the FarmBeats Datahub can be used in the existing accelerator, or in accelerators designed by agriculture industry professionals and researchers.

## FarmBeats Business Kits

A FarmBeats Business Kit has been developed by a third party for precision agriculture education.  The Business Kits use Internet of Things (IoT) technology to collect agriculture data.  The kit includes preconfigured Microsoft Azure cloud services, and a Raspberry Pi with soil moisture, light, ambient temperature, and humidity sensors.  The data collected in the kit is displayed in an Azure IoT Central dashboard.

If you have created and deployed a FarmBeats Business Kit it is possible to move the data you have collected into Azure FarmBeats.  This document will explain the steps, providing an example of how you can move data collected from a 3rd party into Azure FarmBeats.  By doing that, the data can be combined with other data about your farm and used for analysis in FarmBeats and other accelerators.

### Prerequisites

- FarmBeats Public Preview has been successfully installed.

- FarmBeats Business Kit is running and has collected data.

### Required values

As you work through the instructions, some values will be needed to move to other steps.  Make a note of the following fields:

|Field Name | Value|
|-----------|--------|
|Your Datahub API endpoint (e.g. https://\<FarmBeats Name>-api.azurewebsites.net)| |
|Your Azure Tenant ID (Can be found at Azure Active Directory > Overview) | |
|Client ID (Presented in the **Create a Telemetry Client** section) | |
|Client Secret (Presented in the **Create a Telemetry Client** section) | |
|EventHub Connection String (Presented in the **Create a Telemetry Client** section) | |
|Device Model ID# (Presented in **Business Kit Metadata** section) | |MAC Address for your raspberry pi | |
|FarmBeats Farm ID# (Use a **Get** command from your Swagger API Interface) | |
|Device ID# (Presented in **Business Kit Metadata** section) | |
|Sensor Model ID#s for each Sensor Type (Presented in **Business Kit Metadata** section) | |

## Steps

1. [Basic Python Tutorial](./Basic_Python.md)

1. [Create Telemetry Client](./Create_telemetry_client.md)

1. [Create Metadata](./Create_metadata.md)

1. [Send Historical Data](./Send_historical_data.md)

1. [Send data from IoT Central](./Send_data_IoTCentral.md)
