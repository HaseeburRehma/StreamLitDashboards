import webbrowser
import requests
import msal
from msal import PublicClientApplication

APPLICATION_ID = "2a024f2c-e5ea-450e-92f0-b87eab712b98"
CLIENT_SECRET = ""

authority_url = "https://login.microsoftonline.com/consumers/"

base_url = "https://graph.microsoft.com/v1.0"
endpoint = base_url, 'me'

SCOPES = ['User.Read', 'User.Export.All']

#method 1 : authorization with auth code 
client_instance = msal.ConfidentialClientApplication(
    client_id= APPLICATION_ID,
    client_credential= CLIENT_SECRET,
    authority = authority_url
)

authorization_request_url = client_instance.get_authorization_request_url(SCOPES)
webbrowser.open(authorization_request_url, new=True)

authorization_code = "M.C520_SN1.2.U.24bbe1d2-5f45-b65d-2c7c-6ef8203112ab"

access_token = client_instance.acquire_token_by_authorization_code(
    code=authorization_code,
    scopes=SCOPES
)
print(access_token)
access_token_id = access_token['access_token']
headers = { 'Authorization': 'Bearer' + access_token_id}

endpoint = base_url + 'me'
response = requests.get(endpoint, headers=headers)
print(response)
print(response.json())


