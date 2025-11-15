# Text-to-SQL RAG System

## 🚀 Overview

**Text-to-SQL RAG** converts natural-language questions into **accurate MySQL queries** using **semantic retrieval**, **few-shot examples**, and **prompt engineering** to ensure the LLM generates schema-correct SQL without hallucinations.

---
## ▶️ How It Works

1. User asks a **natural-language question**
2. System retrieves the **most relevant example** using semantic similarity (RAG)
3. Schema info + retrieved examples + user query → injected into a prompt
4. Gemini Flash generates a **clean SQL query**
5. The query can be executed against a MySQL database

---

## 🧠 Features

* **Text-to-SQL using RAG (Retrieval-Augmented Generation)**
* **Prompt-engineered SQL generation** with Gemini 2.5 Flash
* **Semantic few-shot retrieval** using HuggingFace embeddings + Chroma
* **Schema-aware prompts** using LangChain’s SQLDatabase
* Outputs **only raw SQL** (no markdown, no explanations)
* LCEL-based modular and extensible pipeline
* Streamlit UI

---

## 📂 Tech Stack

* **LangChain**
* **Gemini 2.5 Flash**
* **HuggingFace Embeddings**
* **Chroma Vector Store**
* **MySQL**
* **Prompt Engineering**
* **Python**
---

## 📌 Example Questions

* *“Show all t-shirts with their discount percentage.”*
* *“How many white color Levi’s t-shirts?”*
* *“Total revenue from each category in 2024.”*

---
