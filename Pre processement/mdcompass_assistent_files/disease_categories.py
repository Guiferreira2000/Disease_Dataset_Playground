import json

# Path to the original file
input_file_path = 'Pre processement/Step_1/Diseases_category.json'
# Path to the new file
output_file_path = 'Pre processement/Step_1/Refactored_Diseases_category.json'

# Function to refactor the category
def refactor_category(category):
    mapping = {
        "Inflammatory diseases": "inflammatory",
        "Non-specific": "non_specific",
        "Metabolic diseases": "metabolic",
        "Renal diseases": "renal",
        "Gastrointestinal diseases": "gastrointestinal",
        "Hepatic diseases": "hepatic",
        "Endocrine diseases": "endocrine"
    }
    return mapping.get(category, category)  # Default to original if not in mapping

# Reading the original JSON file
with open(input_file_path, 'r') as file:
    data = json.load(file)

# Refactoring the data
refactored_data = {key: refactor_category(value) for key, value in data.items()}

# Writing the refactored data to a new JSON file
with open(output_file_path, 'w') as file:
    json.dump(refactored_data, file, indent=4)

print(f"Refactored data written to {output_file_path}")
