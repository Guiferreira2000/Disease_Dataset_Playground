import pandas as pd
import requests
import json
import re

def search_disease_url(disease_name, access_token, linearization_name, release_id):
    search_request = False

    base_url = f"https://id.who.int/icd/release/{release_id}"
    #search_url = f"{base_url}/{linearization_name}/search"
    #search_url = "https://id.who.int/icd/entity/search" # /icd/entity/search
    search_url = f"https://id.who.int/icd/release/11/{release_id}/{linearization_name}/search" # /icd/release/11/{releaseId}/{linearizationname}/search



    headers = {
        "API-Version": "v2",
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
        "Accept-Language": "en",
    }

    params = {
        "q": disease_name,
        "subtreesFilter": "", # Optional parameter. Comma separated list of URIs. If provided, the search will be performed on the entities provided and their descendants
        "subtreeFilterUsesFoundationDescendants": False, # Linearlinization # When a subtree filter is used the search looks at the linearization descendants of the entities in the subtreefilter. If subtreeFilterUsesFoundationDescendants is set to true, the search looks at the foundation descendants of the entities in the subtreefilter
        "includeKeywordResult": False, # Linearlinization # Optional parameter. Default false. If set to true, the search result will also include keyword list - if the last word provided is incomplete, keyword list includes all words that start with the incomplete word (word completion mode) - if the last word is complete, the keyword list will provide suggested additional words that could be added to the search query.
        "chapterFilter": "", # Optional, comma or semicolon separated list of chapter codes eg:01;02;21 When provided, the search will be performed only on these chapters
        "useFlexisearch": False, # Flexible search
        "flatResults": True, # Default value false. If set to true the search result entities are provided in a nested data structure representing the ICD-11 hierarchy. Otherwise they are listed as flat list of matches
        "propertiesToBeSearched": "Title,FullySpecifiedName,Definition,Exclusion",
        "highlightingEnabled": True, # If true it changes the value of the search_boolean!!! # Optional. Default is true, if set to false the search result highlighting is turned off and the results don't contain special tags for highlighting where the results are found within the text
        "medicalCodingMode": True, # Linearlinization # This mode is the default and it should be used when searching the classification for medical coding purposes. In this mode, the search gives results from the entities that have a code. In this mode, the system will search all index terms of an entity. i.e. titles, synonyms, fully specified term, all terms of other entities that are in the foundation and aggregated into this entity
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        search_results = response.json()
        #print(search_results)
        response_data = json.loads(response.text)
        # print(json.dumps(response_data, indent=2))
        with open(f'Datasets/step_2/json_files/search_results_{disease_name}.json', 'w') as f:
            json.dump(response_data, f, indent=2)

        if "destinationEntities" in search_results:
            if search_results["destinationEntities"]:
                print("Status: Found results!")
                search_request = True
                for result in search_results["destinationEntities"]:
                    if "title" in result and result["title"].lower() == disease_name.lower():
                        return result["id"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return None, search_request

# Read the output_symptoms.xlsx file into pandas DataFrame
df_output = pd.read_excel("Datasets/step_2/output_symptoms_updated.xlsx")

# Fetch the access_token
url = "https://icdaccessmanagement.who.int/connect/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": "f4a39ebe-734c-4fb2-8b5d-ac36a670708f_0782aa93-3766-474c-aeb8-04b1e82f3f6f",
    "client_secret": "/0/VmvmGmdePAKyzO6gx52AhAkjw/KTAsrpkBKRe66I=",
    "scope": "icdapi_access"
}
response = requests.post(url, data=payload)
response_body = json.loads(response.text)
access_token = response_body["access_token"]

linearization_name = "mms"  # Replace with the desired linearization name if different
release_id = "2023-01"  # Replace with the desired release ID if different

# Loop through each row of the DataFrame
for index, row in df_output.iterrows():
    symptom = row["Symptom"]
    icd_code = row["ICD 11"]
    
    # If ICD code is not present
    if pd.isnull(icd_code):
        disease_url = search_disease_url(symptom, access_token, linearization_name, release_id)
        # If disease_url found and search request successful
        if disease_url:
            with open(f'Datasets/step_2/json_files/search_results_{symptom}.json') as f:
                data = json.load(f)
            
            destination_entities = data['destinationEntities']
            if destination_entities:
                first_entity = destination_entities[0]
                the_code = first_entity.get('theCode')
                
                # Update the DataFrame with the fetched ICD code
                df_output.at[index, "ICD 11"] = the_code

                # Print the new ICD code found
                print(f"Symptom: {symptom}, ICD Code: {the_code}")

# Save the DataFrame back to output_symptoms.xlsx
df_output.to_excel("Datasets/step_2/symptoms_updated_ICD.xlsx", index=False)
