import pandas as pd

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
with open("Datasets/step_3/unique_symptoms_v2.json", "w") as json_file:
    import json
    json.dump(data, json_file, indent=4)

print("Data has been successfully saved to output_sorted.json")
