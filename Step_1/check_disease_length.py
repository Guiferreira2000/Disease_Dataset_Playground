import pandas as pd
import json
import matplotlib.pyplot as plt
import plotly.express as px

# Load the Excel file into a pandas DataFrame
df = pd.read_excel("Datasets/step_1/Disease_Dataset_19_09_2023.xlsx", engine='openpyxl')

# Number of symptoms threshold
threshold = 11

# Create an empty list to store the diseases with fewer than 10 symptoms
diseases_less_than_10_symptoms = []

# Create a list to store symptom counts for all diseases
symptom_counts = []

# Iterate over each row in the DataFrame
for _, row in df.iterrows():
    # Count non-null symptoms
    symptom_count = row.loc['Symptom_1':'Symptom_25'].count()
    
    # Append the symptom count to the list for plotting
    symptom_counts.append(symptom_count)

    # Check if there are fewer than 10 non-null symptoms
    if symptom_count < threshold:
        disease_info = {
            'Code': row['Code'],
            'ICD 11': row['ICD 11'],
            'Disease': row['Disease'],
            'Symptoms': row.loc['Symptom_1':'Symptom_25'].dropna().tolist()
        }
        diseases_less_than_10_symptoms.append(disease_info)

# Plot the histogram using matplotlib
plt.figure(figsize=(10, 6))
plt.hist(symptom_counts, bins=range(1, 27), color='skyblue', edgecolor='black', align='left')
plt.ylabel('Number of Diseases')
plt.xlabel('Number of Symptoms')
plt.title('Distribution of Diseases by Number of Symptoms')
plt.xticks(range(1, 26))
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('data_insight/symptoms_histogram.png')
plt.close()

# Create a DataFrame for plotting with plotly
plot_df = pd.DataFrame({'Number of Symptoms': symptom_counts})
plot_df['Number of Symptoms'] = plot_df['Number of Symptoms'].astype(str) + ' Symptoms'

# Create the interactive histogram using plotly express
fig = px.histogram(plot_df, x="Number of Symptoms", title="Distribution of Diseases by Number of Symptoms")
fig.write_html("data_insight/symptoms_histogram_interactive.html")

# Write the list to a JSON file
with open("data_insight/output.json", "w") as outfile:
    json.dump(diseases_less_than_10_symptoms, outfile, indent=4)

# Print the count of diseases with fewer than 10 symptoms
print(f"There are {len(diseases_less_than_10_symptoms)} diseases with fewer than {threshold} symptoms.")

print("Process complete! Check 'output.json' for the results, 'symptoms_histogram.png' for the static graph, and 'symptoms_histogram_interactive.html' for the interactive histogram.")
