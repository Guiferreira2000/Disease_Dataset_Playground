Welcome to LangChain

LangChain is a framework for developing applications powered by language models. We believe that the most powerful and differentiated applications will not only call out to a language model via an API, but will also:

    Be data-aware: connect a language model to other sources of data

    Be agentic: allow a language model to interact with its environment

The LangChain framework is designed with the above principles in mind.

This is the Python specific portion of the documentation. For a purely conceptual guide to LangChain, see here. For the JavaScript documentation, see here. 
 
# https://python.langchain.com/en/latest/index.html


Video tutorial
# https://www.youtube.com/watch?v=EnT-ZTrcPrg&t=3s

Documentação

# https://github.com/imClumsyPanda/langchain-ChatGLM/blob/master/README_en.md

Json Loader
# https://python.langchain.com/docs/modules/data_connection/document_loaders/how_to/json

# Common JSON structures with jq schema

    JSON        -> [{"text": ...}, {"text": ...}, {"text": ...}]
    jq_schema   -> ".[].text"

    JSON        -> {"key": [{"text": ...}, {"text": ...}, {"text": ...}]}
    jq_schema   -> ".key[].text"

    JSON        -> ["...", "...", "..."]
    jq_schema   -> ".[]"



CSV Loader

Documentation:

# https://github.com/samwit/langchain-tutorials/blob/main/YT_Talk_to_CSV_%26_Excel_Files_with_LangChain.ipynb

# https://www.youtube.com/watch?v=xQ3mZhw69bc

