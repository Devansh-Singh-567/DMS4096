from flask import Flask, render_template, request, jsonify
from dms4096 import DMS4096
import time
import fitz  # PyMuPDF for PDFs
import docx   # python-docx for Word files

# ✅ Load DMS4096 Key
with open("dms_4096_key.bin", "rb") as key_file:
    key = key_file.read()

dms = DMS4096(key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_text():
    data = request.json
    encrypted_text, elapsed_time = dms.encrypt(data['text'])
    return jsonify({'encrypted': encrypted_text, 'time': format(elapsed_time, '.4f')})  # Enhanced Timer Precision

@app.route('/decrypt', methods=['POST'])
def decrypt_text():
    data = request.json
    decrypted_text, elapsed_time = dms.decrypt(data['text'])
    return jsonify({'decrypted': decrypted_text, 'time': format(elapsed_time, '.4f')})  # Enhanced Timer Precision

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return jsonify({'error': 'No file uploaded'})

    text = extract_text(file)
    if not text:
        return jsonify({'error': 'Unsupported file format or empty file'})

    encrypted_text, elapsed_time = dms.encrypt(text)
    return jsonify({'text': text, 'encrypted': encrypted_text, 'time': format(elapsed_time, '.4f')})  # Enhanced Timer Precision

def extract_text(file):
    """Extract text from PDF or Word file"""
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "\n".join([page.get_text() for page in doc])
    
    elif filename.endswith('.docx'):
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    return None  # Unsupported format

if __name__ == '__main__':
    app.run(debug=True)
