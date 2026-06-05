# 🧾 Scanify Receipts: Receipt OCR Tracker

A Streamlit-based OCR system that extracts structured data from receipt images using OpenCV and Tesseract OCR.

It supports batch uploads, previews receipts, and extracts store name, date, and total amount automatically.

---

## 📌 Features

- 📷 Upload receipt images in browser
- 🧠 OCR text extraction using Tesseract
- 🧼 Image preprocessing with OpenCV
- 🏪 Store name extraction (heuristic)
- 📅 Date extraction from receipt text
- 💰 Total amount detection
- 📁 Batch processing of multiple receipts
- 📊 CSV export of results
- 📈 OCR confidence scoring system
- 🖼️ Image preview in UI

---

## 🧠 Tech Stack

- Python
- Streamlit
- OpenCV
- pytesseract (OCR engine)
- pandas

---

## 🔄 Pipeline

Image → Preprocessing → OCR → Parsing → Structured Data → CSV Export

---

## 🖥️ How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py