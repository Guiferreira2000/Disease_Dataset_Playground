# 20/01/2024 - Last Version
# https://github.com/openai/whisper

import whisper


path= "/home/guilherme/Documents/Github/Tese/Disease_Dataset_Playground/Datasets/Speech-to-text/recorded_audio20231005.m4a"
path= "/home/guilherme/Documents/Github/Tese/Disease_Dataset_Playground/Datasets/Speech-to-text/metodos.m4a"

model = whisper.load_model("base")
result = model.transcribe(path, fp16=False)
print(f' Language: {result["language"]} \n Text: \n{result["text"]}')

