
# -*- coding: utf-8 -*-
import os
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import json

PDF_DIR = os.path.join("data", "pdfs")
IMAGES_DIR = os.path.join("data", "images")
INDEX_DIR = os.path.join("data", "index")
CHUNKS_PATH = os.path.join(INDEX_DIR, "chunks.jsonl")

os.makedirs(INDEX_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)


def normalize_whitespace(text: str) -> str:
    import re
    return re.sub(r'\s+', ' ', text).strip()


def split_into_chunks(text: str, max_tokens: int = 800, overlap_tokens: int = 100):
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token
    text = normalize_whitespace(text)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap_chars
        if start < 0:
            start = 0
        if start >= len(text):
            break
    return chunks


def pdf_page_to_image(pdf_path, page_number, poppler_path: str = ""):
    images = convert_from_path(
        pdf_path,
        first_page=page_number,
        last_page=page_number,
        dpi=300,
        poppler_path=poppler_path or None
    )
    return images[0]


def ocr_image(image: Image.Image, lang: str = 'fra'):
    return pytesseract.image_to_string(image, lang=lang)


def extract_page_text(pdf_path, page_number, ocr_lang: str = 'fra', poppler_path: str = ""):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number - 1]
        text = page.extract_text()
    if text and text.strip():
        return text
    try:
        img = pdf_page_to_image(pdf_path, page_number, poppler_path)
        text = ocr_image(img, lang=ocr_lang)
        return text or ""
    except Exception as e:
        print(f"[WARN] OCR impossible sur {os.path.basename(pdf_path)} page {page_number}: {e}")
        return ""


def ingest_all_pdfs(ocr_lang: str = 'fra', poppler_path: str = ""):
    rows = []
    for fname in os.listdir(PDF_DIR):
        if not fname.lower().endswith('.pdf'):
            continue
        pdf_path = os.path.join(PDF_DIR, fname)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
        except Exception as e:
            print(f"[WARN] Impossible d'ouvrir {fname}: {e}")
            continue
        for p in range(1, num_pages + 1):
            page_text = extract_page_text(pdf_path, p, ocr_lang=ocr_lang, poppler_path=poppler_path)
            if not page_text or not page_text.strip():
                continue
            chunks = split_into_chunks(page_text, max_tokens=800, overlap_tokens=100)
            for idx, ch in enumerate(chunks):
                rows.append({
                    'doc_id': fname,
                    'page': p,
                    'chunk_index': idx,
                    'text': ch
                })
    with open(CHUNKS_PATH, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "
")
    print(f"[OK] {len(rows)} chunks sauvegardés dans {CHUNKS_PATH}")


if __name__ == '__main__':
    ingest_all_pdfs()
