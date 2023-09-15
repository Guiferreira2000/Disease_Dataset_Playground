import pandas as pd
import json
import os
import signal
from contextlib import contextmanager
import openai
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a timeout exception
class TimeoutException(Exception):
    pass

# Define a handler for the timeout
@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timed out!")
    signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)

def check_symptoms_with_chatgpt(disease, all_symptoms, mismatched_symptoms):
    content = f"""
    Disease: {disease}
    All Symptoms: {all_symptoms}
    Mismatched Symptoms: {', '.join(mismatched_symptoms)}
    Do you want to remove all mismatched symptoms? (y/n) If you want to keep some symptoms, type 'y' followed by the indices of the symptoms to keep (for example, 'y02' if you wish to keep the first and third symptom):
    """
    previous_response = None
    attempts = 0
    while attempts < 10:
        with time_limit(10):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a sophisticated medical expert assistant. Your primary objective is to meticulously analyze and determine whether the provided symptoms correlate with a specific disease. It's imperative that you adhere strictly to the required output format, ensuring clarity and precision in your response."},
                        {"role": "user", "content": content}
                    ],
                    max_tokens=10
                )
                current_response = response['choices'][0]['message']['content'].strip()
                if previous_response and previous_response == current_response:
                    return current_response
                previous_response = current_response
                attempts += 1
            except TimeoutException:
                attempts += 1
    return 'n'  # Default to 'n' if no consistent answer after 5 attempts

# Load the Excel file and the JSON file
df = pd.read_excel('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/Datasets/step_1/Disease_Dataset_with_new_symptoms.xlsx')
with open('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/Datasets/step_1/diseases_with_mismatched_symptoms.json') as f:
    mismatched_symptoms_data = json.load(f)

# Create a copy of the DataFrame
df_copy = df.copy()

# Load user inputs from the checkpoint file if it exists
user_inputs = {}
if os.path.exists('log/user_inputs.json'):
    with open('log/user_inputs.json', 'r') as f:
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
    
    # If user input for this disease is already stored, use it. Otherwise, ask the user.
    if disease not in user_inputs:
        user_input = check_symptoms_with_chatgpt(disease, all_symptoms, mismatched_symptoms)
        print(disease + ': ' + user_input + '\n')
        user_inputs[disease] = user_input  # Store the ChatGPT decision

    # Save the user inputs to the checkpoint file
    with open('log/user_inputs.json', 'w') as f:
        json.dump(user_inputs, f)

# Phase 2: Modify the DataFrame based on stored user inputs
for disease, user_input in tqdm(user_inputs.items(), desc="Modifying DataFrame", ncols=100):
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

    # Update the DataFrame with the expected symptoms
    for i, symptom in enumerate(expected_symptoms, start=1):
        df_copy.loc[df_copy['Disease'] == disease, f'Symptom_{i}'] = symptom
    for i in range(len(expected_symptoms)+1, 26):
        df_copy.loc[df_copy['Disease'] == disease, f'Symptom_{i}'] = None

    filtered_df = df_copy[df_copy['Disease'] == disease]
    if not filtered_df.empty:
        final_symptoms = filtered_df.iloc[0]['Symptom_1':'Symptom_25'].dropna().tolist()
    else:
        final_symptoms = []

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
df_copy.to_excel('/home/guilherme/Documents/GitHub/Tese/Dataset_Open_AI/Datasets/step_1/Disease_Dataset_Verified.xlsx', index=False)

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
# os.remove('log/user_inputs.json')