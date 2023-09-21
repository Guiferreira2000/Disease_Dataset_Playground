from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import JSONLoader
import magic
import os
import nltk
import json
from pathlib import Path
from pprint import pprint
from dotenv import load_dotenv
import jq
import openai


# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the path to your file
file_path = 'Datasets/step_3/icd_11_data.json'

# Load the data from the file
data = json.loads(Path(file_path).read_text())

# Convert the JSON data to a list of stringified dictionary entries
split_texts = [{"page_content": json.dumps({key: value}), "metadata": {}} for key, value in data.items()]

# Print the first two split_texts to verify
print(split_texts[0])
print(split_texts[1])