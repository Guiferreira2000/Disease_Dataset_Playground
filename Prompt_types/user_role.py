import os
import openai
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")


content = "Quem foi o ultimo rei de Portugal?"
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "user", "content": content}
  ]
)

chat_response = completion.choices[0].message.content
print(f'ChatGPT: {chat_response}')