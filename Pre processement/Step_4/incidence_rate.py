import openai
import signal
import pandas as pd
import re
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Exception for handling timeouts
class TimeoutException(Exception):
    pass

# Handler function for the alarm
def handler(signum, frame):
    raise TimeoutException()

# Setting up the handler
signal.signal(signal.SIGALRM, handler)

def get_incidence_rate(disease_name):
    content = (f"Please provide the incidence rate of {disease_name} in Europe "
               "expressed in a percentage form from 0.00 - 100.")
    
    signal.alarm(10)  # Set an alarm for 10 seconds
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical expert assistant. Your task is to provide the incidence rate of a given disease in Europe in a specific format."},
                {"role": "user", "content": content}
            ]
        )
        full_response = response['choices'][0]['message']['content'].strip()
        
        # Use regex to extract numbers from the response
        match = re.search(r'(\d+(\.\d+)?)', full_response)
        result = match.group(0) if match else "No numeric data found"

    except TimeoutException:
        result = "Timeout: Could not retrieve information in time."
    finally:
        signal.alarm(0)  # Cancel the alarm
    return result

# Read diseases from the Excel file using pandas
file_path = "Datasets/step_1/Disease_Dataset_22_09_2023.xlsx"
df = pd.read_excel(file_path)
diseases = df['Disease'].tolist()

# List to store results
results = []

# Fetch incidence rates for each disease
for disease in diseases:
    incidence_rate = get_incidence_rate(disease)
    print(f"{disease}: {incidence_rate}")  # This line prints the output for each disease
    results.append({
        'Disease': disease,
        'Incidence Rate in Europe': incidence_rate
    })

# Convert the results to a DataFrame and save to a new Excel file
results_df = pd.DataFrame(results)
results_df.to_excel("Datasets/step_4/Disease_Incidence_Rates.xlsx", index=False)
