##=============================================================================================================##
from flask import Flask, request, render_template, send_file, redirect, url_for
from bs4 import BeautifulSoup
import os
import requests

import pdfToTxt
import service

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

##=============================================================================================================##

# Маршрут главной страницы
@app.route('/')
def index():
    return render_template('new.html')

##=============================================================================================================##

@app.route('/download_audio')
def download_audio_file():
    path_to_file = './synthesized.wav'  # Путь к файлу
    return send_file(path_to_file, as_attachment=True)

# Маршрут для обработки аудиофайлов
@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    file = request.files.get('audio_file')
    if not file or not file.filename.lower().endswith(('.mp3', '.wav', '.ogg')):
        return "Uploaded file is not an audio file", 400
    # file = "audio.wav"

    audio_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(audio_path)
    return render_template('audio_player.html', audio_file=file.filename)

##=============================================================================================================##

@app.route("/upload_file", methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if (file.filename.lower().endswith('.pdf')):
        return service.upload_pdf(UPLOAD_FOLDER, file)
    elif(file):
        return service.upload_file(UPLOAD_FOLDER, file)
    return "No file uploaded", 400


##=============================================================================================================##\

@app.route("/upload_url_file", methods=['POST'])
def upload_url_file():
    url = request.form['url']
    if ("pdf" in url):
        return service.upload_url_pdf(url, UPLOAD_FOLDER)
    elif (url):
        return service.upload_url_file(url, UPLOAD_FOLDER)
    return "No URL provided", 400

##=============================================================================================================##

@app.route('/download/uploads/<filename>')
def download_file(filename):
    return send_file(os.path.join(UPLOAD_FOLDER, filename), as_attachment=True)

# Маршрут для предоставления загруженных файлов
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_file(os.path.join(UPLOAD_FOLDER, filename))

##=============================================================================================================##