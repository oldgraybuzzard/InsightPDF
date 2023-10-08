import unittest
from logic import classify_document, extract_text_from_pdf, extract_date  
# Ensure all functions are imported

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

    def test_extract_date(self):  # This should be a method in the class
        test_cases = [
            ("This is a date: 2022-03-15", "2022-03-15"),
            ("US format: 03/15/2022", "03/15/2022"),
            ("European format: 15/03/2022", "15/03/2022"),
            ("No date here!", None),
            # Add more test cases to ensure robustness
        ]
        
        for input_text, expected_output in test_cases:
            with self.subTest(msg=f"Testing with text: {input_text}"):
                self.assertEqual(extract_date(input_text), expected_output)

# More test methods can be added to check other functionalities.

if __name__ == "__main__":
    unittest.main()
