import openai
import pandas as pd
import os
import json
import re
import time  # Required for the sleep function
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your existing Excel file
excel_path = "Datasets/step_1/draft.xlsx"

# Read the existing Excel file
df = pd.read_excel(excel_path)

# Global constants for retry mechanism
MAX_RETRIES = 3
RETRY_WAIT_SECONDS = 10

# Function to get symptoms with error handling and retry mechanism
def get_symptoms(icd_code, disease_name, existing_symptoms):
    content = f"Disease: {disease_name}\nExisting Symptoms: {existing_symptoms}\nBased on the existing symptoms and the nature of the disease, please provide additional symptoms that might be associated with this disease. The new symptoms should be in medical terminology, each symptom should have between 1 to 3 words, and should not include risk factors or descriptions. Please provide 6 additional symptoms."
    
    retries = 0
    while retries < MAX_RETRIES:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a medical expert assistant. Your task is to provide additional signs or symptoms for diseases based on their existing symptoms. The symptoms should be in medical terminology, should not include risk factors or descriptions, and each symptom should have between 1 to 3 words."},
                    {"role": "user", "content": content}
                ],
                max_tokens=100
            )
            symptoms = response['choices'][0]['message']['content'].strip()
            return symptoms
        except openai.error.APIError:
            retries += 1
            print(f"Error occurred for disease {disease_name}. Retrying in {RETRY_WAIT_SECONDS} seconds (Retry {retries}/{MAX_RETRIES}).")
            time.sleep(RETRY_WAIT_SECONDS)
    
    print(f"Failed to get symptoms for disease {disease_name} after {MAX_RETRIES} attempts.")
    return ''

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

# New list to store added symptoms information
added_symptoms_dict = {}

# Iterate through the DataFrame and update or add data
for index, row in df.iterrows():
    icd_code = row['ICD 11']
    disease_name = row['Disease']
    existing_symptoms = ', '.join([str(symptom) for symptom in row['Symptom_1':'Symptom_25'] if pd.notnull(symptom)])
    # Check if the disease has less than 10 symptoms
    if existing_symptoms.count(',') < 12:
        symptoms = get_symptoms(icd_code, disease_name, existing_symptoms)
        symptoms = process_symptoms(symptoms)
        print(f"Disease: {disease_name}")
        print(f"existing_symptoms: {existing_symptoms}")
        print(f"\nnew_symptoms: {symptoms}")
        
        # Add the new symptoms to the DataFrame
        new_symptoms_list = symptoms.split(', ')
        for i, symptom in enumerate(new_symptoms_list, start=1):
            column_name = f'Symptom_{i+existing_symptoms.count(",")+1}'
            df.at[index, column_name] = symptom
        
        # Save the added symptoms to the added_symptoms_info list
        added_symptoms_dict[disease_name] = {
            'ICD 11': icd_code,
            'Existing_symptoms': existing_symptoms,
            'Added Symptoms': new_symptoms_list
        }
    
    # Save the data iteratively (e.g., every 10 rows)
    if index % 10 == 0:
        df.to_excel('Disease_with_added_symptoms_temp.xlsx', index=False)
        with open('added_symptoms_temp.json', 'w') as file:
            json.dump(added_symptoms_dict, file, indent=4)
        print(f"Temporary data saved at index {index}!")

# Save the modified DataFrame to a new Excel file
df.to_excel('Disease_with_added_symptoms.xlsx', index=False)

print("Excel file created successfully!")

# Save the added symptoms to a new JSON file
with open('added_symptoms.json', 'w') as file:
    json.dump(added_symptoms_dict, file, indent=4)

print("Added symptoms JSON file created successfully!")
