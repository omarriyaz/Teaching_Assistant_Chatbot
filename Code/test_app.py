import unittest
from unittest.mock import MagicMock
from app import get_pdf_text, get_text_chunks, handle_user_input

class TestApp(unittest.TestCase):
    def test_get_pdf_text(self):
        # Define the path to the test PDF file
        test_pdf_path = "Code/testing/testpdf1.pdf"

        # Call the get_pdf_text function
        extracted_text = get_pdf_text([test_pdf_path])

        # Expected text from the test PDF file
        expected_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."

        # Check if the extracted text contains the expected text
        self.assertIn(expected_text, extracted_text)


class TestApp(unittest.TestCase):
    def test_get_text_chunks(self):
        # Define a sample text
        sample_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."

        # Call the get_text_chunks function
        chunks = get_text_chunks(sample_text)

        # Check if the function returns a list of chunks
        self.assertIsInstance(chunks, list)

        # Check if the total length of chunks is the same as the length of the sample text
        self.assertEqual(sum(len(chunk) for chunk in chunks), len(sample_text))



if __name__ == "__main__":
    unittest.main()
