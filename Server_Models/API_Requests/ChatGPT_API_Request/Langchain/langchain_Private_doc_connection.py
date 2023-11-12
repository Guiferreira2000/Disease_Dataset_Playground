from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
# import magic
import os
# import nltk
from dotenv import load_dotenv

# os.getenv("OPENAI_API_KEY") #  
os.environ['OPENAI_API_KEY'] = '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'

loader = DirectoryLoader('/home/guilherme/Documents/pdfs', glob='**/*.pdf')
print(loader)

# This line of code is creating an instance of the DirectoryLoader class, which is used to load text data from multiple files in a directory.

# The DirectoryLoader constructor takes two arguments:

#     root (required): The root directory from which to load files. In this case, the root directory is ../data/PaulGrahamEssaySmall/, which is a relative path to a directory containing text files.
#     glob (optional): A string specifying a Unix-style glob pattern used to match files in the directory. The pattern **/*.txt means to match all files with the .txt extension in the root directory and its subdirectories.

# The resulting loader object can then be used to load text data from the matched files.

# loader = DirectoryLoader('../data/PaulGrahamEssaySmall/', glob='**/*.txt')
documents = loader.load()
#print(documents)

text_splitter = CharacterTextSplitter(chunk_size=4000, chunk_overlap=1500)
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)


    # For tasks where context is critical and resources are abundant, larger chunks with more overlap might be better.
    # For tasks where speed and resource efficiency are paramount, smaller chunks with minimal overlap might be more appropriate.

texts = text_splitter.split_documents(documents)
#print(texts)

embeddings = OpenAIEmbeddings(openai_api_key=os.environ['OPENAI_API_KEY'])
docsearch = Chroma.from_documents(texts, embeddings)

qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch)

# query = "What did McCarthy concluded?"
# qa.run(query)
# result = qa({"query": query})


# print(result['result'])
# llm=ChartOpenAI()  #Mix between original pipeline data information and outside external information (More powerfull)
qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)
query = "How was implemented LLM in the database?"
result = qa({"query": query})


print(result['result'])
print(result['source_documents'])


# query = "How old is McCarthy when the paper was wrote?"
# result = qa({"query": query})


# print(result['result'])
# print(result['source_documents'])

