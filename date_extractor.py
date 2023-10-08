import os
import re
from datetime import datetime
import logging

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'date_extractor.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Regex patterns to find dates in various formats
date_patterns = [
    (re.compile(r'\b\d{4}-\d{2}-\d{2}\b'), "%Y-%m-%d"),  # YYYY-MM-DD
    (re.compile(r'\b\d{2}/\d{2}/\d{4}\b'), "%d/%m/%Y"),  # DD/MM/YYYY
    (re.compile(r'\b\d{2}/\d{2}/\d{2}\b'), "%d/%m/%y"),   # DD/MM/YY
    (re.compile(r'\b\d{2}-\d{2}-\d{2}\b'), "%d-%m-%y"), #DD-MM-YY
    (re.compile(r'\b\d{2}-\d{2}-\d{2}\b'), "%m-%d-%y"), #MM-DD-YY
    (re.compile(r'\b\d{2}-\d{2}-\d{4}\b'), "%d-%m-%Y"), #DD-MM-YYYYY
    (re.compile(r'\b\d{2}\.\d{2}\.\d{4}\b'), "%d-%m-%Y"), #DD.MM.YYYYY
    (re.compile(r'\b\d{2}\.\d{2}\.\d{2}\b'), "%d-%m-%y"), #DD.MM.YY
    (re.compile(r'\b\d{2}-[A-Za-z]{3}-\d{2}\b', re.IGNORECASE), "%d-%b-%y"), #DD-MMM-YY
    (re.compile(r'\b\d{2}[A-Za-z]{3}\d{2}\b', re.IGNORECASE), "%d%b%y"), #DDMMMYY
    # Add additional patterns for other date formats
]

def extract_date(content):
    for pattern, date_format in date_patterns:
        match = pattern.search(content)
        if match:
            date_str = match.group(0)
            if validate_date(date_str, date_format):
                return date_str
            else:
                logging.error(f"Invalid date: {date_str}")
                return None
    return None

def validate_date(date_str, pattern):
    try:
        datetime.strptime(date_str, pattern)  # Try to create a datetime object using the format
        return True  # If successful, return True
    except ValueError:
        return False  # If a ValueError occurs, return False
