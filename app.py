from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from my_celery import analyze_and_rename_document_task
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/path/to/uploads'
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
            print(f"Saving file to {file_path}")  # Debugging line
            file.save(file_path)
            print("File saved, calling Celery task...")  # Debugging line
            analyze_and_rename_document_task.delay(file_path)
            print("Celery task called.")  # Debugging line
            return jsonify(status="File is being processed"), 202
        else:
            return jsonify(error="Invalid file type"), 400
    return render_template('upload.html')

if __name__ == "__main__":
    app.run(debug=True, port=55000)
