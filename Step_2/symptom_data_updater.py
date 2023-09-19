import pandas as pd

# 1. Read both Excel files into pandas DataFrames
df_output = pd.read_excel("Datasets/step_2/symptoms_preprocessing_19_09_2023.xlsx")
df_old = pd.read_excel("Datasets/step_2/symptoms_pre_processing_01_08_2023.xlsx")

# 2. For each symptom in output_symptoms.xlsx, 
# check if it's present in symptoms_pre_processing_01_08_2023.xlsx.
# 3. If present, copy the associated data 
for index, row in df_output.iterrows():
    symptom = row["Symptom"]
    matching_row = df_old[df_old["Symptom"] == symptom]

    if not matching_row.empty:
        for col in matching_row.columns:
            # Update the values for columns present in the older version
            df_output.at[index, col] = matching_row[col].values[0]

# 4. Save the updated output_symptoms.xlsx DataFrame.
df_output.to_excel("Datasets/step_2/output_symptoms_updated.xlsx", index=False)
