import json
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_icd_data', methods=['POST'])
def get_icd_data():
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

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

        url = "https://id.who.int/icd/entity/257068234"
        url = "http://id.who.int/icd/release/11/2023-01/mms/660711115"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "API-Version": "v2",
            "Accept-Language": "en"
        }

        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    else:
        return jsonify({"error": response.text})

if __name__ == '__main__':
    app.run(debug=True)
