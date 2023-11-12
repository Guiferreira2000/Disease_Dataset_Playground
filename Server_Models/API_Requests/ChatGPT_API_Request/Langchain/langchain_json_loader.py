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
# !pip install langchain watermark openai jq

os.environ['OPENAI_API_KEY'] = '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'
file_path = "/home/guilherme/Documents/MDCompass/Machine Learning Implementation/Pre processing/Teste/Sorted_Diseases.json"
# file_path = "/home/guilherme/Documents/Tachovia_1Tacho/TACOVIA_Versoes/Versao_atual/V_05_06_2023/tacovia-platform-bo/SourceCode/package.json"
# file_path = "/home/guilherme/Downloads/package.json"


# Prints the json file (Not important, just an example)
data = json.loads(Path(file_path).read_text())
# pprint(data)




# Define the metadata extraction function.
def metadata_func(record: dict, metadata: dict) -> dict:

    metadata["classification"] = record.get("classification")
    metadata["timestamp_ms"] = record.get("timestamp_ms")

    return metadata


# loader = JSONLoader(
#     file_path='./example_data/facebook_chat.json',
#     jq_schema='.diseases[]',
#     content_key="symptoms",
#     metadata_func=metadata_func
# )


loader = JSONLoader(
    file_path= file_path,
    jq_schema='.diseases[]')   # jq_schema='.diseases[].symptom   



data_1 = loader.load()
# print(data_1[1])

pprint(data_1)


text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=1)
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

texts = text_splitter.split_documents(data_1)
#print(texts)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(texts, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch)

query = "I want you to assign a random number to each disease in the dataset. The dataset has 300 diseases?"
qa.run(query)
result = qa({"query": query})


print(result['result'])

# llm=ChartOpenAI()  #Mix between original pipeline data information and outside external information (More powerfull) 
# qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
# query = "Qual é o tempo máximo de trabalho semanal?"
# result = qa({"query": query})


# print(result['result'])
# print(result['source_documents'])