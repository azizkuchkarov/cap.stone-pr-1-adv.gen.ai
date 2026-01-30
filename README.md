---
title: Rag Support Capstone
emoji: 🚀
colorFrom: red
colorTo: red
sdk: docker
app_port: 7860
pinned: false
---
# Capstone Project 1 — RAG Customer Support (Python + Streamlit)

## Objective
Build a Customer Support solution able to answer questions from datasources and raise support tickets.

## Features
- Web chat UI (Streamlit)
- Retrieval Augmented Generation (RAG) over 3+ documents
- Supports PDFs (including 400+ page manuals)
- Answers include citations: file name + page number
- Conversation history maintained in context window
- Function calling: creates support tickets via tool call
- Issue tracking integration: GitHub Issues

## Data Requirements
Place documents in `data/raw/`:
- At least 3 documents
- At least 2 PDFs
- At least 1 PDF with 400+ pages

## Setup (Local)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
