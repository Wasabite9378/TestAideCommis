
# Agent PDF Local pour Streamlit Cloud

Ce projet permet d'ingérer des PDF (avec OCR si nécessaire), de créer un index sémantique local avec FAISS, et de poser des questions via une interface web (Streamlit).

## Déploiement sur Streamlit Cloud
1. Créez un dépôt GitHub avec ces fichiers.
2. Ajoutez vos PDF dans `data/pdfs` (ou via upload si vous adaptez le code).
3. Sur Streamlit Cloud, configurez:
   - Main file path: `app/streamlit_app.py`
   - requirements.txt à la racine
   - packages.txt à la racine (pour OCR)

## Commandes locales (optionnel)
```bash
python app/ingest_pdfs.py
python app/build_index.py
streamlit run app/streamlit_app.py
```
