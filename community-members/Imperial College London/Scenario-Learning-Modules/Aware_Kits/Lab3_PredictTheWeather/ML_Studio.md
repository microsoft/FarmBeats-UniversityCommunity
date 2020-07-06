# Azure Machine Learning Studio

In this tutorial you will use the new version of Azure Machine Learning Studio and build and train a machine learning model yourself with a provided weather dataset.

## Create an Azure Machine Learning workspace

To use Azure Machine Learning, you create a workspace in your Azure subscription. You can then use this workspace to manage data, compute resources, code, models, and other artifacts related to your machine learning workloads.

1. Sign into the [Azure portal](https://portal.azure.com/#home)

1. Select **＋Create a resource**, search for Machine Learning, and create a new **Machine Learning** resource with the following settings:

    1. **Workspace Name**: A unique name of your choice such as `ML-workspace-Ata`

    1. **Subscription**: Your Azure subscription

    1. **Resource group**: Create a new resource group with a unique name suc as `FarmBeats-ML-Ata`

    1. **Location**: Choose any available location

    1. **Workspace edition**: Enterprise

    <img src="media/ML_workspace_create.png" width="70%">

1. Wait for your workspace to be created (it can take a few minutes). Then go to it in the portal.

1. On the Overview page for your workspace, launch Azure Machine Learning Studio (or open a new browser tab and navigate to https://ml.azure.com ), and sign into Azure Machine Learning studio using your Microsoft account.

1. In Azure Machine Learning studio, you can use the pages under ☰ icon to manage the resources in your workspace.

## Create compute resources

To train and deploy models using Azure Machine Learning designer, you need compute resources on which to run the training process, test the model, and host the model in a deployed service.

### Create compute targets

Compute targets are cloud-based resources on which you can run model training and data exploration processes. In Azure Machine Learning studio, view the **Compute** page (under **Manage**). This is where you manage the compute targets for your data science activities. There are four kinds of compute resource you can create:

1. **Compute Instances**: Development workstations that data scientists use to work with data and models. On the Compute Instances tab, add a new compute instance with the following settings. You'll use this to test your model:

    1. Compute name: enter a unique name

    1. Virtual Machine type: CPU

    1. Virtual Machine size: Standard_DS2_v2
  
1. **Compute Clusters**: Scalable clusters of virtual machines for on-demand processing of experiment code. While the compute instance is being created, switch to the Compute Clusters tab and add a new compute cluster with the following settings. You'll use this to train a machine learning model:

    1. Compute name: enter a unique name

    1. Virtual Machine size: Standard_DS2_v2

    1. Virtual Machine priority: Dedicated

    1. Minimum number of nodes: 2

    1. Maximum number of nodes: 2

    1. Idle seconds before scale down: 120
  
1. **Inference Clusters**: Deployment targets for predictive services that use your trained models.
  
    1. **Compute name**: enter a unique name

    1. **Kubernetes Service**: Create new

    1. **Region**: Select a different region than the one used for your workspace

    1. **Virtual Machine size**: Standard_DS2_v2 (Use the filter to find this in the list)

    1. **Cluster purpose**: Dev-test

    1. **Number of nodes**: 2

    1. **Network configuration**: Basic
 
    1. **Enable SSL configuration**: Unselected  

1. **Attached Compute**: Links to existing Azure compute resources, such as Virtual Machines or Azure Databricks clusters. You don't have to attach a new compute for now.

The compute targets will take some time to be created. You can move onto the next unit while you wait.

> In a production environment, you'd typically set the **minimum number of nodes** value to 0 so that compute is only started when it is needed. However, compute can take a while to start, so to reduce the amount of time you spend waiting for it, you've initialized it with two permanently running nodes for this module.
  
## Explore data

To train a model, you need a dataset that includes historical features (characteristics of the entity for which you want to make a prediction) and known label values (the numeric value that you want to train a model to predict).

### Create a pipeline

To use the Azure Machine Learning designer, you create a pipeline that you will use to train a machine learning model. This pipeline starts with the dataset from which you want to train the model.

1. In Azure Machine Learning studio , view the **Designer** page (under **Author**), and select **+** to create a new pipeline.

1. In the **Settings** pane, change the draft pipeline name (**Pipeline-Created-on-date**) to **Chance of Rain Training** (if the Settings pane is not visible, select the ⚙ icon next to the pipeline name at the top).

1. Observe that you need to specify a compute target on which to run the pipeline. In the **Settings** pane, use **Select compute target** to select the compute cluster you created previously.

#### Add and explore the dataset and create the pipeline

Azure Machine Learning includes a sample dataset that you can use to predict the chance of rain.

1. On the left side of the designer, select the **Datasets** (⌕) tab, and drag the **Weather Dataset** from the **Samples** section onto the canvas.

1. Drag a **Select Columns in Dataset** module to the canvas, below the **Weather Dataset** module. Then connect the output at the bottom of the **Weather Dataset** module to the input at the top of the **Select Columns in Dataset** module.

1. Select the **Select Columns in Dataset module**, and in its **Settings** pane on the right, select **Edit column**. Then in the **Select columns** window, select **By name** and use the **+** links to add **WeatherType, DryBulbCelsius, RelativeHumidity**

1. Drag an **Edit MetaData** module and set its settings as this:

    <img src="media/editMetadata_settings.png" width="40%">

1. Drag a **Clean Missing Data** module and set its settings as this:

    <img src="media/CleanMissingData_settings.png" width="40%">

1. Drag an **Execute R Script** module and set its code as this:

    ```R
    # R version: 3.5.1
    # The script MUST contain a function named azureml_main
    # which is the entry point for this module.

    # Please note that functions dependant on X11 library
    # such as "View" are not supported because X11 library
    # is not pre-installed.

    # The entry point function MUST have two input arguments.
    # If the input port is not connected, the corresponding
    # dataframe argument will be null.
    #   Param<dataframe1>: a R DataFrame
    #   Param<dataframe2>: a R DataFrame
    azureml_main <- function(dataframe1, dataframe2){
    print("R script run.")

    # If a zip file is connected to the third input port, it is
    # unzipped under "./Script Bundle". This directory is added
    # to sys.path.

    # Return datasets as a Named List
    return(list(dataset1=dataframe1, dataset2=dataframe2))
    }
    ```

1. Drag another **Execute R Script** module and set its code as this:

    ```R
    # R version: 3.5.1
    # The script MUST contain a function named azureml_main
    # which is the entry point for this module.

    # Please note that functions dependant on X11 library
    # such as "View" are not supported because X11 library
    # is not pre-installed.

    # The entry point function MUST have two input arguments.
    # If the input port is not connected, the corresponding
    # dataframe argument will be null.
    #   Param<dataframe1>: a R DataFrame
    #   Param<dataframe2>: a R DataFrame
    azureml_main <- function(dataframe1, dataframe2){
      print("R script run.")

    # If a zip file is connected to the third input port, it is
    # unzipped under "./Script Bundle". This directory is added
    # to sys.path.

    dataframe1$isRain[grepl("RA", dataframe1$isRain)] <- "Yes"
    dataframe1$isRain[grepl("SN", dataframe1$isRain)] <- "Yes"
    dataframe1$isRain[grepl("DZ", dataframe1$isRain)] <- "Yes"
    dataframe1$isRain[grepl("PL", dataframe1$isRain)] <- "Yes"
    dataframe1$isRain[dataframe1$isRain != "Yes"] <- "NO"

    # Return datasets as a Named List
    return(list(dataset1=dataframe1, dataset2=dataframe2))
    }
    ```
    
1. Drag a **Split Data** module and set its settings as this:

    <img src="media/SplitData_settings.png" width="40%">
    
1. Make the connections between modules according to the picture below.    
    
    <img src="media/pipeline_structure_1.png" width="40%">
    
1. After splitting the dataset drag a **Train Model** and set the **Label Column** as **isRain**.

1. Then drag a **Two-Class Logistic Regression** module and set its settings as this:

    <img src="media/Logistic_Regression_settings.png" width="40%">

1. Drag a **Select Columns in Dataset** module. Select **edit columns** and add **temperature** and **humidity**.

1. Make the following connections:

    <img src="media/pipeline_2.png" width="40%">
    
1. Finally add a **Score Model** module. Connect the output of **Train Model** to the left input and connect the output of **Select Columns in Dataset** to the right input of **Score Model**. Your pipeline should look like this:

    <img src="media/pipeline_3.png" width="40%">

### Submit the pipeline

1. Press **Create Inference pipeline** and select **Real-time inference pipeline**.

1. Wait for the inference pipeline to be created and select **Submit**.

### Deploy a predictive service

After you've created an inference pipeline for real-time inferencing, you can publish it as a service for client applications to use.

1. View the **Real-time inference pipeline** you created in the previous unit.

1. At the top right, select **Deploy**, and set up a new real-time endpoint named predict-weather on the inference cluster you created previously.
    
1. Wait for the web service to be deployed - this can take several minutes. The deployment status is shown at the top left of the designer interface.

### Test the real-time endpoint

After deployment finishes, you can test your real-time endpoint by going to the Endpoints page.

1. On the **Endpoints** page, select the endpoint you deployed.

1. Select **Test**.

1. Test your model by changing the values for DryBulbCelsius, RelativeHumidity. These are the temperature and humidity readings obtained from your Raspberry Pi. The rest of the values can remain unchanged. Then select **Test**.

### Get REST endpoint and the Primary Key

You need the following to connect to your deployed service from a client application.

1. On the **Endpoints** page, select the endpoint you deployed.

1. When the endpoint opens, view the **Consume** tab and note the following information there. 

    1. The REST endpoint for your service
    1. The Primary Key for your service

## Challenge

Using the REST endpoint and the Primary Key you have noted, integrate your machine learning model to your IoT Central application as you did for the Azure maps section. Feel free to try out and expand this to try predict other than the probability of rainfall.

-------------------------

Try out [Machine Learning Studio (Classic)](ML_Studio_Classic.md) or [Check what you learned!](Knowledge_Check.md)
