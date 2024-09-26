from cryptography.fernet import Fernet
import os

# Generate and save a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the file
def encrypt_file(file_path):
    generate_key()
    key = load_key()
    fernet = Fernet(key)
    
    with open(file_path, 'rb') as file:
        original_data = file.read()
    
    encrypted_data = fernet.encrypt(original_data)
    
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    os.remove(file_path)
    return encrypted_file_path
