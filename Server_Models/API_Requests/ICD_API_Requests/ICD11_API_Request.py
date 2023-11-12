import requests
import json
# https://id.who.int/swagger/index.html
# In this example, you have included the access token you received from the token endpoint in the Authorization header of the GET request to the ICD-11 API endpoint for Cholera (entity ID 257068234).

### Now because of the local deployment on docker, we can access ICD-11 from the following url  http://localhost/icd instead of https://id.who.int/icd
# https://icd.who.int/icdapi/docs2/ICDAPI-DockerContainer/
 # - http://localhost/swagger/index.html
 # - http://localhost/ct11 
 # - http://localhost/browse11


url = "https://icdaccessmanagement.who.int/connect/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": "f4a39ebe-734c-4fb2-8b5d-ac36a670708f_0782aa93-3766-474c-aeb8-04b1e82f3f6f",
    "client_secret": "/0/VmvmGmdePAKyzO6gx52AhAkjw/KTAsrpkBKRe66I=",
    "scope": "icdapi_access"
}
response = requests.post(url, data=payload)
if response.status_code == 200:
    response_body = json.loads(response.text)
    access_token = response_body["access_token"]
    #print("Access token:", access_token)

    url = "https://id.who.int/icd/entity/257068234" # 257068234 identifica a doença. Neste caso, Colera
    #url = "https://id.who.int/icd/entity?q=diabetes" # Retrieves a list of codes that match a specific search term
    #url = "http://localhost/icd/entity/448895267" # Utilizar as keys "Parent" e "chield"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "API-Version": "v2",
        "Accept-Language": "en"
    }

    response = requests.get(url, headers=headers)
    print(response.text)
else:
    print("Error:", response.text)
