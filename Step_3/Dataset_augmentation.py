import pandas as pd
from itertools import combinations

# Load the Excel file
df = pd.read_excel('Datasets/step_3/Labeled_Diseases_Dataset_29_09_2023.xlsx')

# Create an empty DataFrame to store the augmented instances
augmented_data = pd.DataFrame(columns=df.columns)

# Fetching columns based on their names
disease_col = "Disease"
symptom_cols = [col for col in df.columns if "Symptom_" in col]

# Augment instances for each disease
for _, row in df.iterrows():
    disease = row[disease_col]
    symptoms = row[symptom_cols].dropna().tolist()

    # Create the original instance with all symptoms
    augmented_row = row[[col for col in df.columns if col not in symptom_cols]].to_dict()
    augmented_row.update({col: val for col, val in zip(symptom_cols, sorted(symptoms))})
    augmented_data = pd.concat([augmented_data, pd.DataFrame([augmented_row])], ignore_index=True)

    # Specify the desired number of augmented instances
    num_symptoms = len(symptoms)
    num_duplicates = num_symptoms - 1

    # Generate all combinations of symptoms for duplicates
    symptom_combinations = combinations(symptoms, num_symptoms - 1)

    # Create duplicates with different symptom combinations
    for combo in symptom_combinations:
        augmented_symptoms = sorted(list(combo))

        # Create a new row with augmented instance
        augmented_row = row[[col for col in df.columns if col not in symptom_cols]].to_dict()
        augmented_row.update({col: val for col, val in zip(symptom_cols[:num_duplicates], augmented_symptoms)})
        augmented_data = pd.concat([augmented_data, pd.DataFrame([augmented_row])], ignore_index=True)

# Save the original dataset to the first sheet
with pd.ExcelWriter('Datasets/step_3/Augmented_database_29_09_2023.xlsx') as writer:
    df.to_excel(writer, sheet_name='Original Data', index=False)
    augmented_data.to_excel(writer, sheet_name='Augmented Data', index=False)
