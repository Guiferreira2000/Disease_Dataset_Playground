import openai
import pandas as pd
import os
import json
import re
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
    content = f"Disease: {disease_name}\nExisting Symptoms: {existing_symptoms}\nBased on the existing symptoms and the nature of the disease, please provide additional symptoms that might be associated with this disease. The new symptoms should be in medical terminology, each symptom should have between 1 to 3 words, and should not include risk factors or descriptions. Please provide 5 additional symptoms."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a medical expert assistant. Your task is to provide additional symptoms for diseases based on their existing symptoms. The symptoms should be in medical terminology, should not include risk factors or descriptions, and each symptom should have between 1 to 3 words."},
            {"role": "user", "content": content}
        ],
        max_tokens=100
    )
    symptoms = response['choices'][0]['message']['content'].strip()
    return symptoms


def process_symptoms(symptoms):
    # Replace newlines with commas
    symptoms = symptoms.replace('\n', ', ')
    
    # Split the symptoms string into a list of symptoms
    symptoms_list = symptoms.split(', ')
    
    # Remove numbering, content within parentheses, and additional sentences from each symptom, and strip leading/trailing whitespaces
    symptoms_list = [re.sub(r'\d+\.\s*|\s*\(.*?\)|.*:', '', symptom).strip() for symptom in symptoms_list]
    
    # Remove any empty strings from the list
    symptoms_list = [symptom for symptom in symptoms_list if symptom]
    
    # Join the symptoms back into a string
    symptoms = ', '.join(symptoms_list)
    
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
        symptoms = process_symptoms(symptoms)
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
