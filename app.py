from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from my_celery import analyze_and_rename_document_task
import os
import logging

app = Flask(__name__)

# Ensure the logs directory exists
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Logging setup
logging.basicConfig(filename=os.path.join(log_dir, 'flask_app.log'), 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

app.config['UPLOAD_FOLDER'] = '/Users/kfelder/Desktop/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            logging.info(f"Saving file to {file_path}")
            try:
                file.save(file_path)
            except Exception as e:
                logging.error(f"Failed to save the file: {str(e)}")
                return jsonify(error="Failed to save the file"), 500
            
            logging.info("File saved, calling Celery task...")
            analyze_and_rename_document_task.delay(file_path)
            logging.info("Celery task called.")
            return jsonify(status="File is being processed"), 202
        else:
            logging.warning("Invalid file type attempted to upload.")
            return jsonify(error="Invalid file type"), 400

    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True, port=55000)
