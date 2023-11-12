import requests
import json

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

    search_term = "Cholera"  # Replace 'Cholera' with the desired disease name
    url = f"https://id.who.int/icd/entity/search?q={search_term}"

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
