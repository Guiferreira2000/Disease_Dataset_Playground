import pandas as pd
import json

# Load the Excel file
df = pd.read_excel('Datasets/mdcompass_assistent_files/Labeled_Diseases_Dataset_29_09_2023.xlsx')

# Since the file path is not provided, I'm using the sample data from the user's message
# The actual implementation should read the Excel file as shown above.

# Filter out the relevant columns (disease and symptoms)
disease_and_symptoms = df.filter(regex='^(Disease|Symptom_)')

# Set the 'Disease' column as the index to facilitate the creation of the JSON structure
disease_and_symptoms.set_index('Disease', inplace=True)

# Remove all NaN values and convert each row into a list
diseases_json = disease_and_symptoms.apply(lambda x: [symptom for symptom in x if pd.notnull(symptom)], axis=1).to_dict()

# Write to a JSON file
with open('Datasets/mdcompass_assistent_files/symptoms_per_diseases.json', 'w') as json_file:
    json.dump(diseases_json, json_file, indent=4)
