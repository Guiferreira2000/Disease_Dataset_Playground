import pandas as pd
dataset_1 = "Datasets/step_2/output_symptoms_updated.xlsx"
dataset_2 = "Datasets/step_2/symptoms_updated_ICD.xlsx"
# Read the Excel file into a pandas DataFrame
df = pd.read_excel(dataset_2)

# Select only rows up to index 1233 (0-indexed, so it includes the row at index 1233)
df_subset = df.loc[:1233]

# Count the number of empty cells in the "ICD 11" column for the subset
empty_count = df_subset["ICD 11"].isna().sum()

print(f"Number of empty cells in the 'ICD 11' column up to row 1233: {empty_count}")
