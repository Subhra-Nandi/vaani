import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
from faster_whisper import WhisperModel

model = WhisperModel("./models/small", device="cpu", compute_type="int8")

def record_audio(seconds=7, sample_rate=16000):
    print("Recording... (speak after 1 second)")
    import time
    time.sleep(0.5)  # small buffer before capture starts
    audio = sd.rec(int(seconds * sample_rate),
                   samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()
    print("Done.")
    return audio, sample_rate

def transcribe(audio, sample_rate):
    write("/tmp/input.wav", sample_rate, audio)
    segments, info = model.transcribe(
        "/tmp/input.wav",
        language="hi",          # force Hindi
        task="transcribe",      # NOT translate
        beam_size=5,            # better accuracy
        vad_filter=True         # ignore silence
    )
    return " ".join([s.text for s in segments])

if __name__ == "__main__":
    audio, sr = record_audio(seconds=6)
    text = transcribe(audio, sr)
    print(f"Transcribed: {text}")