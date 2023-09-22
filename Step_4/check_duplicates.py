import pandas as pd

# Load the dataset
file_path = "Datasets/step_1/Disease_Dataset_22_09_2023.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

# Check for duplicates in the "ICD 11" column
duplicates = df[df.duplicated(subset='ICD 11', keep=False)].sort_values(by="ICD 11")

# Output the results
if duplicates.shape[0] > 0:
    print("There are duplicates in the 'ICD 11' column. Here are the duplicated values:")
    for index, row in duplicates.iterrows():
        print(f"Code {row['Code']}: {row['ICD 11']} - Disease: {row['Disease']}")
else:
    print("There are no duplicates in the 'ICD 11' column.")
