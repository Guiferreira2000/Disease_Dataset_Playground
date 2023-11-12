import os
import openai
from pydub import AudioSegment  # Import the PyDub library
from dotenv import load_dotenv

load_dotenv()  # This will load the .env file

# Input and output file paths
input_file_path = "Datasets/Speech-to-text/metodos.m4a"
output_file_path = "Datasets/Speech-to-text/metodos.wav"

# Convert MP3 to WAV
audio = AudioSegment.from_mp3(input_file_path)
audio.export(output_file_path, format="wav")

openai.api_key = os.getenv("OPENAI_API_KEY")
audio_file = open(output_file_path, "rb")
transcript = openai.Audio.translate("whisper-1", audio_file)
