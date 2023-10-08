import requests
import os

# URL for the API endpoint
url = "http://localhost:55000/classify_and_rename"

# File path you want to send
file_path = os.path.join("C:", "Users", "kfelder", "Desktop", "CHRA", "https___taxapps.floridarevenue.com_OnlineBillPayment_PaymentConfirmation.pdf")

def send_file(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    except requests.RequestException as e:
        print(f"Request failed: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    else:
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.text}")

if __name__ == "__main__":
    send_file(file_path)
