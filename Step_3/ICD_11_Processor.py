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
    
    # Remove duplicates from the symptoms list
    unique_symptoms = list(set(symptoms_list))
    
    # Update the JSON dictionary with the ICD 11 code and its symptoms
    json_dict[code] = {
        "Symptoms": unique_symptoms
    }
    
    # Append to the original JSON list
    for symptom in unique_symptoms:
        json_list.append({
            "ICD 11 Code": code,
            "Symptom": symptom
        })

# Save the JSON list structure to a file (original format)
with open("Datasets/step_3/icd_11_GPT_formated_data.json", "w") as f:
    json.dump(json_list, f, indent=4)

# Save the JSON dictionary structure to a file (new format)
with open("Datasets/step_3/icd_11_formated_data_dict.json", "w") as f:
    json.dump(json_dict, f, indent=4)

print("Processing complete!")
