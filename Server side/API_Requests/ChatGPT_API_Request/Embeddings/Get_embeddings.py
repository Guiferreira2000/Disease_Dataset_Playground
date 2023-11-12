# https://github.com/openai/openai-cookbook/blob/main/examples/Obtain_dataset.ipynb

# imports
import openai
openai.api_key = "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"

# list models
models = openai.Model.list()

# print the first model's id
print(models.data[0].id)



import pandas as pd
import tiktoken

from openai.embeddings_utils import get_embedding

# embedding model parameters
embedding_model = "text-embedding-ada-002"
embedding_encoding = "cl100k_base"  # this the encoding for text-embedding-ada-002
max_tokens = 8000  # the maximum for text-embedding-ada-002 is 8191



def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

df['ada_embedding'] = df.combined.apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
df.to_csv('/home/guilherme/Downloads/Reviews_with_embeddings_1k.csv', index=False)



import pandas as pd

df = pd.read_csv('/home/guilherme/Downloads/Reviews_with_embeddings_1k.csv')
df['ada_embedding'] = df.ada_embedding.apply(eval).apply(np.array)
