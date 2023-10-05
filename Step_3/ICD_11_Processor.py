import pandas as pd
import json

# Load the dataset
df = pd.read_excel("Datasets/step_2/symptoms_updated_ICD.xlsx")

# Extract unique ICD 11 codes and sort them
unique_icd_codes = sorted(df['ICD 11'].unique())

# Create JSON structures for both files
json_list = []
json_dict = {}

for code in unique_icd_codes:
    # Filter rows with the current ICD 11 code and create a copy
    filtered_df = df[df['ICD 11'] == code].copy()
    
    # Consolidate the terms into "Similar terms"
    filtered_df.loc[:, 'Similar terms'] = filtered_df[['Suggested changes', 'Medical term 1', 'Medical term 2', 'Medical term 3', 'Medical term 4']].apply(lambda x: x.dropna().tolist(), axis=1)
    
    # Create a list of all symptoms and similar terms
    symptoms_list = filtered_df['Symptom'].tolist() + [term for sublist in filtered_df['Similar terms'].tolist() for term in sublist]
    
    # Handle ICD codes that have "/"
    split_codes = [icd.strip() for icd in code.split('/')]  # Remove potential whitespace
    
    # Update the JSON list for the icd_11_GPT_formated_data.json
    for individual_code in split_codes:
        for symptom in symptoms_list:
            json_list.append({
                "icd_11_code": individual_code,
                "symptom": symptom.strip()  # Remove trailing spaces
            })
            
    # Update the dictionary for the icd_11_formated_data.json
    for individual_code in split_codes:
        if individual_code not in json_dict:
            json_dict[individual_code] = []
        json_dict[individual_code].extend(symptoms_list)

# Ensure unique symptoms for each ICD in the dictionary (for icd_11_formated_data.json)
for key, value in json_dict.items():
    json_dict[key] = list(set([v.strip() for v in value]))  # Remove trailing spaces and ensure uniqueness

# Remove duplicates from json_list
json_list = [{"icd_11_code": item["icd_11_code"], "symptom": item["symptom"].strip()} for item in json_list]  # Ensure there's no trailing space
seen = set()
json_list = [x for x in json_list if tuple(x.items()) not in seen and not seen.add(tuple(x.items()))]

# Save the JSON list structure to a file (for icd_11_GPT_formated_data.json)
with open("Datasets/step_3/icd_11_GPT_formated_data_v2.json", "w") as f:  # Changed the file name to match the requirement
    json.dump(json_list, f, indent=4)

# Save the JSON dictionary structure to a file (for icd_11_formated_data.json)
with open("Datasets/step_3/icd_11_formated_data.json", "w") as f:
    json.dump(json_dict, f, indent=4)

print("Processing complete!")
