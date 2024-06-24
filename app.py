import os
from flask import Flask, request, render_template, send_file
from transformers import T5ForConditionalGeneration, T5Tokenizer
from utils import parse_pdf, summarize_text, save_summary_to_pdf

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'summaries'

tokenizer = T5Tokenizer.from_pretrained("t5-large")
model = T5ForConditionalGeneration.from_pretrained("t5-large")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        print("No file part")
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return "No selected file", 400

    if file and file.filename.endswith('.pdf'):
        text = parse_pdf(file)
        print("Extracted text from PDF:", text)

        if text.strip():
            summary = summarize_text(text, model, tokenizer)
            summary_text = summary
            print("Generated summary:", summary_text)
        else:
            summary_text = "No valid text provided."

        pdf_path = save_summary_to_pdf(summary_text)
        print("PDF saved to:", pdf_path)

        return render_template('index.html', summary=summary_text, pdf_path=pdf_path)

    return "Invalid file type", 400

@app.route('/download_pdf')
def download_pdf():
    pdf_path = request.args.get('pdf_path')
    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
