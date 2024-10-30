# RAG-Knowledge-Base
A repository to hold all RAG knowledge that we have.

# Overview

- RAG is a small app scraping django documentation populate vector database and ask questions over that documentation returning answer combined with OpenAI API as a LLM
- Chroma RAG is using ChromDB as vector DB
- Postgres RAG is using PostgreSQL as a vector DB

# Pre-requisites
- virtual environment like pyenv
- Python 3.12.7
- PostgreSQL >= 14

# Installation

### Clone repository

> git clone git@github.com:HackSoftware/RAG-Knowledge-Base.git

### Create virtual environment

> cd RAG-Knowledge-Base
> 
> pyenv install 3.12.7
> 
> pyenv virtualenv 3.12.7 rag_3.12.7
> 
> pyenv activate rag_3.12.7 
> 
> pyenv local rag_3.12.7

### Install dependencies

> pip install -r requirements.txt

### Add OpenAI API key and postgres url

> cp .env.example .env

# Usage

### Populate chroma DB

> python chroma_rag/populate_db.py

### Ask question over django documentation

> python chroma_rag/ask.py

### Populate Postgres DB

> python postgres_rag/populate_postgresql2.py

### Ask question over django documentation

> python postgres_rag/ask.py
