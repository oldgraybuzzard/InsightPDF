import PyPDF2
import os

# Your rules and other constants
rules = {
    'SF50': ['NOTIFICATION'],
    'SF52': ['Standard Form 52', '52', 'REQUEST', 'REQUEST FOR PERSONNEL ACTION'],
    # ... other document types and keywords
}

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
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

    # Ensure the filename is unique
    unique_new_path = get_unique_filename(new_path)

    shutil.copy2(original_path, unique_new_path)
    os.remove(original_path)

    return unique_new_path

def get_unique_filename(file_path):
    """
    Generates a unique filename by appending a number if the file already exists.
    """
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    counter = 1
    new_name = f"{name}{ext}"

    while os.path.exists(os.path.join(directory, new_name)):
        new_name = f"{name}-{counter}{ext}"
        counter += 1

    return os.path.join(directory, new_name)

# Additional logic for extracting date and other processes...
