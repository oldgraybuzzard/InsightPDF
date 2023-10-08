import os
import requests
import logging

# URL for the API endpoint
url = "http://localhost:55000/classify_and_rename"

log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Setup logging
logging.basicConfig(filename=os.path.join(log_dir, 'file_upload.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_file(file_path):
    """
    Sends a file specified by file_path to the API endpoint.
    """
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(url, files=files, timeout=10) # 10s timeout for both connect and read
            response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Request failed for file {file_path}: {str(e)}")
        print(f"Request failed: {str(e)}")
    except Exception as e:
        logging.error(f"An unexpected error occurred for file {file_path}: {str(e)}")
        print(f"An unexpected error occurred: {str(e)}")
    else:
        logging.info(f"File {file_path} sent successfully. Response {response.status_code}: {response.text}")
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")

def send_files_in_folder(folder_path):
    """
    Sends all files in the specified folder to the API endpoint.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        logging.error(f"Folder not found: {folder_path}")
        print(f"Folder not found: {folder_path}")
        return

    # List all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a file
        if os.path.isfile(file_path):
            logging.info(f"Sending file: {filename}")
            print(f"Sending file: {filename}")
            send_file(file_path)
        else:
            logging.warning(f"Skipping non-file item: {filename}")
            print(f"Skipping non-file item: {filename}")

if __name__ == "__main__":
    # Specify the path to the folder.
    folder_path = os.path.join("C:", "Users", "YourUsername", "Desktop", "CHRA")
    
    # Call the function with the folder_path as the argument
    send_files_in_folder(folder_path)
