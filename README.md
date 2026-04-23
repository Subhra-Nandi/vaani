# 🎙️ Vaani — Hindi Voice Assistant for Student Re-engagement

Vaani is an AI-powered Hindi voice assistant that listens to user speech, understands intent, manages conversation flow, and responds with natural Hindi speech.

This project simulates a real-world conversational AI pipeline with speech recognition, dialogue management, LLM-based reasoning, and voice synthesis.

---

## 🚀 Features

* 🎤 Speech-to-Text using Whisper (CPU)
* 🔊 Hindi Text-to-Speech using Coqui TTS
* 🌐 Language Detection (Lingua)
* 🧠 Dialogue Manager (State Machine)
* 🤖 LLM-based Objection Handling (Ollama)
* 🗂️ Redis Session Memory
* 🔁 End-to-End Voice Interaction Loop
* ⚡ FastAPI Backend for API access

---

## 🏗️ Project Structure

```bash
vaani/
├── stt.py
├── tts.py
├── lang_detect.py
├── session.py
├── dialogue.py
├── llm_handler.py
├── main.py
├── api.py
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧠 System Flow

```text
Mic Input
   ↓
Whisper STT
   ↓
Language Detection
   ↓
Dialogue Manager (State Machine)
   ↓
LLM (Ollama, if needed)
   ↓
Coqui TTS
   ↓
Speaker Output
```

---

## ⚙️ Setup (WSL2 Recommended)

### 1. Install WSL2 (Windows)

```bash
wsl --install
```

---

### 2. Open Ubuntu & Install System Dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg portaudio19-dev docker.io curl git
```

---

### 3. Get the Project

#### Option A — Clone from GitHub (Recommended)

```bash
git clone https://github.com/Subhra-Nandi/vaani.git
cd vaani
```

#### Option B — Copy from Windows (if already created locally)

```bash
# Find your Windows username
ls /mnt/c/Users

# Replace <windows-username> with your system username
cp -r /mnt/c/Users/<windows-username>/path/to/vaani ~/
cd ~/vaani
```

---

### 4. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 5. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 6. Start Redis (Docker)

```bash
sudo service docker start
docker run -d -p 6379:6379 --name redis redis:alpine
```

---

### 7. Install & Run Ollama (LLM)

```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
```

Open a new terminal:

```bash
ollama pull llama3.2:1b
```

---

## ▶️ Running the Application

### 🎤 Run Full Voice Assistant

```bash
python3 main.py
```

---

### 🌐 Run API Server

```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

Open in browser:

```text
http://localhost:8000/docs
```

---

## ⚠️ Notes

* Microphone support in WSL may be limited → use `.wav` input if needed
* Whisper runs on CPU → slower but stable
* Ensure Redis and Ollama are running before starting
* Audio playback uses `ffplay` in WSL

---

## 🧪 Example Interaction

```text
User: mujhe padhai mein help chahiye
Bot: Aapne Fractions complete nahi kiya...
User: nahi time nahi hai
Bot: (LLM handles objection in Hindi)
```

---

## 🔮 Future Improvements

* 📞 Telephony integration (Twilio)
* ⚡ Real-time streaming audio
* 🌍 Multi-language expansion
* ☁️ Cloud deployment
* 📊 Analytics dashboard

---

## 🛠️ Tech Stack

* Python
* Faster-Whisper
* Coqui TTS
* Lingua
* Redis
* Ollama
* FastAPI
* Docker

---

## 👨‍💻 Author

Subhra Nandi

---

## ⭐ Learning Focus

* Conversational AI systems
* Dialogue state machines vs LLMs
* Speech pipelines
* Scalable system design

---
