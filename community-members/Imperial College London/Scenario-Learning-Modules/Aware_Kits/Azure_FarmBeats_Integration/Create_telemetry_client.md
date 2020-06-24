# Create a Telemetry Client

After creating the metadata in Azure FarmBeats you must create a client that has access to your Azure FarmBeats installation.  The data from your FarmBeats Business Kit must be sent to Azure Event Hubs for processing.  Azure Event Hubs is a service that enables telemetry ingestion from connected devices and applications.

This step creates a device partner and provides you with information that will be needed in later steps.

1. Download this ![zip file](https://aka.ms/farmbeatspartnerscriptv2) and extract it to a local drive on your computer.

    The zip file contains one PowerShell file: `generatePartnerCredentials.ps1`

1. Sign in to your ![Azure Portal](https://portal.azure.com/)

    Navigate to Azure Active Directory > App Registrations

1. Select the App Registration that was created as part of your FarmBeats deployment.

1. Select Expose an API > Select Add a client application.
    - Enter

        `04b07795-8ddb-461a-bbee-02f9e1bf7b46`

    - Check Authorize scope.

    This will give access to the Azure Cloud Shell to perform the following steps.

1. Open Cloud Shell by clicking the icon on the toolbar in the upper ritheght corner of the portal.

    ![open cloudshell](./media/cloud_shell.png)

1. Set the environment to PowerShell.

    ![powershell](./media/powershell.png)

1. Upload the *generatePartnerCredentials.ps1* file.

    ![upload file](./media/upload_doc.png)
1. Enter the following command in the PowerShell.

    ```powershell
    Connect-AzureAD
    ```

    **Connect-AzureAD** cmdlet connects an authenticated account to use for Azure Active Directory., this command connects the current PowerShell session to the Azure Active Directory tenant.

1. Go to Azure Directory > Overview page to find the Tenant ID.

1. Run the **generatePartnerCredentials.ps1** with the following command:

    ```powershell
    ./generatePartnerCredentials.ps1
    ```

1. Enter the information as prompted.

    i. Your Datahub API Endpoint: [https://\<FarmBeats Name>-api.azurewebsites.net]

    ii. Your tenant ID.

    iii. For `type of partner` enter 1 for sensor.

    iv. For `Partner name` enter AWARE to indicate the manufacturer of the business kit.

1. If prompted for sign in, open a browser to the page: [https://microsoft.com/devicelogin] and enter the code provided on the screen.

1. You will receive an acknowledgement that you have signed into the Microsoft Azure Cross-platform Command Line Interface application on your device.  Close the browser window and return to the Power Shell window.

1. In your Power Shell window, you should see a message that you have successfully created the app registration.  The Partner Integration credentials should be listed below the message. Make a note of them as you will need them in the next step.

------------
Go to next step: [Create Metadata](./Create_metadata.md)
