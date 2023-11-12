# https://www.youtube.com/watch?v=sUSw9MaPm2M


# Documentation:
 # https://gpt-index.readthedocs.io/en/latest/index.html
 # https://pypi.org/project/gpt-index/

import os

os.environ['OPENAI_API_KEY'] = "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"



# Load you data into 'Documents' a custom type by LlamaIndex

from llama_index import SimpleDirectoryReader

documents = SimpleDirectoryReader('./data').load_data()
print(documents)



# Create an index of your documents

from llama_index import GPTSimpleVectorIndex

index = GPTSimpleVectorIndex(documents)
print(documents)


# Query your index!

response = index.query("What do you think of Facebook's LLaMa?")
print(response)



# Setup your LLM

from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper, GPTKeywordTableIndex
from langchain import OpenAI

# define LLM
llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="text-davinci-002"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

# # build index
# index = GPTKeywordTableIndex.from_documents(documents, service_context=service_context)

# # get response from query
# response = index.query("What did the author do after his time at Y Combinator?")
# print(response)

# define prompt helper
# set maximum input size
max_input_size = 4096
# set number of output tokens
num_output = 256
# set maximum chunk overlap
max_chunk_overlap = 20
prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)

custom_LLM_index = GPTSimpleVectorIndex(
    documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
)



###############
# Wikipedia Example
###############

from llama_index import download_loader

WikipediaReader = download_loader("WikipediaReader")

loader = WikipediaReader()
wikidocs = loader.load_data(pages=['Cyclone Freddy'])

# https://en.wikipedia.org/wiki/Cyclone_Freddy


wiki_index = GPTSimpleVectorIndex(wikidocs)



response = wiki_index.query("What is cyclone freddy?")
print(response)

