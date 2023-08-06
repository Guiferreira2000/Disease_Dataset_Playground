import os
import openai
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")



messages = [
    {"role": "system", "content": "You're a recruiter who asks interview questions. You ask one new question after my response"}
]


while True:
    content = input("User: ")
    messages.append({"role": "user", "content": content})

    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=messages
    )

    chat_response = completion.choices[0].message.content
    print(f'ChatGPT: {chat_response}')
    messages.append({"role": "assistant", "content": chat_response})