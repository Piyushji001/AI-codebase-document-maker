# Autonomous Codebase Documenter

An AI-powered full-stack application that automatically generates comprehensive documentation for any GitHub repository using advanced LLMs (Large Language Models).

## 🚀 Features

- **AI-Powered Analysis**: Uses Gemini 2.5 Flash or GPT-4o-mini to understand and document code
- **Full-Stack Architecture**: React frontend, FastAPI backend, Celery workers, and LangGraph AI agents
- **Real-Time Progress**: Live status updates as your documentation is being generated
- **Download Ready**: Get a complete ZIP file with markdown documentation
- **Docker-Based**: Easy setup with Docker Compose

## 🏗️ Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: FastAPI (Python)
- **Worker**: Celery + Redis (Task Queue)
- **AI Agent**: LangGraph + LangChain
- **Storage**: MinIO (S3-compatible)

## 📋 Prerequisites

- Docker Desktop
- Node.js 18+
- Python 3.10+ (for local development)
- API Key for Gemini or OpenAI

## 🛠️ Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd autonomous-codebase-documenter
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
GOOGLE_API_KEY=your_gemini_api_key
# OR
OPENAI_API_KEY=your_openai_api_key
```

### 3. Start Infrastructure

```bash
cd infra
docker-compose up -d
```

This starts:
- Redis (port 6379)
- MinIO (ports 9000, 9001)
- Backend (port 8000)
- Worker (background)
- Agent (port 8001)

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## 🎯 Usage

1. Open `http://localhost:5173` in your browser
2. Paste a GitHub repository URL
3. Click "Generate Documentation"
4. Watch the real-time progress
5. Download the generated documentation ZIP

## 🔑 Getting API Keys

### Google Gemini (Recommended - Free Tier Available)
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create a new project and generate a key

### OpenAI (Fallback)
1. Visit https://platform.openai.com/
2. Go to API Keys section
3. Create a new secret key

## 📦 Project Structure

```
/autonomous-codebase-documenter
├── frontend/          # React + Vite
├── backend/           # FastAPI
├── worker/            # Celery tasks
├── agent/             # LangGraph AI logic
├── infra/             # Docker Compose
└── .env.example       # Environment template
```

## 🧪 Testing

Submit a small public repository first (e.g., a "Hello World" repo) to test the system.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project for learning or portfolio purposes!

## 🙏 Acknowledgments

- Built with LangChain and LangGraph
- Powered by Google Gemini / OpenAI
- UI inspired by modern design principles
