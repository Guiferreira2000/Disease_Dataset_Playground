import os
import openai
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "You're a recruiter who asks tough interview questions"}
]


while True:
    content = input("User: ")
    content = "Onde vão ser as jornadas da juventude em 2023?"
    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')