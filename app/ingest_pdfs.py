
import os, json
import pdfplumber
from pdf2image import convert_from_path
from PIL import Image
import pytesseract

PDF_DIR = os.path.join('data', 'pdfs')
INDEX_DIR = os.path.join('data', 'index')
CHUNKS_PATH = os.path.join(INDEX_DIR, 'chunks.jsonl')
os.makedirs(INDEX_DIR, exist_ok=True)

def normalize_whitespace(text):
    import re
    return re.sub(r'\s+', ' ', text).strip()

def split_into_chunks(text, max_tokens=800, overlap_tokens=100):
    chars_per_token = 4
    max_chars = max_tokens * chars_per_token
    overlap_chars = overlap_tokens * chars_per_token
    text = normalize_whitespace(text)
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        start = end - overlap_chars
        if start < 0: start = 0
        if start >= len(text): break
    return chunks

def extract_page_text(pdf_path, page_number, ocr_lang='fra'):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_number - 1]
        text = page.extract_text()
    if text and text.strip():
        return text
    img = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, dpi=300)[0]
    return pytesseract.image_to_string(img, lang=ocr_lang)

def ingest_all_pdfs():
    rows = []
    for fname in os.listdir(PDF_DIR):
        if not fname.lower().endswith('.pdf'): continue
        pdf_path = os.path.join(PDF_DIR, fname)
        with pdfplumber.open(pdf_path) as pdf:
            num_pages = len(pdf.pages)
        for p in range(1, num_pages + 1):
            text = extract_page_text(pdf_path, p)
            if not text.strip(): continue
            for idx, chunk in enumerate(split_into_chunks(text)):
                rows.append({'doc_id': fname, 'page': p, 'chunk_index': idx, 'text': chunk})
    with open(CHUNKS_PATH, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '
')
    print(f'[OK] {len(rows)} chunks sauvegardés.')

if __name__ == '__main__':
    ingest_all_pdfs()
