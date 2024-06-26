# PDF Summarization Web Application

This project provides a web application built with Flask to extract and summarize text from PDF documents. The application uses various NLP models including BERT, GPT-2, and XLNet for text summarization. It also includes functionality to parse tables from PDF files.

## Features

- Extract text from PDF files.
- Summarize extracted text using BERT, GPT-2, and XLNet models.
- Parse tables from PDF documents.
- Download the summary as a PDF file.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository:**

    ```sh
    git clone https://github.com/g3tawayfrom/itmo_practice.git
    cd itmo_practice
    ```

2. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Flask application:**

    ```sh
    python app.py
    ```

2. **Open your web browser and go to:**

    ```
    http://127.0.0.1:5000
    ```

3. **Use the application:**

    - You can input text directly or upload a PDF file to extract and summarize its content.
    - View the generated summaries for BERT, GPT-2, and XLNet.
    - Download the summary as a PDF file.

## File Structure

- `app.py`: Main application file containing the Flask routes and logic for handling file uploads and text summarization.
- `summarization.py`: Contains functions for extracting text from PDF files, processing tables, and summarizing text using different models.
- `requirements.txt`: Lists all the dependencies required for the project.
- `templates/index.html`: HTML template for the web application interface.

## Dependencies

- Flask: Web framework for Python.
- transformers: Huggingface library for NLP models.
- pdfplumber: Library for extracting text from PDF files.
- PyPDF2: Library for working with PDF files.
- FPDF: Library for creating PDF files.
- NLTK: Natural Language Toolkit for text processing.

## Models Used

- BERT (Bidirectional Encoder Representations from Transformers)
- GPT-2 (Generative Pre-trained Transformer 2)
- XLNet


