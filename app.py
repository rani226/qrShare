import os
import qrcode
from flask import Flask, render_template, request, send_file, send_from_directory
from github import Github

app = Flask(__name__)

# GitHub credentials and settings
GITHUB_TOKEN = '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'
REPO_NAME = 'FileStore'
BRANCH_NAME = 'main'  # Change this if your branch name is different

# Route for the home page
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')  # Serve index.html from the current directory

# Route for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    
    # Save the file locally (optional)
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)  # Create the uploads directory if it doesn't exist
    file.save(file_path)

    # Upload to GitHub
    upload_result = upload_to_github(file_path, file.filename)

    # Generate the GitHub URL for the uploaded file
    github_url = f"https://github.com/<rani226>/{REPO_NAME}/blob/{BRANCH_NAME}/{file.filename}"

    # Generate the QR code
    qr_image_path = generate_qr_code(github_url)

    return render_template('success.html', qr_image_path=qr_image_path)

# Function to upload the file to GitHub
def upload_to_github(file_path, file_name):
    g = Github(GITHUB_TOKEN)
    repo = g.get_user().get_repo(REPO_NAME)

    with open(file_path, 'rb') as file:
        content = file.read()
        
        try:
            existing_file = repo.get_contents(file_name)
            sha = existing_file.sha  # Get the sha of the existing file
            repo.update_file(existing_file.path, "Update via Flask app", content, sha)
            return f"File {file_name} updated on GitHub successfully."
        except Exception:
            repo.create_file(file_name, "Upload via Flask app", content)
            return f"File {file_name} uploaded to GitHub successfully."

# Function to generate a QR code
def generate_qr_code(url):
    qr = qrcode.make(url)
    qr_image_path = 'static/uploads/qrcode.png'
    os.makedirs('static/uploads', exist_ok=True)  # Create the static/uploads directory if it doesn't exist
    qr.save(qr_image_path)
    return qr_image_path

# Route to serve the QR code image
@app.route('/qr')
def serve_qr_code():
    return send_file('static/uploads/qrcode.png')

if __name__ == '__main__':
    app.run(debug=True)
