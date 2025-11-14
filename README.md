# Rag_chat
## Code Generation API with Retrieval-Augmented Evaluation
This project implements a Retrieval-Augmented Code Generation pipeline using FastAPI, FAISS, HuggingFace embeddings, and a pluggable code-generation module.
It supports:

Document ingestion
Vectorstore indexing
Question answering
Code generation (/generate_code endpoint)
Automated evaluation with pass@k metrics

# Features

##Retrieval-Augmented Generation (RAG)

Documents can be uploaded via /upload
Text is embedded using all-MiniLM-L6-v2
Stored & retrieved using FAISS

## Code Generation API

/generate_code endpoint generates Python code based on task description
Easy to switch between fallback generator and LLM-based generator

## API Server (FastAPI)

-Interactive UI available at:
 http://127.0.0.1:8000/docs

- Automated Evaluation Framework
Evaluates the generator across multiple tasks
Executes generated code against unit tests

Computes:
pass_ratio
pass@1
pass@3
pass@5

latency stats
Results stored in eval_results.json

# Project Structure
```text
chat_x/
│
├── main.py                      # FastAPI application (API endpoints + routing)
├── agent.py                     # RAG pipeline + code generation logic
├── models.py                    # Database models (SQLAlchemy + SQLite)
├── init_db.py                   # Database initialization script
│
├── run_evaluation.py            # Automated evaluation script (pass@k, unit tests)
│
├── tests/                       # Evaluation dataset & unit tests
│   ├── eval_prompts.jsonl       # Prompts + test script mapping
│   ├── test_add.py              # Unit tests for add()
│   ├── test_reverse.py          # Unit tests for reverse_string()
│   └── test_max.py              # Unit tests for find_max()
│
└── generated_code.py            # Auto-generated file during evaluation
```

# Start the server:
uvicorn main:app --reload

# Open Swagger UI:
http://127.0.0.1:8000/docs

# How to Run Evaluation
python run_evaluation.py
            |
Calls /generate_code
Saves generated code as generated_code.py
Runs the corresponding unit tests
Computes pass@k metrics
Saves everything in eval_results.json

# Evaluation Results
pass_ratio: 1.0
pass@1: 3/3 = 1.000
pass@3: 3/3 = 1.000
pass@5: 3/3 = 1.000
Mean pass_ratio@n: 1.0
