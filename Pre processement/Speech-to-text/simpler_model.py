import whisper
import time
from tqdm import tqdm
import librosa  # for audio file duration

# Load the Whisper model
model = whisper.load_model("base")

# Define the audio file and output file
audio_1 = "Datasets/Speech-to-text/sample-0.mp3"
audio_2 = "Datasets/Speech-to-text/metodos.mp3"
audio_3 = "Datasets/Speech-to-text/recorded_audio.wav"
audio_file = "Datasets/Speech-to-text/Entrevista_2.m4a"
output_file = "Datasets/Speech-to-text/Entrevista_2.txt"

# Determine the duration of the audio file (in seconds)
duration = librosa.get_duration(filename=audio_file)

# Estimated transcription speed factor (you might need to adjust this based on your observations)
speed_factor = 0.5  # example: 0.5x means half the duration of the audio

# Initialize the progress bar
with tqdm(total=duration) as pbar:
    # Start the transcription process in a background thread (or process)
    # NOTE: This is a simplified representation. Actual implementation may require threading or multiprocessing.
    result = model.transcribe(audio_file)

    # Simulate progress bar update (assuming linear progress)
    for _ in range(int(duration * speed_factor)):
        time.sleep(1)  # Sleep for a second
        pbar.update(1/speed_factor)  # Update the progress bar

# Save the result to a file
with open(output_file, "w") as file:
    file.write(result["text"])

print(f"Transcription completed and saved to '{output_file}'")
