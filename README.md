# 🚀 MCP AI Agent (LLM + MCP API Orchestrator)

An intelligent, production-ready AI agent that understands natural language and dynamically selects & executes backend APIs using LLM reasoning.

> Transform APIs into a self-operating system using AI.

---

## 🔥 Overview

This project replaces traditional hardcoded API flows with an **LLM-driven orchestration engine**.

Instead of writing backend logic for each API, the system allows users to interact in natural language, and the AI handles everything:

- Understands user intent  
- Selects the correct API (tool)  
- Extracts required parameters  
- Asks for missing inputs  
- Executes the API  
- Returns a clean, human-readable response  

---

## 🧠 Core Concept

- APIs = Tools  
- LLM = Decision Engine  
- Backend = Execution Layer  

No hardcoded routing. No manual orchestration.

---

## ⚙️ Architecture

User → FastAPI → Chat Service → LLM → Tool Selection → MCP Client → Backend APIs → Response

---

## ✨ Features

- LLM-driven tool selection (no hardcoding)
- Multi-model support (OpenAI, Gemini, Anthropic)
- Context-aware conversation memory
- Automatic argument extraction
- Dynamic missing field handling (asks user)
- Robust API error handling
- Token-efficient tool catalog filtering
- Full-stack system (FastAPI + React UI)

---

## 🏗️ Tech Stack

- Backend: FastAPI, Python  
- LLM Layer: LangChain  
- Models: OpenAI, Gemini, Anthropic  
- Protocol: MCP (Model Context Protocol)  
- Frontend: React (Vite)  
- Async: httpx, asyncio  

---

## 🚀 Quick Start

1. Clone Repository

git clone https://github.com/niraj080-er/mcp-ai-agent.git  
cd wallet-ai-agent/wallet-agent

---

2. Install Backend Dependencies

pip install -r requirements.txt  

---

3. Setup Environment

Create a `.env` file:

OPENAI_API_KEY=your_key  
GEMINI_API_KEY=your_key  
ANTHROPIC_API_KEY=your_key  

MCP_URL=http://localhost:8087/mcp/  
MCP_AUTH_TOKEN=your_token_here  

---

4. Access

API Docs → http://localhost:8000/docs  
UI → http://localhost:5173  

---

## 🔄 Example

User Input:

Get wallet details for mobile number 1234567890  

System Flow:

1. Detects intent  
2. Selects correct API  
3. Extracts parameters  
4. Calls backend tool  
5. Returns formatted response  

---

## 💡 Example Conversation

User: Show wallet details  
Agent: Please provide mobile number  

User: 1234567890  
Agent: Here are the wallet details...  

---

## 🚀 Why This Project Matters

Traditional backend systems:
- Hardcoded logic  
- Complex API orchestration  
- Difficult to scale  

This system:
- Uses LLM for decision-making  
- Reduces backend complexity  
- Enables natural language API interaction  

---

## 🔥 Key Innovation

APIs are no longer called — they are intelligently selected and executed by AI.

---

## 🧠 Future Improvements

- Tool embeddings for smarter selection  
- LangGraph workflow orchestration  
- Streaming responses  
- Observability (logging & tracing)  
- Authentication & RBAC  

---

## 📬 Contact

If you found this useful or want to collaborate, feel free to connect.

---

⭐ If you like this project, please give it a star!
