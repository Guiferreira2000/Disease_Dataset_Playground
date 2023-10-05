import pandas as pd
import json
from collections import Counter

# Load the xlsx file
df = pd.read_excel("Datasets/step_2/symptoms_updated_ICD.xlsx")

# Check if the necessary columns are present in the dataframe
if 'Symptom' not in df.columns or 'ICD 11' not in df.columns:
    raise ValueError("The required columns (Symptom or ICD 11) are not present in the xlsx file.")

# Sort the dataframe based on the 'ICD 11' column
df = df.sort_values(by='ICD 11')

# Convert the dataframe to the desired JSON structure
data = [{"icd_11_code": icd, "symptom": symptom} for icd, symptom in zip(df['ICD 11'], df['Symptom'])]

# Save the data as a JSON file
# with open("Datasets/step_3/unique_symptoms_v2.json", "w") as json_file:
#     import json
#     json.dump(data, json_file, indent=4)

# print("Data has been successfully saved to output_sorted.json")



# Load the JSON data from the file
with open("Datasets/step_3/icd_11_GPT_formated_data_v2.json", "r") as f:
    json_data = json.load(f)

# Extract the symptom values from the loaded data
symptoms = [entry["symptom"] for entry in json_data]

# Identify duplicates
symptom_counts = Counter(symptoms)
duplicates = {symptom: count for symptom, count in symptom_counts.items() if count > 1}

print("Duplicate symptoms identified:")
for symptom, count in duplicates.items():
    print(f"{symptom}: {count} occurrences")