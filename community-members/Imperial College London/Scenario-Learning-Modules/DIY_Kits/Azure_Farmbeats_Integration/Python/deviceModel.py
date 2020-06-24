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
    "Authorization": ' '.join(["Bearer", access_token]),
    "Content-Type" : "application/json"
    }

messagejson = {
  "type": "Node",
  "manufacturer": "AWARE",
  "productCode": "IndoorM1",
  "ports": [
    {
      "name": "BusinessKit",
      "type": "Analog"
    }
  ],
  "name": "BusinessKit",
  "description": "Raspberry Pi with Light, Soil Moisture, Air Temperature, Humidity, and Barometric Pressure sensors",
  "properties": {
    "Light": {},
    "Soil Moisture": {},
    "Air Temperature": {},
    "Humidity": {},
    "Barometric Pressure": {}
  }
}

messagejson = json.dumps(messagejson)

response = requests.post(url=''.join([ENDPOINT, '/DeviceModel']), data = messagejson, headers=headers)
print(response)

# To see the response uncomment the next line
# print(response.text)
