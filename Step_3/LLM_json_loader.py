from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI, VectorDBQA
import os
import json
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the path to your file
file_path = 'Datasets/step_3/icd_11_GPT_formated_data.json'

# Load the data from the file
data = json.loads(Path(file_path).read_text())

class Document:
    def __init__(self, page_content, metadata):
        self.page_content = page_content
        self.metadata = metadata

# Convert the JSON data to a list of Document instances
documents = [Document(json.dumps(entry), {}) for entry in data]

# Print the first two documents to verify
print(documents[0].page_content)
print(documents[1].page_content)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(documents, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)

# Define the initial data observation
df_head = "\n".join([json.dumps(entry) for entry in data[:5]])

# Define the question you want to answer
input_question = "Which code is more closely associated with Pus-like discharge?"

# Create the prompt for the API call
api_prompt = f'''
You are working with a JSON dataset in Python. The dataset is structured as a list of dictionaries. Each dictionary has two key-value pairs:

1. "ICD 11 Code": Represents a unique code for a medical condition.
2. "Symptom": Describes a symptom associated with that medical condition.

For example:
{df_head}

Your task is to identify if there are any redundant synonyms in the dataset that are associated with different ICD 11 Codes.

You always have to use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [python_repl_ast]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!
Question: {input_question}
'''

# query = "Its not suposed to have the same or similar synonyms associated with different codes. The labelling must not be redundant. Try to identify redundant synonyms"

result = qa({"query": api_prompt})

print(result['result'])