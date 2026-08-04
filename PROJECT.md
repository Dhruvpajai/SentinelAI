# SentinelAI

## Project Goal
SentinelAI is an AI security middleware that detects and blocks prompt injection, jailbreak attempts, system prompt extraction, role manipulation, and other malicious prompts before they reach an LLM. It also analyzes LLM responses to prevent sensitive information leakage.

## Tech Stack
- Python
- FastAPI
- Streamlit
- Sentence Transformers (MiniLM)
- XGBoost
- SQLAlchemy
- SQLite
- PyTorch
- scikit-learn

## Architecture
User
↓
FastAPI Backend
↓
Prompt Firewall
↓
LLM Adapter
↓
Response Firewall
↓
Streamlit Dashboard

## Development Rules
- Use clean architecture.
- Keep modules small and reusable.
- Use Python type hints.
- Follow PEP8.
- Avoid unnecessary dependencies.
- Do not implement future features unless requested.
- Keep code production-ready.

## Current Milestone
Milestone 1:
Create the backend foundation with FastAPI.