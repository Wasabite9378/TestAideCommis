
# -*- coding: utf-8 -*-
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

INDEX_DIR = os.path.join("data", "index")
CHUNKS_PATH = os.path.join(INDEX_DIR, "chunks.jsonl")
FAISS_INDEX_PATH = os.path.join(INDEX_DIR, "faiss.index")
META_PATH = os.path.join(INDEX_DIR, "meta.json")
MODEL_NAME = 'sentence-transformers/all-MiniLM-L6-v2'


def build_faiss_index():
    rows = []
    texts = []
    with open(CHUNKS_PATH, 'r', encoding='utf-8') as f:
        for line in f:
            r = json.loads(line)
            rows.append(r)
            texts.append(r['text'])
    if not rows:
        raise RuntimeError("Aucun chunk trouvé. Lancez app/ingest_pdfs.py d'abord.")

    print("[INFO] Chargement du modèle d'embeddings...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, batch_size=64, show_progress_bar=True, normalize_embeddings=True)
    embeddings = np.array(embeddings).astype('float32')

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, FAISS_INDEX_PATH)
    meta = {
        'dim': dim,
        'count': len(rows),
        'mapping': [{'doc_id': r['doc_id'], 'page': r['page'], 'chunk_index': r['chunk_index']} for r in rows]
    }
    with open(META_PATH, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"[OK] Index FAISS: {FAISS_INDEX_PATH}")
    print(f"[OK] Métadonnées: {META_PATH}")


if __name__ == '__main__':
    build_faiss_index()
