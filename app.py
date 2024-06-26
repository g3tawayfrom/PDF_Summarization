import os
from flask import Flask, request, render_template, send_file
from pdf_processing import extract_text, summarize_with_bert, summarize_with_gpt2, summarize_with_xlnet, preprocessing, save_summary_to_pdf
from fpdf import FPDF

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""
    if 'text' in request.form and request.form['text'].strip():
        text = request.form['text']
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            text = extract_text(file)

    if text.strip():
        preprocessed_text = preprocessing(text)
        bert_summary = summarize_with_bert(preprocessed_text)
        gpt2_summary = summarize_with_gpt2(preprocessed_text)
        xlnet_summary = summarize_with_xlnet(preprocessed_text)
        summary_text = f"BERT Summary:\n{bert_summary}\n\nGPT-2 Summary:\n{gpt2_summary}\n\nXLNet Summary:\n{xlnet_summary}"
    else:
        summary_text = "No valid text provided."

    pdf_path = save_summary_to_pdf(summary_text)
    return render_template('index.html', summary=summary_text, text=text, pdf_path=pdf_path)

@app.route('/download_pdf')
def download_pdf():
    pdf_path = request.args.get('pdf_path')
    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)
