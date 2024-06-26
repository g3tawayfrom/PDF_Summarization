import pdfplumber
from summarizer import Summarizer, TransformerSummarizer

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

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
