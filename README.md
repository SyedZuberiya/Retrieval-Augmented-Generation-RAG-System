# 🔍📄 Retrieval-Augmented Generation (RAG) System

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that allows users to interactively query PDF documents using natural language. It combines dense vector retrieval and generative language models to produce accurate, context-aware answers.

---

## 📌 Overview

**RAG** is a hybrid NLP system that first retrieves relevant chunks of information from a document (retrieval) and then generates a response (generation) using a language model. This is ideal for applications like:

- Question answering over documents
- Conversational agents based on private data
- Context-aware document summarization

---

## 🚀 Features

✅ PDF text extraction using `PyMuPDF`  
✅ Chunking with `langchain`’s `RecursiveCharacterTextSplitter`  
✅ Semantic embedding generation via `sentence-transformers`  
✅ Similarity search using `FAISS`  
✅ Answer generation using HuggingFace transformer models (`GPT-2` or any causal LM)  
✅ Interactive CLI/chat-based interface  

---

## 🛠️ Technologies Used

| Tool/Library           | Purpose                                       |
|------------------------|-----------------------------------------------|
| `PyMuPDF (fitz)`       | Extract text from PDF files                   |
| `langchain`            | Text splitting and preprocessing              |
| `sentence-transformers`| Embedding text into vector space              |
| `faiss-cpu`            | Vector similarity search for retrieval        |
| `transformers`         | Pretrained language models (e.g., GPT-2)      |
| `torch`                | Backend for transformer-based models          |
| `ipywidgets`           | PDF upload support in Jupyter notebooks       |

---

**Results**
![image](https://github.com/user-attachments/assets/f7b90d8a-b13d-4cdb-8b9d-e7877b93d1ad)
![image](https://github.com/user-attachments/assets/dbbb35f0-6c93-4ab4-a0df-753fa81fe8dc)
![image](https://github.com/user-attachments/assets/ad6f6b74-9bf3-4f61-8455-c5e2f530f2e3)

## 📁 Project Structure

├── chatbot.py # Main RAG system implementation
├── requirements.txt # Dependencies
└── README.md # Project overview and usage

👤 Author
Developed by Syeda Zuberiya
