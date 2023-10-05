import pandas as pd

# Load the xlsx file into a pandas DataFrame
df = pd.read_excel("Datasets/step_4/Disease_Dataset_22_09_2023.xlsx")

# Convert the DataFrame into a dictionary with ICD 11 codes as keys and Disease as values
data_dict = dict(zip(df["ICD 11"], df["Disease"]))

# Save the dictionary as a JSON file
with open("Datasets/step_4/Diseases.json", "w") as json_file:
    import json
    json.dump(data_dict, json_file, indent=4)

print("Excel file has been successfully converted to the desired JSON format!")
