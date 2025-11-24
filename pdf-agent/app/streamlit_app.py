
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer
import faiss

INDEX_DIR = os.path.join('data', 'index')
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, 'faiss.index')
META_PATH = os.path.join(INDEX_DIR, 'meta.json')
CHUNKS_PATH = os.path.join(INDEX_DIR, 'chunks.jsonl')
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'

@st.cache_resource
def load_resources():
    st.write("Chargement du modèle et de l'index...")
    model = SentenceTransformer(MODEL_NAME)
    index = faiss.read_index(FAISS_INDEX_PATH)
    with open(META_PATH, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    chunk_texts = []
    with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            chunk_texts.append(json.loads(line)['text'])
    mapping = meta['mapping']
    return model, index, chunk_texts, mapping

model, index, chunk_texts, mapping = load_resources()

st.title('🔍 Agent PDF Local')
st.write("Posez une question, l'agent va chercher dans vos PDF.")

question = st.text_input('Votre question :', placeholder='Ex: Quelle est la procédure X ?')
top_k = st.slider('Nombre de résultats :', 1, 10, 5)

if st.button('Rechercher') and question.strip():
    q_emb = model.encode([question], normalize_embeddings=True)
    q_emb = np.array(q_emb).astype('float32')
    scores, idxs = index.search(q_emb, top_k)
    idxs = idxs[0]
    scores = scores[0]

    st.subheader('Résultats :')
    for score, i in zip(scores, idxs):
        m = mapping[i]
        st.markdown(f"**Document:** {m['doc_id']} | **Page:** {m['page']} | Score: {score:.4f}")
        st.write(chunk_texts[i])
        st.markdown('---')
