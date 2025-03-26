import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages

hashes = []  # List to store hashes

@app.route('/')
def index():
    return render_template('index.html', hashes=hashes)

@app.route('/add_hash', methods=['POST'])
def add_hash():
    hash_value = request.form.get('hash_value')
    if hash_value:
        hashes.append(hash_value)
    return redirect(url_for('index'))


@app.route('/export_txt')
def export_txt():
    txt_path = "hashes.txt"
    with open(txt_path, 'w') as f:
        for hash_value in hashes:
            f.write(f"{hash_value}\n")
    return send_file(txt_path, as_attachment=True)

@app.route('/import_hashes', methods=['POST'])
def import_hashes():
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))

    if file:
        content = file.read().decode('utf-8')
        new_hashes = content.splitlines()
        for hash_value in new_hashes:
            if hash_value and hash_value not in hashes:
                hashes.append(hash_value)
        flash('Hashes imported successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/search_hash', methods=['POST'])
def search_hash():
    search_value = request.form.get('search_value')
    if search_value in hashes:
        flash(f'Hash "{search_value}" found!', 'success')
    else:
        flash(f'Hash "{search_value}" not found.', 'error')
    return redirect(url_for('index'))

@app.route('/compare_hash', methods=['POST'])
def compare_hash():
    compare_value = request.form.get('compare_value')
    matches = [h for h in hashes if h == compare_value]
    if matches:
        flash(f'Match found for hash "{compare_value}"!', 'success')
    else:
        flash(f'No match found for hash "{compare_value}".', 'error')
    return redirect(url_for('index'))

@app.route('/compare_two_hashes', methods=['POST'])
def compare_two_hashes():
    hash1 = request.form.get('hash1')
    hash2 = request.form.get('hash2')
    if hash1 == hash2:
        flash(f'The hashes are equal: "{hash1}"', 'success')
    else:
        flash(f'The hashes are not equal: "{hash1}" and "{hash2}"', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
