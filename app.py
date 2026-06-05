import streamlit as st
import cv2
import pytesseract
import numpy as np
import pandas as pd
import re
from PIL import Image
import os

# If Windows: else can be omitted
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(img):
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # FIX
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    return thresh


def extract_text(img):
    processed = preprocess_image(img)
    return pytesseract.image_to_string(processed)


def extract_store(text):
    lines = text.split("\n")
    return lines[0] if lines else "Unknown Store"


def extract_date(text):
    match = re.search(r"\d{2}[/-]\d{2}[/-]\d{2,4}", text)
    return match.group() if match else "Unknown Date"


def extract_total(text):
    matches = re.findall(r"\$?\d+\.\d{2}", text)
    return matches[-1] if matches else "Not Found"


def save_csv(data):
    df = pd.DataFrame([data])
    file_exists = os.path.isfile("output.csv")
    df.to_csv("output.csv", mode="a", header=not file_exists, index=False)

def confidence_score(text):
    score = 0

    if len(text) > 50:
        score += 30
    if any(char.isdigit() for char in text):
        score += 30
    if "$" in text:
        score += 20
    if "total" in text.lower():
        score += 20

    return min(score, 100)


st.title("Scanify Receipts")

uploaded_files = st.file_uploader(
    "Upload Receipt Images",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    results = []

    for file in uploaded_files:
        image = Image.open(file)

        st.image(image, caption=f"Uploaded: {file.name}", use_container_width=True)

        text = extract_text(image)

        confidence = confidence_score(text)
        st.progress(confidence / 100)
        st.write(f"🔍 OCR Confidence: {confidence}%")

        store = extract_store(text)
        date = extract_date(text)
        total = extract_total(text)

        data = {
            "file": file.name,
            "store": store,
            "date": date,
            "total": total,
            "confidence": confidence
        }

        results.append(data)
        save_csv(data)

        st.subheader(file.name)
        st.text(text)
        st.json(data)

    st.success("Processing complete! Saved to output.csv")
    st.dataframe(pd.DataFrame(results))

