from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
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
import re
# !pip install langchain watermark openai jq

os.environ['OPENAI_API_KEY'] = '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'

file_path = '/home/guilherme/Documents/Github/Tese/Disease_Dataset_Playground/Server_Models/API_Requests/json_files/icd_11_GPT_formated_data_v2.json'


# Prints the json file (Not important, just an example)
data = json.loads(Path(file_path).read_text())
# pprint(data)



class Document:
    def __init__(self, page_content, metadata={}):
        if not isinstance(page_content, str):
            raise ValueError("page_content must be a string")
        self.page_content = page_content
        self.metadata = metadata


# Creating Document objects
documents = [Document(json.dumps(entry), {}) for entry in data]

print(f"\n\n\n ---> {documents[0].page_content}") # "{icd_11_code: 1A07.Y, symptom: Ulceration}
print(f"\n\n\n ---> {documents[1].page_content}\n\n\n") # {icd_11_code: 1A07.Y, symptom: Ulcerations}\n1C82"}

text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=1500)
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)


    # For tasks where context is critical and resources are abundant, larger chunks with more overlap might be better.
    # For tasks where speed and resource efficiency are paramount, smaller chunks with minimal overlap might be more appropriate.

texts = text_splitter.split_documents(documents)
#print(texts)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(documents, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)

# Define the initial data observation
df_head = "\n".join([json.dumps(entry) for entry in data[:5]])
# df_head = "\n".join([json.dumps({key: data[key]}) for key in list(data.keys())[:5]])

symptom = "Fear of water"
# Define the question you want to answer
input_question = f"Which code is more closely associated with {symptom}?"

# Create the prompt for the API call
api_prompt = f'''
You are analyzing a dataset of medical symptoms and their associated ICD 11 Codes. The dataset is formatted as a list of dictionaries, where each dictionary contains:

1. "ICD 11 Code": Represents the unique code for a medical condition.
2. "Symptom": Describes a symptom associated with that medical condition.

Sample data from the dataset:
{df_head}

Your task is to meticulously analyze and determine the most relevant ICD-11 code for a given symptom. This involves intelligently recognizing and mapping the symptom, including those not explicitly listed in our database, to its closest equivalent in the dataset. For instance, if presented with a symptom like 'Fear of water', you must astutely infer its association with 'Hydrophobia', which corresponds to the ICD-11 code '1C82'. Your approach should be context-aware and capable of discerning semantic similarities and nuances in symptoms, ensuring accurate and reliable identification of the appropriate ICD-11 codes.

You always have to use and print the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [python_repl_ast]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: Present only the code value

Begin!
Question: {input_question}
'''

# query = "Its not suposed to have the same or similar synonyms associated with different codes. The labelling must not be redundant. Try to identify redundant synonyms"

result = qa({"query": api_prompt})

print(result['result'])



def extract_icd_code(output_string):
    """
    Extracts the ICD code from the given output_string.

    Args:
    - output_string (str): The input string containing the ICD code.

    Returns:
    - str: The found ICD code. Returns None if no code is found.
    """

    # The regex pattern to find ICD code from the given format.
    pattern = r"(?:[A-Z]{4}\d{1,}|[A-Z0-9]{4})(?:\.[A-Z0-9]+)?"
    icd_pattern = re.compile(pattern)

    # First, look for the "Final Answer: " format
    final_answer = re.search(r"Final Answer: (.+)", output_string)

    if final_answer:
        answer_text = final_answer.group(1)
        match = icd_pattern.search(answer_text)
        if match:
            return match.group(0)

    # If not found in "Final Answer:", search the entire output_string
    general_search = icd_pattern.search(output_string)
    if general_search:
        return general_search.group(0)

    return None


icd_code = extract_icd_code(result['result'])

print(f"\n\n\n ICD CODE ---> {icd_code}")
