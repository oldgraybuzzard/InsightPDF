from celery import Celery
import shutil
from pypdf import PdfReader
import os
import logging

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'celery.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

rules = {
    'SF50': ['NOTIFICATION'],
    'SF52': ['Standard Form 52', '52', 'REQUEST', 'REQUEST FOR PERSONNEL ACTION'],
}

@app.task
def analyze_and_rename_document_task(file_path):
    try:
        extracted_text = extract_text_from_pdf(file_path)
        document_type = classify_document(extracted_text)
        new_path = rename_document(file_path, document_type)
        return new_path
    except Exception as e:
        logging.error(f"Error processing {file_path}: {str(e)}")

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
    return text

def classify_document(text):
    for doc_type, keywords in rules.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return doc_type
    return 'unknown'

def rename_document(original_path, new_name):
    directory, _ = os.path.split(original_path)
    folder_name = os.path.basename(directory)
    new_name_with_folder = f"{folder_name}-{new_name}"
    new_path = os.path.join(directory, new_name_with_folder)
    unique_new_path = get_unique_filename(new_path)
    shutil.copy2(original_path, unique_new_path)
    os.remove(original_path)
    return unique_new_path

def get_unique_filename(file_path):
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = f"{name}{ext}"
    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{name}-{counter}{ext}"
        counter += 1
    return os.path.join(directory, new_name)
