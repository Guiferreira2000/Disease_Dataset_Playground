from langchain.llms import OpenAI
from langchain import PromptTemplate, LLMChain
from langchain.callbacks import get_openai_callback
import os

os.environ['OPENAI_API_KEY'] = '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'

template = """Question: {question}

Answer: Let's think step by step."""


prompt = PromptTemplate(template=template, input_variables=["question"])

llm = OpenAI(model_name='text-davinci-003', 
             temperature=0.9, 
             max_tokens = 256)

text = 'Tell me things about MJ?'

llm_chain = LLMChain(prompt=prompt, llm=llm)

question = "What NFL team won the Super Bowl in the year Justin Beiber was born?"


# Anything inside the context manager will get tracked. Here's an example of using it to track multiple calls in sequence.
with get_openai_callback() as cb:
  # Method 1
    llm_result = llm(text)
    print(llm_result)
  # Method 2
    Answer = llm_chain.run(question)
    print(Answer)

    print(cb)