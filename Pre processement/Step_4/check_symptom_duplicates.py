import pandas as pd
## This code isnt working!!!
input_path = "Datasets/step_3/Labeled_Diseases_Dataset_29_09_2023.xlsx"
output_path = "Datasets/step_3/Disease_Dataset_NoDuplicates_29_09_2023.xlsx"

# # Load the dataset
# df = pd.read_excel(input_path, engine='openpyxl')

# # Helper function to handle duplicate removal and print duplicate symptoms
# def remove_duplicates(row):
#     symptoms = row[2:].dropna().tolist()  # Extract symptoms and drop NaNs
#     unique_symptoms_set = set()  # Set to hold unique symptoms
#     duplicates = set()  # Set to hold duplicated symptoms

#     # Identify unique and duplicate symptoms
#     for s in symptoms:
#         if s in unique_symptoms_set:
#             duplicates.add(s)
#         else:
#             unique_symptoms_set.add(s)

    # Print duplicate symptoms
    # if duplicates:
    #     print(f"For disease '{row['Disease']}', the duplicated symptoms are: {', '.join(duplicates)}")

#     unique_symptoms = list(unique_symptoms_set)  # Convert set to list

#     # Replace original symptoms with unique symptoms and set the rest to NaN
#     for idx, col in enumerate(df.columns[2:], start=2):
#         if idx - 2 < len(unique_symptoms):
#             row[col] = unique_symptoms[idx - 2]
#         else:
#             row[col] = None

#     return row

# # Apply the helper function
# df_no_duplicates = df.apply(remove_duplicates, axis=1)

# # Save the dataframe without duplicates
# df_no_duplicates.to_excel(output_path, index=False)
