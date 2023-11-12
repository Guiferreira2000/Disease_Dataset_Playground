import openai
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your existing Excel file
excel_path = "/home/guilherme/Documents/Tese/Documentation/Dataset_teste/Disease_Dataset_02_08_2023.xlsx"

# Read the existing Excel file
df = pd.read_excel(excel_path)

# Function to get symptoms from the model
def get_symptoms(icd_code, disease_name, existing_symptoms):
    prompt = f"ICD Code: {icd_code}\nDisease: {disease_name}\nSymptoms: {existing_symptoms}\nPlease add new symptoms that weren't considered. The new symptoms must be in the same format as the existing ones. The symptoms must have between 1 to 3 words. Dont mention risk factors. Only symptoms in their medical term"
    response = openai.Completion.create(
        model="davinci:ft-fcul-2023-08-05-15-27-19",
        prompt=prompt,
        max_tokens=5
    )
    symptoms = response.choices[0].text.strip()
    return symptoms

# JSON file to store diseases with less than 10 symptoms
diseases_with_few_symptoms = []

# Iterate through the DataFrame and update or add data
for index, row in df.loc[1:309].iterrows():
    icd_code = row['ICD 11']
    disease_name = row['Disease']
    print (f"Disease: {disease_name}")
    existing_symptoms = ', '.join([str(symptom) for symptom in row['Symptom_1':'Symptom_25'] if pd.notnull(symptom)])
    print (f"existing_symptoms: {existing_symptoms}")
    # Check if the disease has less than 10 symptoms
    if existing_symptoms.count(',') < 9:
        symptoms = get_symptoms(icd_code, disease_name, existing_symptoms)
        print (f"new_symptoms: {symptoms}")
        
        # Add to the JSON file
        diseases_with_few_symptoms.append({
            'ICD 11 Code': icd_code,
            'Disease': disease_name,
            'Symptoms': existing_symptoms + ', ' + symptoms
        })

# Save the JSON file
with open('diseases_with_few_symptoms.json', 'w') as file:
    json.dump(diseases_with_few_symptoms, file)

print("JSON file created successfully!")
