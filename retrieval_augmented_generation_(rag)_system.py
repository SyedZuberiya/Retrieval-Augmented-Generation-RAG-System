# -*- coding: utf-8 -*-
"""Retrieval-Augmented Generation (RAG) System

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HbWDQV2PgM4-9mf5rFwbrM-zn8jB4CA2
"""

!pip install pymupdf langchain sentence-transformers faiss-cpu transformers torch
!pip install -U langchain-community

import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# For file upload in notebook
try:
    from google.colab import files
    COLAB = True
except ImportError:
    COLAB = False

if not COLAB:
    import ipywidgets as widgets
    from IPython.display import display

def upload_pdf():
    if COLAB:
        print("Upload your PDF file (e.g., sample.pdf):")
        uploaded = files.upload()
        filename = list(uploaded.keys())[0]
        print(f"Uploaded file: {filename}")
        return filename
    else:
        print("Upload your PDF file (e.g., sample.pdf):")
        uploader = widgets.FileUpload(accept='.pdf', multiple=False)
        display(uploader)
        while not uploader.value:
            pass  # Wait until file is uploaded
        for filename in uploader.value:
            content = uploader.value[filename]['content']
            with open(filename, 'wb') as f:
                f.write(content)
            print(f"Uploaded file: {filename}")
            return filename

# 1. Load & chunk documents (single PDF)
def load_pdf(file_path):
    doc = fitz.open(file_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()
    return full_text

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# 2. Embed chunks using sentence-transformers
def embed_chunks(chunks, model_name="all-MiniLM-L6-v2"):
    embedder = SentenceTransformer(model_name)
    embeddings = embedder.encode(chunks, convert_to_numpy=True)
    # Normalize embeddings
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings, embedder

# 3. Build FAISS vector store
def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  # Using Inner Product for normalized vectors
    index.add(embeddings)
    return index

# 4. Retrieve similar chunks by query
def retrieve(query, embedder, index, chunks, top_k=3):
    query_vec = embedder.encode([query], convert_to_numpy=True)
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)
    distances, indices = index.search(query_vec, top_k)
    results = [(chunks[i], distances[0][idx]) for idx, i in enumerate(indices[0])]
    return results

# 5. Load a more advanced causal LM from transformers (CPU/GPU)
def load_llm(model_name="gpt2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model

# 6. Generate answer conditioned on retrieved chunks + user query
def generate_answer(query, retrieved_chunks, tokenizer, model, max_new_tokens=150):
    context = "\n\n".join([f"Source chunk:\n{chunk}" for chunk, _ in retrieved_chunks])
    prompt = (
        f"Use the following context to answer the question.\n"
        f"Cite the source chunks explicitly in your answer.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n"
        f"Answer:"
    )

    inputs = tokenizer.encode(prompt, return_tensors="pt")

    # Generate with no_grad context for efficiency
    with torch.no_grad():
        outputs = model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id,
        )
    answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return answer.split("Answer:")[-1].strip()

def main():
    filename = upload_pdf()  # Upload your PDF interactively

    print("Loading and chunking document...")
    text = load_pdf(filename)
    chunks = chunk_text(text)
    print(f"Number of chunks: {len(chunks)}")

    print("Embedding chunks...")
    embeddings, embedder = embed_chunks(chunks)
    index = build_faiss_index(embeddings)

    print("Loading LLM model...")
    tokenizer, model = load_llm()

    while True:
        query = input("\nEnter your question (or 'exit' or 'quit' to quit): ")
        if query.lower() in ['exit', 'quit']:
            break

        retrieved = retrieve(query, embedder, index, chunks)
        print("\nTop retrieved chunks:")
        for i, (chunk, dist) in enumerate(retrieved):
            print(f"[{i+1}] (Similarity Score: {dist:.4f}): {chunk[:200]}...\n")

        answer = generate_answer(query, retrieved, tokenizer, model)
        print("\nGenerated answer:")
        print(answer)

        print("\nCited source chunks:")
        for i, (chunk, score) in enumerate(retrieved):
            print(f"[{i+1}] (Score: {score:.4f}): {chunk[:300]}...\n")

if __name__ == "__main__":
    main()