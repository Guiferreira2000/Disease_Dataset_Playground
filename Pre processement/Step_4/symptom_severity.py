import openai
import json
import re
import signal
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Handling timeouts
class TimeoutException(Exception): pass

def handler(signum, frame):
    raise TimeoutException()

# Set the signal handler and a 10-second alarm
signal.signal(signal.SIGALRM, handler)

def get_severity_score(code, symptoms):
    total_score = 0
    num_responses = 3  # Since we'll always assume a score of 5 if no valid score is returned

    for _ in range(3):  # Ask the model three times
        content = (f"Based on these symptoms {', '.join(symptoms)}, "
                   "please assign an average severity score from 1-10 as your answer. Don't respond anything else and try to follow a Gaussian distribution")

        signal.alarm(10)  # Set an alarm for 10 seconds
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical expert assistant. Your task is to provide a severity score for a given ICD 11 code and its associated symptoms."},
                    {"role": "user", "content": content}
                ]
            )
            full_response = response['choices'][0]['message']['content'].strip()
            print(f"ICD 11 code: {code} - Response: {full_response}")  # Print the model's response
            
            # Use regex to extract numbers from the response
            match = re.search(r'(\d+)', full_response)  # Looking for a single-digit or double-digit integer
            result = int(match.group(0)) if match else 5  # Assign a score of 5 if no valid score is found
            if result < 1 or result > 10:
                raise ValueError("Invalid score range")
            total_score += result

        except (TimeoutException, ValueError):
            total_score += 5  # If there's a timeout or value error, assume a score of 5 for that attempt
        finally:
            signal.alarm(0)  # Cancel the alarm

    average_score = total_score / num_responses
    return average_score

# Load data from JSON
with open("Datasets/step_3/icd_11_formated_data_dict.json", "r") as f:
    data = json.load(f)

severity_scores = {}

for code, info in data.items():
    symptoms = info['Symptoms']
    score = get_severity_score(code, symptoms)
    severity_scores[code] = round(score, 2)

# Save the severity scores to a JSON file
with open('Datasets/step_4/severity_scores.json', 'w') as f:
    json.dump(severity_scores, f)

print("Datasets/step_4/Severity scores saved to severity_scores.json!")
