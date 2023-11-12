import openai
import pandas as pd
import os
import json
import re
import signal
from collections import defaultdict
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to the Excel file with new symptoms
excel_path = "Disease_Dataset_with_new_symptoms.xlsx"

# Read the Excel file
df = pd.read_excel(excel_path)

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

# Function to check symptoms with the model
def check_symptom(disease_name, symptom):
    content = f"Disease: {disease_name}\nSymptom: {symptom}\nIf you are at least 95% certain that the symptom is not associated with the disease, say 'no'. Otherwise, say 'yes'."
    signal.alarm(10)  # Set an alarm for 10 seconds
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a medical expert assistant. Your task is to verify if a given symptom is associated with a specific disease. Only reject the association if you are at least 95% certain."},
                {"role": "user", "content": content}
            ],
            max_tokens=10
        )
        result = response['choices'][0]['message']['content'].strip().lower() == 'yes'
    except TimeoutException:
        result = True  # If the function times out, assume the symptom is associated with the disease
    finally:
        signal.alarm(0)  # Cancel the alarm
    return result

# Dictionary to store diseases with mismatched symptoms
diseases_with_mismatched_symptoms = defaultdict(list)

# Read the last completed index from a file
try:
    with open('last_completed_index.txt', 'r') as file:
        last_completed_index = int(file.read())
except FileNotFoundError:
    last_completed_index = 0

# Counters for the total number of symptoms and mismatches
total_symptoms = 0
total_mismatches = 0

# Iterate through the DataFrame and check each symptom
for index, row in df.loc[last_completed_index:].iterrows():
    disease_name = row['Disease']
    print(f"\nDisease: {disease_name}")
    disease_symptoms = 0
    disease_mismatches = 0
    for symptom in row['Symptom_1':'Symptom_25']:
        if pd.notnull(symptom):
            print(f"Checking symptom: {symptom}")
            disease_symptoms += 1
            total_symptoms += 1
            if not check_symptom(disease_name, symptom):
                print(f"Mismatched symptom: {symptom}")
                diseases_with_mismatched_symptoms[disease_name].append(symptom)
                disease_mismatches += 1
                total_mismatches += 1
    # Calculate the accuracy for the disease
    disease_accuracy = (disease_symptoms - disease_mismatches) / disease_symptoms * 100
    print(f"Accuracy for {disease_name}: {disease_accuracy}%")
    # Save the index of the last completed disease check to a file
    with open('last_completed_index.txt', 'w') as file:
        file.write(str(index))

# Calculate the total accuracy
total_accuracy = (total_symptoms - total_mismatches) / total_symptoms * 100
print(f"Total accuracy: {total_accuracy}%")

# Convert the dictionary to a list of dictionaries
diseases_with_mismatched_symptoms = [{'Disease': disease, 'Mismatched Symptoms': ', '.join(symptoms)} for disease, symptoms in diseases_with_mismatched_symptoms.items()]

# Save the JSON file
with open('diseases_with_mismatched_symptoms.json', 'w') as file:
    json.dump(diseases_with_mismatched_symptoms, file)

print("JSON file created successfully!")

# Delete the last_completed_index.txt file
if os.path.exists("last_completed_index.txt"):
    os.remove("last_completed_index.txt")
else:
    print("The file does not exist")
