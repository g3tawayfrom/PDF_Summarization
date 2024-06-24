import os
from flask import Flask, request, render_template, send_file
from transformers import pipeline, T5ForConditionalGeneration, T5Tokenizer
import PyPDF2
import pdfplumber
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTFigure
from fpdf import FPDF

app = Flask(__name__)


summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", revision="a4f8f3e")

model_name = "t5-large"
model = T5ForConditionalGeneration.from_pretrained(model_name)
tokenizer = T5Tokenizer.from_pretrained(model_name)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/summarize', methods=['POST'])
def summarize():
    text = ""
    if 'text' in request.form and request.form['text'].strip():
        text = request.form['text']
    elif 'file' in request.files:
        file = request.files['file']
        if file.filename.endswith('.pdf'):
            text = parse_pdf(file)

    # Отладочный вывод для проверки извлеченного текста
    print("Extracted text:", text)

    if text.strip():
        summary = summarize_text(text, model, tokenizer)
        summary_text = summary
    else:
        summary_text = "No valid text provided."

    # Отладочный вывод для проверки резюме
    print("Summary text:", summary_text)

    # Save the summary to a PDF
    pdf_path = save_summary_to_pdf(summary_text)

    return render_template('index.html', summary=summary_text, text=text, pdf_path=pdf_path)


@app.route('/download_pdf')
def download_pdf():
    pdf_path = request.args.get('pdf_path')
    if pdf_path and os.path.exists(pdf_path):
        return send_file(pdf_path, as_attachment=True)
    return "File not found", 404


def text_extraction(element):
    line_text = element.get_text()
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            for character in text_line:
                if isinstance(character, LTChar):
                    line_formats.append(character.fontname)
                    line_formats.append(character.size)
    format_per_line = list(set(line_formats))
    return (line_text, format_per_line)


def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table


def table_converter(table):
    table_string = ''
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [
            item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item
            in row]
        table_string += ('|' + '|'.join(cleaned_row) + '|\n')
    table_string = table_string[:-1]
    return table_string


def is_element_inside_any_table(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for table in tables:
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return True
    return False


def find_table_for_element(element, page, tables):
    x0, y0up, x1, y1up = element.bbox
    y0 = page.bbox[3] - y1up
    y1 = page.bbox[3] - y0up
    for i, table in enumerate(tables):
        tx0, ty0, tx1, ty1 = table.bbox
        if tx0 <= x0 <= x1 <= tx1 and ty0 <= y0 <= y1 <= ty1:
            return i
    return None


def parse_pdf(pdf_file):
    pdfFileObj = pdf_file.stream
    pdfReaded = PyPDF2.PdfReader(pdfFileObj)
    full_text = ""

    for pagenum, page in enumerate(extract_pages(pdf_file.stream)):
        pageObj = pdfReaded.pages[pagenum]
        page_text = []
        line_format = []
        text_from_tables = []
        page_content = []
        table_in_page = -1
        pdf = pdfplumber.open(pdf_file.stream)
        page_tables = pdf.pages[pagenum]
        tables = page_tables.find_tables()
        if len(tables) != 0:
            table_in_page = 0

        for table_num in range(len(tables)):
            table = extract_table(pdf_file.stream, pagenum, table_num)
            table_string = table_converter(table)
            text_from_tables.append(table_string)

        page_elements = [(element.y1, element) for element in page._objs]
        page_elements.sort(key=lambda a: a[0], reverse=True)

        for i, component in enumerate(page_elements):
            element = component[1]

            if table_in_page == -1:
                pass
            else:
                if is_element_inside_any_table(element, page, tables):
                    table_found = find_table_for_element(element, page, tables)
                    if table_found == table_in_page and table_found != None:
                        page_content.append(text_from_tables[table_in_page])
                        page_text.append('table')
                        line_format.append('table')
                        table_in_page += 1
                    continue

            if not is_element_inside_any_table(element, page, tables):
                if isinstance(element, LTTextContainer):
                    (line_text, format_per_line) = text_extraction(element)
                    page_text.append(line_text)
                    line_format.append(format_per_line)
                    page_content.append(line_text)

                if isinstance(element, LTFigure):
                    continue

        full_text += ''.join(page_content) + "\n"

    pdfFileObj.close()

    # Отладочный вывод для проверки полного текста
    print("Full extracted text:", full_text)

    return full_text


def summarize_text(text, model, tokenizer):
    max_length = min(len(text) // 2, 512)
    min_length = min(len(text) // 10, 50)
    min_length = min(min_length, max_length)

    inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(inputs, max_length=max_length, min_length=min_length, length_penalty=2.0, num_beams=4,
                             early_stopping=True)
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Отладочный вывод для проверки резюме
    print("Generated summary:", summary)

    return summary


def save_summary_to_pdf(summary):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf_path = os.path.join("summaries", "summary.pdf")
    os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
    pdf.output(pdf_path)
    return pdf_path


if __name__ == '__main__':
    app.run(debug=True)
