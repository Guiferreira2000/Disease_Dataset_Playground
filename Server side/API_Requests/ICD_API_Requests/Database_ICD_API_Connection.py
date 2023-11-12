import requests
import json
import re
import openpyxl

# https://id.who.int/swagger/index.html

# Versions of the ICD 11 code (release id)
# https://icd.who.int/icdapi/docs2/SupportedClassifications/

### 1º Part - search_disease_url function


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
        "highlightingEnabled": True,
        "medicalCodingMode": True, # Linearlinization # This mode is the default and it should be used when searching the classification for medical coding purposes. In this mode, the search gives results from the entities that have a code. In this mode, the system will search all index terms of an entity. i.e. titles, synonyms, fully specified term, all terms of other entities that are in the foundation and aggregated into this entity
    }

    response = requests.get(search_url, headers=headers, params=params)

    if response.status_code == 200:
        search_results = response.json()
        #print(search_results)
        response_data = json.loads(response.text)
        # print(json.dumps(response_data, indent=2))
        # Replace special characters and spaces with an underscore
        safe_disease_name = re.sub('[^0-9a-zA-Z]+', '_', disease_name)
        with open(f'/home/guilherme/Documents/MDCompass Documentation/json files/search_results_{safe_disease_name}.json', 'w') as f:
            json.dump(response_data, f, indent=2)

        if "destinationEntities" in search_results:
            if search_results["destinationEntities"]:
                print("Status: Found results!")
                search_request = True
                print(search_request)
                for result in search_results["destinationEntities"]:
                    if "title" in result and result["title"].lower() == disease_name.lower():
                        return result["id"]
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

    return None, search_request


### 2º Part - Call parameters for the function


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

    # disease_name = "Abscess of the pharynx"  # Replace this with the disease name you want to search
    linearization_name = "mms"  # Replace with the desired linearization name
    release_id = "2023-01"  # Replace with the desired release ID
    # disease_url = search_disease_url(disease_name, access_token, linearization_name, release_id)
    # search_boolean = disease_url[1]

else:
    print("Error:", response.text)




##### 3º Part - Past the disease code to the excell book

# # Open the Excel file
# workbook = openpyxl.load_workbook('/home/guilherme/Documents/MDCompass/API_Requests/ICD_API_Requests/dd_Alphabetically_Sorted_Symptoms.xlsx')

# # Select the worksheet
# worksheet = workbook['Symptoms']


# for cell in worksheet['A2:A613']:
#     disease_name = cell[0].value

#     # Call the search_disease_url function
#     disease_url, search_boolean = search_disease_url(disease_name, access_token, linearization_name, release_id)

#     if search_boolean:
#         # Extract the ICD-11 code from the JSON data
#         safe_disease_name = re.sub('[^0-9a-zA-Z]+', '_', disease_name)
#         with open(f'/home/guilherme/Documents/MDCompass Documentation/json files/search_results_{safe_disease_name}.json', 'r') as f:
#             data = json.load(f)
        
#         destination_entities = data['destinationEntities']
#         if destination_entities:
#             first_entity = destination_entities[0]
#             the_code = first_entity.get('theCode')
#             definition = None
#             for matching_pv in first_entity['matchingPVs']:
#                 if matching_pv['propertyId'] == 'Definition':
#                     definition = matching_pv['label']
#                     definition = re.sub('<[^<]+?>', '', definition)
#                     break

#             print(f"ICD-11 code for '{disease_name}': {the_code}")
#             # Write the ICD-11 code to the corresponding cell in column B
#             cell[0].offset(column=6).value = the_code
#     else:
#         print(f"No results found for '{disease_name}'.")
        
# # Save the modified Excel file
# workbook.save('/home/guilherme/Documents/MDCompass/API_Requests/ICD_API_Requests/ss_Alphabetically_Sorted_Symptoms.xlsx')
