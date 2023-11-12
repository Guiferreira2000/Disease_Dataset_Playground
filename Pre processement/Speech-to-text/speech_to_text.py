import whisper
import subprocess
import re  # Import the regular expression module

model = whisper.load_model("base")
model = model.float()

# load audio and pad/trim it to fit 30 seconds
audio_1 = "Datasets/Speech-to-text/sample-0.mp3"
audio_2 = "Datasets/Speech-to-text/metodos.mp3"
audio_3 = "Datasets/Speech-to-text/recorded_audio.wav"

audio = whisper.load_audio(audio_3)
audio = whisper.pad_or_trim(audio)

# make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio).float().to(model.device)

# detect the spoken language
_, probs = model.detect_language(mel)
print(f"Detected language: {max(probs, key=probs.get)}")

# decode the audio
options = whisper.DecodingOptions(fp16=False)
result = whisper.decode(model, mel, options)

# print the recognized text
print(result.text)

# Translate the audio file if necessary
def translate_audio(audio_path):
    command = [
        'whisper',
        audio_path,
        '--language', 'Portuguese',  # Replace 'Japanese' with the detected or known language
        '--task', 'translate'
    ]

    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return result.stdout

# Translate the audio file
translation_result = translate_audio(audio_3)

# New code to remove timestamps
translation_text_only = re.sub(r'\[\d+:\d+\.\d+ --> \d+:\d+\.\d+\]  ', '', translation_result)
print(translation_text_only)
