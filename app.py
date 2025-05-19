import os
import qrcode
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, render_template, request, send_file, send_from_directory

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("firebase_service_account.json")  # Path to your service account key
firebase_admin.initialize_app(cred, {
    'storageBucket': 'qrshare-94732.appspot.com'  # Replace with your Firebase project ID
})

# Route for the home page
@app.route('/')
def home():
    #return render_template('index.html')
    return send_from_directory('.', 'index.html')

# Route for file upload
@app.route('upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the file locally
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    # Upload to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_filename(file_path)

    # Generate a public URL for the uploaded file
    blob.make_public()
    firebase_url = blob.public_url

    # Generate the QR code
    qr_image_path = generate_qr_code(firebase_url)

    return render_template('success.html', qr_image_path=qr_image_path)

# Function to generate a QR code
def generate_qr_code(url):
    qr = qrcode.make(url)
    qr_image_path = 'static/uploads/qrcode.png'
    os.makedirs('static/uploads', exist_ok=True)
    qr.save(qr_image_path)
    return qr_image_path

# Route to serve the QR code image
@app.route('/qr')
def serve_qr_code():
    return send_file('static/uploads/qrcode.png')

if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)

'''def serve_qr_code():
    return send_file('static/uploads/qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)'''
