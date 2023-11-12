import requests
import json
import os
import openai
import datetime
# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("prompt", help="Write here the prompt to the OpenAI API")
# args = parser.parse_args()

# API available models:
# https://platform.openai.com/docs/models/overview

# api_key = os.getenv("OPENAI_API_KEY")

api_key = "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"

# Load your API key from an environment variable or secret management service
openai.organization = "FCUL"
openai.api_key = os.getenv(api_key)

#########
# API Reference - Complitions:
# https://platform.openai.com/docs/api-reference/completions

api_endpoint = "https://api.openai.com/v1/completions"
request_headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + api_key
}

request_data = {
  "model": "text-davinci-003",
  "prompt": "Print todays date", # f"{args.prompt}",
  "max_tokens": 7,
  "temperature": 0.1,
  # "top_p": 1,
  # "n": 1,
  # "stream": False,
  # "logprobs": null,
  # "stop": "\n"
}
response = requests.post(api_endpoint, headers=request_headers, json=request_data)

if response.status_code == 200:
  print(response.json()["choices"][0]["text"])
  response_text = response.json()["choices"][0]["text"]
  # response_data = json.loads(response_text)

  with open(f'/home/guilherme/Documents/MDCompass Documentation/json files/Chatgpt/search_results_{openai.organization}.json', 'w') as f:
    json.dump(response_text, f, indent=2)

else:
  print(f"Request failed with code: {str(response.status_code)}")


# response = openai.Completion.create(
#   model="text-davinci-003",
#   prompt="Say this is a test",
#   temperature=0, # Setting temperature to 0 will make the outputs mostly deterministic, but a small amount of variability may remain.
#   max_tokens=7 # Controls the response behaviour in length
# )

