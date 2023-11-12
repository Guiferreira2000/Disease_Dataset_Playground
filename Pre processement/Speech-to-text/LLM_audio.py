from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import openai
import re
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import TextLoader

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the path to your file
file_path = 'recorded_audio.txt'
# file_path = 'Datasets/step_3/icd_11_formated_data.json'

loader = TextLoader(file_path)
# loader = DirectoryLoader('/home/guilherme/Documents/GitHub/Tese/Disease_Dataset_Playground', glob='**/*.txt')
documents = loader.load()



# Convert the JSON data to a list of Document instances
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

texts = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()
# embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(texts, embeddings)


# qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch)


qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=docsearch.as_retriever(search_kwargs={"k": 1}))
# qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)




# Define the initial data observation



# Create the prompt for the API call
api_prompt = f'''
You are provided with a medical case text and your task is to filter out only the signs and symptoms mentioned in the text, without any further information.

Start your response always like this:

Signs and symptoms: [<Place the symtoms in here separeted by ", "]

'''

query = "Could you resume the text?"
query = api_prompt

result = qa({"query": query})


print(result['result'])

# New code block starts here
result_str = result['result']

# Check if the necessary prefix is in the result string
prefix = 'Signs and symptoms: '
if prefix in result_str:
    # Remove the prefix
    symptoms_str = result_str[len(prefix):]
    # As there's no closing bracket, we'll assume the symptoms list goes until the end of the string
    # Split the symptoms string into individual symptoms
    symptoms_list = [symptom.strip() for symptom in symptoms_str.split(',')]
else:
    print("No symptoms found")
    symptoms_list = []

# Now symptoms_list will contain all the symptoms in list format
print(symptoms_list)