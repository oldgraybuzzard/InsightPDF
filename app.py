from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from my_celery import analyze_and_rename_document_task
import logging
import traceback
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.ProductionConfig')
    load_configurations(app)
    configure_logging(app)
    return app

def load_configurations(app):
    secret_key = os.getenv('SECRET_KEY')
    if secret_key is None:
        raise ValueError("SECRET_KEY is not set in the environment variables.")
    
    app.config['SECRET_KEY'] = secret_key
    app.config['DEBUG'] = os.getenv('DEBUG') == 'True'
    
def configure_logging(app):
    log_dir = app.config.get('LOG_DIR')
    if log_dir is None:
        raise ValueError("LOG_DIR is not configured.")
    
    logging.basicConfig(
        filename=os.path.join(log_dir, 'flask_app.log'), 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

app = create_app()

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
                logging.error(f"Failed to save the file: {str(e)}\n{traceback.format_exc()}")
                return jsonify(error="Failed to save the file"), 500
            
            logging.info("File saved, calling Celery task...")
            task = analyze_and_rename_document_task.delay(file_path)
            logging.info(f"Celery task called with ID: {task.id}")

            # Check the task status
            task_status = task.status
            logging.info(f"Task status: {task_status}")
            
            return jsonify(status="File is being processed", task_id=task.id), 202
        else:
            logging.warning("Invalid file type attempted to upload.")
            return jsonify(error="Invalid file type"), 400

    return render_template('upload.html')

@app.errorhandler(500)
def handle_internal_server_error(e):
    logging.error(f"Internal Server Error: {str(e)}\n{traceback.format_exc()}")
    return jsonify(error="Internal Server Error"), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], port=55000)
