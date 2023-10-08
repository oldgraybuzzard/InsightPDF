import os
import logging
from logic import extract_text_from_pdf, get_unique_filename
from date_extractor import extract_date

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'document_analyzer.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_and_rename_document(file_path):
    try:
        # Using the function defined in logic.py to extract text from PDF
        content = extract_text_from_pdf(file_path)
        date = extract_date(content)
        
        if date:
            file_name_without_ext, file_extension = os.path.splitext(os.path.basename(file_path))
            new_file_name = f"{file_name_without_ext}-{date}{file_extension}"
            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

            # Ensure the new filename is unique
            unique_new_path = get_unique_filename(new_file_path)

            os.rename(file_path, unique_new_path)
            logging.info(f"File {file_path} renamed to {unique_new_path}")

            return os.path.basename(unique_new_path)
        else:
            logging.warning(f"No date found in the document: {file_path}")
            return os.path.basename(file_path)  # Return the original name if no date found
    
    except Exception as e:
        logging.error(f"An error occurred while processing {file_path}: {str(e)}")
        return None  # You might decide to handle this differently based on your use case
