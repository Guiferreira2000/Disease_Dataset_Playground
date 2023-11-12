import pandas as pd

input_path = "Datasets/step_3/Labeled_Diseases_Dataset_22_09_2023.xlsx"
output_path = "Datasets/step_3/Labeled_Diseases_Dataset_29_09_2023.xlsx"

# Load the dataset
df = pd.read_excel(input_path, engine='openpyxl')

# Counter for transformed strings
transformed_count = 0

# Helper function to handle the transformation
def split_symptoms(row):
    global transformed_count
    new_row = row.copy()
    for col in df.columns[3:]:  # start from Symptom_1 column
        symptom = row[col]
        if pd.notna(symptom):  # check if symptom is not NaN
            # Splitting symptoms with '/'
            if '/' in symptom:
                transformed_count += 1
                s1, s2 = symptom.split('/')
                new_row[col] = s1
                # Find next available column
                idx = df.columns.get_loc(col) + 1
                while pd.notna(new_row[df.columns[idx]]):  # find next empty symptom column
                    idx += 1
                new_row[df.columns[idx]] = s2
            # Removing everything after '&'
            elif '&' in symptom:
                transformed_count += 1
                new_row[col] = symptom.split('&')[0]
    return new_row

# Apply the helper function
transformed_df = df.apply(split_symptoms, axis=1)

# Print the number of transformed strings
print(f"Number of transformed strings: {transformed_count}")

# Save the transformed dataframe
transformed_df.to_excel(output_path, index=False)
