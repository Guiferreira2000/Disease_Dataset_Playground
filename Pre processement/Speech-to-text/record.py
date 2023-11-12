import pyaudio
import wave
import threading
import os

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
FILE_PATH = "/home/guilherme/Documents/GitHub/Tese/Disease_Dataset_Playground/Datasets/Speech-to-text/recorded_audio.wav"

audio = pyaudio.PyAudio()

def record_audio(file_path):
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []

    print("Recording... Press Enter to stop.")
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()

    waveFile = wave.open(file_path, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    print(f"Recording saved to: {file_path}")

is_recording = True

if __name__ == "__main__":
    directory = os.path.dirname(FILE_PATH)
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create the directory if it doesn't exist

    record_thread = threading.Thread(target=record_audio, args=(FILE_PATH,))
    record_thread.start()

    input()  # Wait for Enter key press
    is_recording = False
    record_thread.join()

    audio.terminate()
