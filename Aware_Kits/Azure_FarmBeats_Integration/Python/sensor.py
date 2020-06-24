import requests, json
import msal

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
  "hardwareId": "BME280",
  "sensorModelId": "<SENSOR MODEL>",
  "location": {
    "latitude": 0,
    "longitude": 0,
    "elevation": 0
  },
  "depth": 0,
  "port": {
    "name": "BusinessKit",
    "type": "Analog"
  },
  "deviceId": "<DEVICE ID>",
  "name": "pressure",
  "description": "Grove - Temp & Hum & Bar sensors",
  "properties": {
      "Pressure": {},
      "Humidity": {},
      "Temperature": {}
  }
}

messagejson = json.dumps(messagejson)

response = requests.post(ENDPOINT + '/Sensor', data = messagejson, headers=headers)
print(response)
