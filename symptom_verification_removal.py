import pandas as pd
import json
import os

# Load the Excel file and the JSON file
df = pd.read_excel('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/draft.xlsx')
with open('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/diseases_with_mismatched_symptoms_v2.json') as f:
    mismatched_symptoms_data = json.load(f)

# Create a copy of the DataFrame
df_copy = df.copy()

# Load user inputs from the checkpoint file if it exists
user_inputs = {}
if os.path.exists('user_inputs.json'):
    with open('user_inputs.json', 'r') as f:
        user_inputs = json.load(f)

# Initialize the incident log
incident_log = []

# Phase 1: Collect user inputs for each disease
for disease_data in mismatched_symptoms_data:
    disease = disease_data['Disease']

    # Check if the disease exists in the DataFrame
    if disease not in df_copy['Disease'].values:
        print(f"Warning: Disease '{disease}' not found in the Excel file.")
        continue

    mismatched_symptoms = disease_data['Mismatched Symptoms'].split(', ')
    
    # Get the row of the disease in the DataFrame
    disease_row = df_copy[df_copy['Disease'] == disease].iloc[0]
    
    # Get all the symptoms of the disease
    all_symptoms = ', '.join([str(symptom) for symptom in disease_row['Symptom_1':'Symptom_25'] if pd.notnull(symptom)])
    
    print(f"Disease: {disease}")
    print(f"All Symptoms: {all_symptoms}")
    print(f"Mismatched Symptoms: {', '.join(mismatched_symptoms)}")
    
    # If user input for this disease is already stored, use it. Otherwise, ask the user.
    if disease not in user_inputs:
        user_input = input("Do you want to remove all mismatched symptoms? (y/n) If you want to keep some symptoms, type 'y' followed by the indices of the symptoms to keep (e.g., 'y02' to keep the first and third symptom): ")
        user_inputs[disease] = user_input  # Store the user input

    # Save the user inputs to the checkpoint file
    with open('user_inputs.json', 'w') as f:
        json.dump(user_inputs, f)

# Phase 2: Modify the DataFrame based on stored user inputs
for disease, user_input in user_inputs.items():
    mismatched_symptoms = [data['Mismatched Symptoms'].split(', ') for data in mismatched_symptoms_data if data['Disease'] == disease][0]
    all_symptoms = ', '.join([str(symptom) for symptom in df_copy[df_copy['Disease'] == disease].iloc[0]['Symptom_1':'Symptom_25'] if pd.notnull(symptom)])

    # If the user provides an invalid input, assume 'n'
    if user_input.lower() not in ['y', 'n'] and not user_input.lower().startswith('y'):
        user_input = 'n'
    
    # If the user wants to remove all mismatched symptoms
    if user_input.lower() == 'y':
        for symptom in mismatched_symptoms:
            df_copy.loc[df_copy['Disease'] == disease, df_copy.columns[df_copy.eq(symptom).any()]] = None
        expected_symptoms = [symptom for symptom in all_symptoms.split(', ') if symptom not in mismatched_symptoms]
    # If the user wants to keep some symptoms
    elif user_input.lower().startswith('y'):
        symptoms_to_keep_indices = [int(index) for index in user_input[1:]]
        symptoms_to_remove = [symptom for i, symptom in enumerate(mismatched_symptoms) if i not in symptoms_to_keep_indices]
        for symptom in symptoms_to_remove:
            df_copy.loc[df_copy['Disease'] == disease, df_copy.columns[df_copy.eq(symptom).any()]] = None
        expected_symptoms = [symptom for symptom in all_symptoms.split(', ') if symptom not in symptoms_to_remove]
    else:  # user_input is 'n'
        expected_symptoms = all_symptoms.split(', ')

    final_symptoms = df_copy[df_copy['Disease'] == disease].iloc[0]['Symptom_1':'Symptom_25'].dropna().tolist()

    wrongly_analyzed_symptoms = list(set(expected_symptoms) - set(final_symptoms))
    if wrongly_analyzed_symptoms or set(expected_symptoms) != set(final_symptoms):
        accuracy_rate = len(set(expected_symptoms).intersection(set(final_symptoms))) / len(set(expected_symptoms)) * 100
        incident_log.append({
            'Disease': disease,
            'Initial Symptoms': all_symptoms.split(', '),
            'User Input': user_input,
            'Mismatched Symptoms': mismatched_symptoms,
            'Expected Symptoms': expected_symptoms,
            'Final Symptoms': final_symptoms,
            'Wrongly Analyzed Symptoms': wrongly_analyzed_symptoms,
            'Accuracy Rate': f"{accuracy_rate:.2f}%"
        })

# Reorder the symptom columns for each disease
for index, row in df_copy.iterrows():
    symptoms = [symptom for symptom in row['Symptom_1':'Symptom_25'] if pd.notnull(symptom)]
    for i, symptom in enumerate(symptoms, start=1):
        df_copy.at[index, f'Symptom_{i}'] = symptom
    for i in range(len(symptoms)+1, 26):
        df_copy.at[index, f'Symptom_{i}'] = None

# Save the modified DataFrame to a new Excel file
df_copy.to_excel('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/Disease_Dataset_Verified.xlsx', index=False)

# Ensure the logs directory exists
if not os.path.exists('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/logs/'):
    os.makedirs('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/logs/')

# Save the incident log to a file
with open('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/logs/incident_log.txt', 'w') as f:
    for incident in incident_log:
        f.write(f"Disease: {incident['Disease']}\n")
        f.write(f"Initial Symptoms: {', '.join(incident['Initial Symptoms'])}\n")
        f.write(f"User Input: {incident['User Input']}\n")
        f.write(f"Mismatched Symptoms: {', '.join(incident['Mismatched Symptoms'])}\n")
        f.write(f"Expected Symptoms: {', '.join(incident['Expected Symptoms'])}\n")
        f.write(f"Final Symptoms: {', '.join(incident['Final Symptoms'])}\n")
        f.write(f"Wrongly Analyzed Symptoms: {', '.join(incident['Wrongly Analyzed Symptoms'])}\n")
        f.write(f"Accuracy Rate: {incident['Accuracy Rate']}\n")
        f.write('-' * 100 + '\n')

# Inform the user if any incidents were logged
if incident_log:
    print(f"{len(incident_log)} incidents were logged. Please check '/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/logs/incident_log.txt' for details.")
else:
    print("No incidents were logged.")

# Delete the checkpoint file
os.remove('user_inputs.json')
