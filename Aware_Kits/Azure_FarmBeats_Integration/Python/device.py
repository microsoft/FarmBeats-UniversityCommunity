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
  "deviceModelId": "<DEVICE MODEL>",
  "hardwareId": "<MAC ADDRESS>",
  "reportingInterval": 300,
  "location": {
    "latitude": 0,
    "longitude": 0,
    "elevation": 0
  },
  "parentDeviceId": "",
  "name": "FB Business Kit",
  "description": "FB Business Kit",
  "properties": {
    "additionalProp1": {},
    "additionalProp2": {},
    "additionalProp3": {}
  }
}

messagejson = json.dumps(messagejson)

response = requests.post(url=''.join([ENDPOINT, '/Device']), data=messagejson, headers=headers)
print(response)

# To see the response uncomment the next line
# print(response.text)
