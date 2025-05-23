from flask import Flask, request, render_template, send_file
import yt_dlp
import uuid
import os

app = Flask(__name__)
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    uid = str(uuid.uuid4())
    output_path = f"{DOWNLOAD_FOLDER}/{uid}.%(ext)s"

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        mp3_file = output_path.replace('%(ext)s', 'mp3')
        return send_file(mp3_file, as_attachment=True)
    except Exception as e:
        return f"<p>Erro: {str(e)}</p>"
