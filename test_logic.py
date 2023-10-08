import os
import unittest
from unittest.mock import patch, mock_open  # Ensure to import mock_open
from logic import classify_document, extract_text_from_pdf, extract_date
from werkzeug.datastructures import FileStorage
from app import app
from my_celery import analyze_and_rename_document_task
import tempfile

# Test data
TEST_FILE_PATH = r'Users/kfelder/CHRA Tests/SF-52 LN RPA_Redacted.pdf'
TEST_FILE = 'SF-52 LN RPA_Redacted.pdf'

class TestFileUpload(unittest.TestCase):
    
    @classmethod    
    def setUpClass(cls):
        cls.app = app.test_client()

    @patch("builtins.open", new_callable=mock_open, read_data=b"mocked data")
    def test_file_upload(self, mock_file):
        with open(TEST_FILE_PATH, 'rb') as fp:
            response = self.app.post('/upload', content_type='multipart/form-data', 
                                     data={'file': (fp, TEST_FILE)})
        self.assertEqual(response.status_code, 202, f"Expected status code 202, got {response.status_code} instead")
        self.assertIn(b'File is being processed', response.data)
    
        # Add more assertions here
    @patch('requests.post')
    def test_send_file(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'Success'
        # Test code that triggers the API call
        with open(TEST_FILE_PATH, 'rb') as f:
            # [Your API call logic triggering requests.post here...]
            pass
        
        # Assertions to check if the function behaves correctly with the above mock response
        mock_post.assert_called_once_with(
            '/upload',
            files={'file': (TEST_FILE, f)},
            # ... [any other parameters to validate]
        )

class TestPDFExtraction(unittest.TestCase):
    
    @patch('your_module.PdfReader')
    def test_extract_text_from_pdf(self, mock_reader):
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Some Text"
        
        mock_reader.return_value.pages = [mock_page]
        
        result = extract_text_from_pdf("some_path.pdf")
        self.assertEqual(result, "Some Text")

if __name__ == "__main__":
    unittest.main()
        
# class TestDocumentClassification(unittest.TestCase):
    
#     def test_classify_document(self):
#         test_data = [
#             {"text": "This is a notification about an event.", "type": "SF50"},
#             {"text": "This document is a request for approval.", "type": "SF52"},
#             {"text": "This text doesn't match any document type.", "type": "unknown"},
#             {"text": "", "type": "unknown"},  # testing with empty string
#             {"text": None, "type": "unknown"},  # testing with None
#         ]
#         for data in test_data:
#             with self.subTest(msg=f"Testing with text: {data['text']}"):
#                 self.assertEqual(classify_document(data['text']), data['type'])

#     def test_extract_date(self):
#         test_cases = [
#             ("This is a date: 2022-03-15", "2022-03-15"),
#             # More cases
#         ]
#         for input_text, expected_output in test_cases:
#             self.assertEqual(extract_date(input_text), expected_output)
    
#     @patch('logic.some_dependency', autospec=True)
#     def test_classify_document_with_mock(self, mock_dependency):
#         mock_dependency.return_value = 'expected value'
#         test_data = [
#             {"text": "Effective Date", "type": "Date"},
#             # ...[Other test cases requiring mock]...
#         ]
#         for data in test_data:
#             with self.subTest(msg=f"Testing with text: {data['text']}"):
#                 self.assertEqual(classify_document(data['text']), data['type'])
                
#  # Note: If there are other functions to test in 'logic' module, they should be tested here.
    
# class TestTasks(unittest.TestCase):

#     @patch('my_celery.analyze_and_rename_document_task.apply_async')
#     def test_analyze_and_rename_document_task(self, mock_apply_async):
#         analyze_and_rename_document_task.delay(TEST_FILE_PATH)
#         mock_apply_async.assert_called_once_with(args=[TEST_FILE_PATH])

# More test methods can be added to check other functionalities.

if __name__ == "__main__":
    unittest.main()
