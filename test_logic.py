import unittest
from logic import classify_document, extract_text_from_pdf

class TestDocumentClassification(unittest.TestCase):
    
    def setUp(self):
        self.test_data = [
            {"text": "This is a notification about an event.", "type": "SF50"},
            {"text": "This document is a request for approval.", "type": "SF52"},
            {"text": "This text doesn't match any document type.", "type": "unknown"},
            {"text": "", "type": "unknown"},  # testing with empty string
            {"text": None, "type": "unknown"},  # testing with None
        ]
    
    def test_classify_document(self):
        for data in self.test_data:
            with self.subTest(msg=f"Testing with text: {data['text']}"):
                self.assertEqual(classify_document(data['text']), data['type'])
                
    # More test methods can be added to check other functionalities.
    
if __name__ == "__main__":
    unittest.main()
