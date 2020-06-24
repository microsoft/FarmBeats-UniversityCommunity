import requests, json, msal

# Your service principal App ID
CLIENT_ID = "<Enter Client ID>"
# Your service principal password
CLIENT_SECRET = "<Enter Client Secret>"
# Tenant ID for your Azure subscription
TENANT_ID = "<Enter Tenant ID>"

AUTHORITY_HOST = 'https://login.microsoftonline.com'
AUTHORITY = AUTHORITY_HOST + '/' + TENANT_ID

ENDPOINT = "https://<FARMBEATS NAME>-api.azurewebsites.net"
SCOPE = ENDPOINT + "/.default"

context = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
token_response = context.acquire_token_for_client(SCOPE)
# We should get an access token here
access_token = token_response.get('access_token')

headers = {
    "accept": "application/json",
    "Authorization": "Bearer " + access_token,
    "Content-Type" : "application/json"
    }

messagejson = {
    "type": "Analog",
    "manufacturer": "Grove",
    "productCode": "BME280",
    "sensorMeasures": [
        {
            "name": "grove temperature",
            "dataType": "Double",
            "type": "AmbientTemperature",
            "unit": "Fahrenheit",
            "aggregationType": "None",
            "depth": 0,
            "description": "grove ambient temperature"
        },
        {
            "name": "grove humidity",
            "dataType": "Double",
            "type": "RelativeHumidity",
            "unit": "Percentage",
            "aggregationType": "Average",
            "depth": 0,
            "description": "grove relative humidity"
        },
        {
            "name": "grove barometer",
            "dataType": "Double",
            "type": "Pressure",
            "unit": "Percentage",
            "aggregationType": "Average",
            "depth": 0,
            "description": "grove barometric pressure"
        }
    ],
    "name": "BME280",
    "description": "Grove - Temp & Humi & Barometer Sensor",
    "properties": {}
}

messagejson = json.dumps(messagejson)
# print((messagejson))

response = requests.post(url=''.join([ENDPOINT,'/SensorModel']), data = messagejson, headers=headers)
print(response)
