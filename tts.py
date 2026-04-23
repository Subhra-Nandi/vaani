from gtts import gTTS
import subprocess

def speak(text: str, output_path="/tmp/reply.mp3"):
    tts = gTTS(text=text, lang='hi', slow=False)
    tts.save(output_path)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", output_path],
                   capture_output=True)

if __name__ == "__main__":
    speak("नमस्ते! मैं सुन रहा हूँ।")