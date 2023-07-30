import openai
import pandas as pd
from tqdm import tqdm

# Initialize OpenAI API
openai.api_key = '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'

# Read the CSV
print("Reading the CSV file...")
df = pd.read_csv('Disease_Dataset_24_07_2023.csv')

# Function to get symptoms from OpenAI
def get_symptoms(disease):
    print(f"Fetching symptoms for {disease}...")
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"List 20 symptoms of {disease}",
        max_tokens=150
    )
    # Parse the response to extract symptoms (this might need refining)
    symptoms = response.choices[0].text.split('\n')
    return symptoms

# Add symptoms
print("Processing diseases...")
for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    symptoms = get_symptoms(row['Disease'])
    for i, symptom in enumerate(symptoms):
        column_name = f'Symptom_{i+1}'
        df.at[index, column_name] = symptom

# Save back to CSV
print("Saving the updated data to CSV...")
df.to_csv('Updated_Disease_Dataset.csv', index=False)
print("Process completed!")
