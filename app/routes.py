from flask import Blueprint, request, render_template, session, redirect, url_for, send_file
from .scraper import download_images_from_url
import zipfile
import io
import requests

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urlLink = request.form['urlLink']
        new_images = download_images_from_url(urlLink)

        current_images = session.get('images', [])

        session['images'] = current_images + new_images

        return redirect(url_for('main.index'))

    images = session.get('images', [])
    return render_template('index.html', images=images)

@main.route('/download', methods=['GET'])
def download_images():
    images = session.get('images', [])

    if not images:
        return redirect(url_for('main.index'))

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for idx, image_url in enumerate(images):
            image_name = f"image_{idx+1}.jpg"
            zip_file.writestr(image_name, requests.get(image_url).content)

    zip_buffer.seek(0)

    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='images.zip'
    )

@main.route('/clear', methods=['POST'])
def clear_images():
    session.pop('images', None)
    return redirect(url_for('main.index'))
