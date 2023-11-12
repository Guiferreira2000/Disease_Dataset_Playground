# https://gpt-index.readthedocs.io/en/latest/index.html
# https://llamahub.ai/

# LLM DOCUMENTATION
#https://gpt-index.readthedocs.io/en/latest/how_to/customization/custom_llms.html


Welcome to LlamaIndex 🦙 !

LlamaIndex (GPT Index) is a project that provides a central interface to connect your LLM’s with external data.

    Github: https://github.com/jerryjliu/llama_index

    PyPi:

            LlamaIndex: https://pypi.org/project/llama-index/.

            GPT Index (duplicate): https://pypi.org/project/gpt-index/.

    Twitter: https://twitter.com/gpt_index

    Discord https://discord.gg/dGcwcsnxhU

Ecosystem

    🏡 LlamaHub: https://llamahub.ai

    🧪 LlamaLab: https://github.com/run-llama/llama-lab

🚀 Overview
Context

    LLMs are a phenomenonal piece of technology for knowledge generation and reasoning. They are pre-trained on large amounts of publicly available data.

    How do we best augment LLMs with our own private data?

    One paradigm that has emerged is in-context learning (the other is finetuning), where we insert context into the input prompt. That way, we take advantage of the LLM’s reasoning capabilities to generate a response.

To perform LLM’s data augmentation in a performant, efficient, and cheap manner, we need to solve two components:

    Data Ingestion

    Data Indexing

Proposed Solution

That’s where the LlamaIndex comes in. LlamaIndex is a simple, flexible interface between your external data and LLMs. It provides the following tools in an easy-to-use fashion:

    Offers data connectors to your existing data sources and data formats (API’s, PDF’s, docs, SQL, etc.)

    Provides indices over your unstructured and structured data for use with LLM’s. These indices help to abstract away common boilerplate and pain points for in-context learning:

            Storing context in an easy-to-access format for prompt insertion.

            Dealing with prompt limitations (e.g. 4096 tokens for Davinci) when context is too big.

            Dealing with text splitting.

    Provides users an interface to query the index (feed in an input prompt) and obtain a knowledge-augmented output.

    Offers you a comprehensive toolset trading off cost and performance.

