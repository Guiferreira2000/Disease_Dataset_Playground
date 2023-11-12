from langchain.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os
from langchain.document_loaders.csv_loader import UnstructuredCSVLoader

os.environ['OPENAI_API_KEY'] = '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'


# Phase 1 - Document loader
file_path = '/home/guilherme/Documents/MDCompass/Machine Learning Implementation/Pre processing/Teste/Disease_Dataset_21_06_2023.csv'
# Load the documents
loader = CSVLoader(file_path=file_path)
data = loader.load()

print(data)


# Phase 2 - Document transformer



