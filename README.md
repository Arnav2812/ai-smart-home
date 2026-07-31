# ⚡ AI-Driven Smart Home NLP Engine
> **Decoupled LLM Intent Routing & Context Engineering Guardrail Dashboard**  
> An enterprise-grade, low-latency AI edge control system that translates unstructured natural language into validated, executable IoT device commands with real-time state synchronization and OpenTelemetry observability.

---

## 📸 Dashboard Overview

![AI Smart Home Dashboard](https://raw.githubusercontent.com/Arnav2812/ai-smart-home/main/docs/dashboard-preview.png)

---

## 🏗️ System Architecture

```text
                                +-----------------------+
                                |   React / Vite Dashboard |
                                +-----------+-----------+
                                            |
                                            | HTTP POST /api/parse-command
                                            v
                                +-----------+-----------+
                                |    FastAPI Gateway    |
                                +-----+-----------+-----+
                                      |           |
           +--------------------------+           +--------------------------+
           |                                                                 |
           v                                                                 v
+--------------+--------------+                                   +--------------+--------------+
|   Groq Cloud (Llama 3)     |                                   |  Local Context Guardrails   |
| Structured JSON Parsing     |                                   |  Topology & Capability Rules|
+--------------+--------------+                                   +--------------+--------------+
|                                                                 |
+--------------------------+           +--------------------------+
|           |
v           v
+-----------+-----------+
|   Device Manager State|
|    (IoT Local Engine) |
+-----------+-----------+
|
v
+-----------+-----------+
| OpenTelemetry Spans  |
| (Trace & Latency Log) |
+-----------------------+
```

---

## 🔥 Key Features

* **Decoupled LLM Intent Processing**: Uses **Groq Cloud (Llama 3)** to parse multi-intent natural language queries into structured `JSON` payloads via **Pydantic** validation models.
* **Context Engineering & Safety Guardrails**: Prevents LLM hallucinations or destructive commands by filtering parsed intents through a local topology and capability matrix (`DeviceManager`).
* **Real-Time State Synchronization**: React frontend mirrors physical state changes across lights, audio monitors, thermostats, and other edge devices instantly.
* **OpenTelemetry Observability**: End-to-end tracing across pipeline stages to isolate cloud LLM latency (~200ms) from local guardrail validation latency (~1ms).
* **Adversarial Input Handling**: Gracefully handles ambiguous, out-of-scope, or illogical user commands without crashing the system.

---

## 🛠️ Tech Stack

| Domain | Technology |
| :--- | :--- |
| **Backend Framework** | Python 3.10+, FastAPI, Uvicorn |
| **AI / LLM Integration** | Groq SDK, Llama 3 (8B Instruct), Pydantic |
| **Frontend Framework** | React 18, Vite, Lucide Icons, CSS3 Modern Flex/Grid |
| **Observability** | OpenTelemetry SDK, FastAPI Auto-Instrumentation |
| **Tooling & Environment** | Python-Dotenv, Git, PowerShell |

---

## 📂 Project Structure

```text
ai-smart-home/
├── backend/
│   ├── main.py                   # FastAPI Application & OTel Setup
│   ├── llm_service.py            # Groq Llama 3 Structured Parser
│   ├── device_manager.py         # Context Guardrails & Topology Matrix
│   ├── requirements.txt          # Python Dependencies
│   └── .env                      # API Credentials (GROQ_API_KEY)
└── frontend/
    ├── index.html                # Entry Point HTML
    ├── vite.config.js            # Vite Configuration
    ├── package.json              # Frontend Dependencies
    └── src/
        ├── main.jsx              # React Root Mount
        └── App.jsx               # Dashboard UI & State Handler
```

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10+
* Node.js 18+ & npm
* A Groq API Key (Free tier available at console.groq.com)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows:
.env\Scriptsctivate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file and add your Groq API Key
echo "GROQ_API_KEY=your_actual_groq_api_key_here" > .env

# Run the FastAPI server
uvicorn main:app --reload
```
*The backend API will be available at http://localhost:8000. API documentation is accessible at http://localhost:8000/docs.*

### 3. Frontend Setup

```bash
# Navigate to frontend directory (from project root)
cd frontend

# Install Node modules
npm install

# Start Vite development server
npm run dev
```
*Open your browser and navigate to http://localhost:5173.*

---

## 🧪 Example API Request & Pipeline Flow

**Input Request (POST `/api/parse-command`)**

```json
{
  "prompt": "Dim the studio lights to 30% and play Drake on speakers"
}
```

**1. Structured LLM Output (Pydantic Scheme)**

```json
{
  "reasoning": "Parsed light brightness adjustment and audio playback request.",
  "parsed_successfully": true,
  "commands": [
    {
      "device_id": "studio_lights",
      "action": "set_brightness",
      "parameters": { "brightness": 30 }
    },
    {
      "device_id": "studio_audio",
      "action": "play_music",
      "parameters": { "track": "Drake" }
    }
  ]
}
```

**2. Guardrail Validation Result**

```json
[
  {
    "device_id": "studio_lights",
    "status": "EXECUTED",
    "message": "Executed 'set_brightness' on 'Studio Lights'."
  },
  {
    "device_id": "studio_audio",
    "status": "EXECUTED",
    "message": "Executed 'play_music' on 'Studio Audio Monitors'."
  }
]
```

---

## 📊 OpenTelemetry Console Output Sample

When requests process through the system, custom OTel spans dump latency breakdowns to standard output:

```json
{
    "name": "llm_intent_parsing",
    "context": {
        "trace_id": "0x8f2d1e0129a8b...",
        "span_id": "0x1a2b3c4d..."
    },
    "attributes": {
        "user.prompt": "Dim the studio lights to 30%",
        "llm.parsed_successfully": true,
        "llm.command_count": 1
    },
    "duration_ms": 218.4
}
```

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.
