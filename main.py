import os
from flask import Flask, request, render_template
from transformers import pipeline
import fitz

app = Flask(__name__)

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e", max_position_embeddings=1024)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""
    if 'text' in request.form:
        text = request.form['text']
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            text = extract_text_from_pdf(file)

    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return render_template('index.html', summary=summary[0]['summary_text'], text=text)

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)