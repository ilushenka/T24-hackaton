from flask import render_template
from bs4 import BeautifulSoup
import os
import requests

import pdfToTxt
import gptReq

def request_processing(file_path, text_content, to_remove=None):
    gpt_ans = gptReq.gpt_request(text_content)

    with open(file_path, 'w', encoding='utf-8') as text_file:
        text_file.write(gpt_ans.strip())
    if to_remove:
        os.remove(to_remove)
    print('sagrusheno')
    return render_template('download.html', filename=text_file.name)

def upload_pdf(UPLOAD_FOLDER, file):   
    pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(pdf_path)

    text_content = pdfToTxt.extract_text_from_pdf(pdf_path)
    file_path = pdf_path.rsplit('.', 1)[0] + '.txt'

    return request_processing(file_path, text_content)

def upload_file(UPLOAD_FOLDER, file):
    if file.filename.lower().endswith('.txt'):
        if pdfToTxt.contains_forbidden_words(file, pdfToTxt.forbidden_words):
            return "Файл содержит запрещенные слова. Загрузка отменена.", 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        with open(file) as f:
            text_content = f.open()

        return request_processing(file_path, text_content)

    return "File is not a text file", 400

def upload_url_pdf(url, UPLOAD_FOLDER):
    try:
        response = requests.get(url)
        response.raise_for_status() 

        pdf_path = 'temp.pdf'
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)

        text_content = pdfToTxt.extract_text_from_pdf(pdf_path)
        text_filename = 'converted_text.txt'
        file_path = os.path.join(UPLOAD_FOLDER, text_filename)

        return request_processing(file_path, text_content, to_remove=pdf_path)

    except requests.exceptions.RequestException as e:
        return f"Ошибка при загрузке PDF: {e}"

def upload_url_file(url, UPLOAD_FOLDER):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for ad in soup.find_all(class_=['ad', 'advertisement', 'ads', 'banner']):
            ad.decompose()

        paragraphs = soup.find_all('p')
        text_content = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        file_path = os.path.join(UPLOAD_FOLDER, 'webpage_text.txt')

        if pdfToTxt.contains_forbidden_words(text_content, pdfToTxt.forbidden_words):
            return "Извлеченный текст содержит запрещенные слова. Загрузка отменена.", 400

        return request_processing(file_path, text_content)

    except Exception as e:
        return f"An error occurred while fetching the webpage: {e}", 500