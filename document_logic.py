import os
import shutil
from pypdf import PdfReader
import logging

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'document_logic.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Your rules and other constants
rules = {
    'SF50': ['NOTIFICATION'],
    'SF52': ['Standard Form 52', '52', 'REQUEST', 'REQUEST FOR PERSONNEL ACTION'],
    # ... other document types and keywords
}

def extract_text_from_pdf(file_path):
    """
    Extract text content from a PDF file.
    
    :param file_path: str, path to the PDF file
    :return: str, extracted text
    """
    text = []
    try:
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            number_of_pages = len(reader.pages)
            page = reader.pages[0]
            text = page.extract_text()
        return "".join(text)
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        return ""

def classify_document(text):
    """
    Classify document type based on specific keywords in the text.

    :param text: str, text to classify
    :return: str, document type or 'unknown' if no match is found
    """
    if text is None:
        logging.error("Attempted to classify None text.")
        return 'unknown'
    
    for doc_type, keywords in rules.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return doc_type
    return 'unknown'

def rename_document(original_path, new_name):
    """
    Rename document ensuring the new name is unique.

    :param original_path: str, path to the original file
    :param new_name: str, new base name for the file
    :return: str, path to the renamed file
    """
    directory, _ = os.path.split(original_path)
    folder_name = os.path.basename(directory)
    new_name_with_folder = f"{folder_name}-{new_name}"
    new_path = os.path.join(directory, new_name_with_folder)

    unique_new_path = get_unique_filename(new_path)

    try:
        shutil.copy2(original_path, unique_new_path)
        os.remove(original_path)
    except Exception as e:
        print(f"Error renaming file {original_path} to {unique_new_path}: {e}")
        return original_path  # If error, return the original path
    
    return unique_new_path

def get_unique_filename(file_path):
    """
    Generates a unique filename by appending a number if the file already exists.

    :param file_path: str, desired file path
    :return: str, unique file path
    """
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    counter = 1

    while os.path.exists(os.path.join(directory, f"{name}{ext}")):
        name = f"{name}-{counter}"
        counter += 1

    return os.path.join(directory, f"{name}{ext}")
