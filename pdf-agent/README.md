
# Agent PDF Local (FAISS + Streamlit)

Ce projet permet d'ingérer des PDF (avec OCR si nécessaire), de créer un index sémantique local avec FAISS, et de poser des questions via une interface web (Streamlit).

## Structure
```
pdf-agent/
├─ data/
│  ├─ pdfs/        # Déposez vos PDF ici
│  └─ index/       # Index FAISS + métadonnées seront générés ici
├─ app/
│  ├─ ingest_pdfs.py      # Ingestion (PDF -> texte -> chunks.jsonl)
│  ├─ build_index.py      # Construction de l'index FAISS
│  └─ streamlit_app.py    # Interface de recherche
└─ requirements.txt
```

## Prérequis
- Python 3.10+
- Tesseract OCR (pour les PDF scannés)
- Poppler (pour `pdf2image`) 

> Windows: installez Poppler et Tesseract, ajoutez-les au PATH.

## Installation
```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

## Utilisation
1. **Déposez vos PDF** dans `data/pdfs/`.
2. **Ingestion**:
   ```bash
   python app/ingest_pdfs.py
   ```
3. **Indexation**:
   ```bash
   python app/build_index.py
   ```
4. **Interface**:
   ```bash
   streamlit run app/streamlit_app.py
   ```
   Ouvrez http://localhost:8501 et posez vos questions.

## Notes
- L'OCR utilise `pytesseract` avec la langue par défaut `fra`. Modifiez dans `ingest_pdfs.py` si nécessaire.
- Si Poppler/Tesseract ne sont pas dans le PATH, fournissez leurs chemins directement dans votre système.

## Réindexation
- En cas d'ajout de nouveaux PDF, relancez l'ingestion puis l'indexation.

