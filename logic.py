import os
import PyPDF2
import shutil
import logging

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'logic.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Rules for document classification
rules = {
    'SF50': ['NOTIFICATION'],
    'SF52': ['Standard Form 52', '52', 'REQUEST', 'REQUEST FOR PERSONNEL ACTION'],
    # ... other document types and keywords
}

def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF document.

    :param file_path: str, path to the PDF file
    :return: str, extracted text
    """
    text = ""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {str(e)}")
    return text

def classify_document(text):
    """
    Classifies the document based on the text and predefined rules.

    :param text: str, extracted text from the document
    :return: str, document type
    """
    for doc_type, keywords in rules.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return doc_type
    return 'unknown'

def get_unique_filename(file_path):
    """
    Generates a unique filename by appending a number if the file already exists.

    :param file_path: str, path to the file
    :return: str, unique file path
    """
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = f"{name}{ext}"

    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{name}-{counter}{ext}"
        counter += 1

    return os.path.join(directory, new_name)

def rename_and_move_document(original_path, new_name, target_folder):
    """
    Renames and moves the document to a target folder ensuring the filename is unique.

    :param original_path: str, path to the original document
    :param new_name: str, new name for the document
    :param target_folder: str, path to the target folder
    :return: str, path to the moved document
    """
    try:
        _, file_extension = os.path.splitext(original_path)
        new_file_name = f"{new_name}{file_extension}"
        new_file_path = os.path.join(target_folder, new_file_name)

        # Ensure the filename is unique
        unique_new_path = get_unique_filename(new_file_path)

        shutil.copy2(original_path, unique_new_path)
        os.remove(original_path)

        return unique_new_path

    except Exception as e:
        print(f"Error renaming/moving {original_path}: {str(e)}")
        return original_path  # If an error occurs, return the original path

# Additional logic for extracting date and other processes...
