from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleKeywordTableIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os

os.environ['OPENAI_API_KEY'] = "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"

def createVectorIndex (path):
    max_input = 4096
    tokens = 256
    chunk_size = 600 # Useful to deal with large chunks of code
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap,chunk_size_limit=chunk_size)

    # Define LLM
    llmpredictor = LLMPredictor(llm=OpenAI(temperature=0.1, model_name="text-davinci-003", max_tokens=tokens))

    #Load data
    docs = SimpleDirectoryReader(path).load_data()

    # Create vector index
    vectorindex = GPTSimpleVectorIndex(documents=docs, llm_predictor=llmpredictor, prompt_helper=prompt_helper)
    vectorindex.save_to_disk(f'/home/guilherme/Documents/MDCompass Documentation/json files/Chatgpt/vectorindex.json')
    return vectorindex



vectorindex = createVectorIndex('/home/guilherme/Documents/MDCompass Documentation/json files/Chatgpt/output-onlinefiletools.txt')


def answerMe(vectorindex):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vectorindex)
    while true:
        prompt = input('Please ask: ')
        response = vIndex.query(prompt,response_mode="compact")
        print(f'Response: {response} \n')

answerMe('vectorindex.json')
