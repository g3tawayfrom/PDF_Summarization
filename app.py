import os
from flask import Flask, request, render_template, send_file
from summarization import extract_text, summarize_with_bert, summarize_with_gpt2, summarize_with_xlnet
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
        bert_summary = summarize_with_bert(text)
        gpt2_summary = summarize_with_gpt2(text)
        xlnet_summary = summarize_with_xlnet(text)

        summary = {
            "bert": bert_summary,
            "gpt2": gpt2_summary,
            "xlnet": xlnet_summary
        }

        pdf_path = save_summary_to_pdf(summary)
    else:
        summary = None
        pdf_path = None

    return render_template('index.html', summary=summary, text=text, pdf_path=pdf_path)

@app.route('/download_pdf')
def download_pdf():
    pdf_path = request.args.get('pdf_path')
    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return "File not found", 404

def save_summary_to_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for key, value in summary.items():
        pdf.multi_cell(0, 10, f"{key.capitalize()} Summary:\n{value}\n\n")
    pdf_path = os.path.join("summaries", "summary.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf.output(pdf_path)
    return pdf_path


if __name__ == '__main__':
    app.run(debug=True)
