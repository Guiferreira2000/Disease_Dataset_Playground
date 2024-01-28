# 20/01/2024 - Last Version
# https://github.com/openai/whisper

import whisper
import tqdm
import time
import soundfile as sf
import subprocess
import re
import os

def get_audio_duration(path):
    # Use FFmpeg to get the duration of the audio file
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", path]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    duration_str = result.stdout.decode('utf-8').strip()
    # Convert the duration to a number (in seconds)
    duration = float(duration_str) if duration_str else 0
    return duration


path = "/home/guilherme/Documents/Github/Tese/Disease_Dataset_Playground/Datasets/Speech-to-text/metodos.m4a"

model = whisper.load_model("base")

# Get the duration of the audio for the progress bar
audio_duration = get_audio_duration(path)

# Initialize the progress bar
progress_bar = tqdm.tqdm(total=audio_duration, desc='Transcribing', unit='sec')

# Start the transcription in a separate thread or process
import threading

def transcribe():
    result = model.transcribe(path, fp16=False)
    print(f' Language: {result["language"]} \n Text: \n{result["text"]}\n')

    # Replace the audio file extension with .txt for the output file
    text_file_path = os.path.splitext(path)[0] + ".txt"

    # Write the transcription to the text file
    with open(text_file_path, 'w') as text_file:
        text_file.write(f'{result["text"]}')

    progress_bar.n = audio_duration  # Ensure the progress bar completes
    progress_bar.close()


transcribe_thread = threading.Thread(target=transcribe)
transcribe_thread.start()

# Update the progress bar every second
while transcribe_thread.is_alive():
    progress_bar.update(1)  # Update by one second
    time.sleep(1)
