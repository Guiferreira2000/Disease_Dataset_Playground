import pandas as pd
import json

file_path = "/home/guilherme/Documents/Tese/Documentation/Dataset_teste/Disease_Dataset_02_08_2023.xlsx"
df = pd.read_excel(file_path)

# Convert to JSONL format
with open('dataset.jsonl', 'w') as file:
    for index, row in df.iterrows():
        icd_code = row['ICD 11'] # Assuming ICD 11 code is in column B
        disease = row['Disease']  # Assuming diseases are in column C
        symptoms = ', '.join(row['Symptom_1':'Symptom_25'].dropna().tolist()) # Using the correct headers for symptoms
        prompt = f"ICD Code: {icd_code}\nDisease: {disease}\nSymptoms:"
        completion = f" {symptoms}"
        json_line = {"prompt": prompt, "completion": completion}
        file.write(json.dumps(json_line) + '\n') # Write the line as a valid JSON object
