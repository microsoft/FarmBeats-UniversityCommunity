# Azure Services
## Azure Event Hubs. (This just gets the data)
Allows us to take streaming data and connect it to other services, such as storing the data or using Azure Stream Analytics to analyse the data in real time. Real-time data ingestion service is simple, trusted and scalable. Data ingested have to be in json format. (Use “json.dumps()” method in python to convert to json).

## Azure Blob Storage. (Store the data)
Allows us to store blobs (objects) of unstructured data that can be easily access from other Azure Services. Azure Storage can also store files, tables and queues.

## Azure Stream Analytics. 
Provides real-time analytics on streams of data, allowing us to stream data from one service to another. We will use it to pass the data from Azure Event Hubs (stream input) to Azure Blob storage (stream output). For this, we will need to create a new query, and start the job from the overview menu.

Check data is being stored in the Blob storage by going into the “Storage Explorer (preview)”, select the container, and download the json file.

## Azure Functions.
Event driven serverless compute platform. A way to define small blocks of code that are triggered by events such as a web request, data changes in storage or event being put onto an Azure Event Hub.

Azure Stream Analytics can call Azure Functions in response to streaming data, either individual messages or and aggregation across a time window. (i.e. if moisture is lower than a threshold, then the plant needs watering).
