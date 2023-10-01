from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import openai
import re

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the path to your file
file_path = 'Datasets/step_3/icd_11_GPT_formated_data_v2.json'
# file_path = 'Datasets/step_3/icd_11_formated_data.json'


# Load the data from the file
data = json.loads(Path(file_path).read_text())

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

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

# Convert the JSON data to a list of Document instances
documents = [Document(json.dumps(entry), {}) for entry in data]

# Print the first two documents to verify
# print(documents[0].page_content)
# print(documents[1].page_content)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(documents, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)

# Define the initial data observation
df_head = "\n".join([json.dumps(entry) for entry in data[:5]])
# df_head = "\n".join([json.dumps({key: data[key]}) for key in list(data.keys())[:5]])

symptom = input("Type symptom")
# Define the question you want to answer
input_question = f"Which code is more closely associated with {symptom}?"
# Create the prompt for the API call
api_prompt = f'''
You are analyzing a dataset of medical symptoms and their associated ICD 11 Codes. The dataset is formatted as a list of dictionaries, where each dictionary contains:

1. "ICD 11 Code": Represents the unique code for a medical condition.
2. "Symptom": Describes a symptom associated with that medical condition.

Sample data from the dataset:
{df_head}

Given a symptom, your task is to determine the associated ICD 11 Code.

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

icd_code = extract_icd_code(result['result']) 

if icd_code:
    print(icd_code)
else:
    print("No ICD code found!")