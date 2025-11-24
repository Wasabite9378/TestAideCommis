
# Déploiement Agent PDF sur Streamlit Cloud

## Étapes
1. Créez un dépôt GitHub avec ces fichiers.
2. Sur Streamlit Cloud :
   - Main file path : `streamlit_app.py` (racine)
   - requirements.txt et packages.txt à la racine
3. Ajoutez vos PDF dans `data/pdfs` via GitHub.
4. Lancez l'app :
   - Ingestion : `python app/ingest_pdfs.py`
   - Indexation : `python app/build_index.py`
   - Interface : Streamlit Cloud

## Notes
- OCR activé (Tesseract + Poppler via packages.txt)
- Pour simplifier, utilisez guillemets doubles dans le code.
