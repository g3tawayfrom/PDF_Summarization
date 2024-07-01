import os
from flask import Flask, request, render_template, send_file
from fpdf import FPDF
import pdfplumber
from summarizer import Summarizer, TransformerSummarizer


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
import os


app = Flask(__name__)


def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text


def summarize_with_bert(text):
    bert_model = Summarizer()
    summary = ''.join(bert_model(text, min_length=200))
    return summary


def summarize_with_gpt2(text):
    GPT2_model = TransformerSummarizer(transformer_type="GPT2", transformer_model_key="gpt2-medium")
    summary = ''.join(GPT2_model(text, min_length=200))
    return summary


def summarize_with_xlnet(text):
    xlnet_model = TransformerSummarizer(transformer_type="XLNet", transformer_model_key="xlnet-base-cased")
    summary = ''.join(xlnet_model(text, min_length=200))
    return summary


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""
    if 'text' in request.form and request.form['text'].strip():
        text = request.form['text']
    elif 'file' in request.files and request.files['file'].filename != '':
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
    pdf_path = os.path.join("summaries", "summary.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a custom style
    custom_style = ParagraphStyle(
        'CustomStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=15
    )

    flowables = []

    for key, value in summary.items():
        flowables.append(Paragraph(f"{key.capitalize()} Summary:", custom_style))
        flowables.append(Spacer(1, 0.2 * inch))
        flowables.append(Paragraph(value, custom_style))
        flowables.append(Spacer(1, 0.5 * inch))

    doc.build(flowables)

    return pdf_path


if __name__ == '__main__':
    app.run(debug=True)
