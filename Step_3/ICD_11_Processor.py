import pandas as pd

# Load the dataset
df = pd.read_excel("Datasets/step_2/symptoms_updated_ICD.xlsx")

# Extract unique ICD 11 codes and sort them
unique_icd_codes = sorted(df['ICD 11'].unique())

# Write the sorted unique ICD 11 codes to a new Excel file
pd.DataFrame(unique_icd_codes, columns=['ICD 11']).to_excel("Datasets/step_3/sorted_unique_ICD_11_codes.xlsx", index=False)

# Create a JSON file
icd_json = {}

for code in unique_icd_codes:
    # Filter rows with the current ICD 11 code and create a copy
    filtered_df = df[df['ICD 11'] == code].copy()
    
    # Consolidate the terms into "Similar terms"
    filtered_df.loc[:, 'Similar terms'] = filtered_df[['Suggested changes', 'Medical term 1', 'Medical term 2', 'Medical term 3', 'Medical term 4']].apply(lambda x: x.dropna().tolist(), axis=1)
    
    # Drop the original columns
    filtered_df = filtered_df.drop(columns=['ICD 11', 'Suggested changes', 'Medical term 1', 'Medical term 2', 'Medical term 3', 'Medical term 4'])
    
    # Convert the filtered dataframe to a list of dictionaries
    rows_list = filtered_df.to_dict(orient='records')
    
    # Add to the JSON structure
    icd_json[code] = rows_list

# Save the JSON structure to a file
with open("Datasets/step_3/icd_11_data.json", "w") as f:
    import json
    json.dump(icd_json, f, indent=4)

print("Processing complete!")
