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
pprint(data)


# Define a function to extract metadata if needed
def metadata_func(record: dict, metadata: dict) -> dict:
    # Extract any additional metadata you need from the record
    # For example:
    metadata["Symptom"] = record.get("Symptom")
    return metadata

# Use the JSONLoader to extract the desired data
loader = JSONLoader(
    file_path='Datasets/step_3/icd_11_data.json',
    jq_schema='.[] | .[].Symptom',  # This schema extracts the 'Symptom' values from each entry
    metadata_func=metadata_func  # Optional: use this if you want to extract additional metadata
)

loaded_data = loader.load()
# pprint(loaded_data)



## Section 2

symptoms = [doc.page_content for doc in loaded_data]

# If you want to split symptoms (might not be necessary given the nature of the data)
text_splitter = CharacterTextSplitter(
    separator = "    ],",
    chunk_size=100,
    chunk_overlap=20,
    length_function=len,
    add_start_index=True
)

split_texts = text_splitter.create_documents(symptoms)
print(len(split_texts))
print(split_texts[0])
print(split_texts[1])

# Extract Metadata
metadata_list = []
for key in data:
    for entry in data[key]:
        metadata = {
            'Frequency': entry['Frequency'],
            'Similar terms': entry['Similar terms']
        }
        metadata_list.append(metadata)


# text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=1)

# texts = text_splitter.split_documents(loaded_data)
# #print(texts)

# embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
# docsearch = Chroma.from_documents(texts, embeddings)

# qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch)

# query = "You have access to a dictionary of different ICD codes that represent a interval of symptoms. Do you have acces to the dictionaries?"
# qa.run(query)
# result = qa({"query": query})


# print(result)