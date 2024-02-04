import unittest
import os
from ttk.file_parser import process_single_file
from ttk.models.text_models import BookModel


class TestProcessSingleFileIntegration(unittest.TestCase):
    output_dir = None
    file_name_long = None
    file_name_small = None

    @classmethod
    def setUpClass(cls):
        # Create the test input data
        cls.input_dir = 'data'
        cls.output_dir = '.'
        cls.file_name_long = 'book_sample.txt'
        cls.file_name_small = 'short_sample.txt'
        cls.chapter_prefix = '='
        cls.section_prefix = '=='
        cls.subsection_prefix = '==='

    @classmethod
    def tearDownClass(cls):
        # Clean up the output file
        os.remove(os.path.join(cls.output_dir, cls.file_name_long.replace('.txt', '.json')))
        os.remove(os.path.join(cls.output_dir, cls.file_name_small.replace('.txt', '.json')))
        pass

    def test_process_single_file_integration_long(self):
        # Run the test method for testing
        process_single_file(
            self.file_name_long,
            self.input_dir,
            self.output_dir,
            self.chapter_prefix,
            self.section_prefix,
            self.subsection_prefix
        )

        self._check_process_output(file_name=self.file_name_long)

    def test_process_single_file_integration_small(self):
        # Run the test method for testing
        process_single_file(
            self.file_name_small,
            self.input_dir,
            self.output_dir,
            self.chapter_prefix,
            self.section_prefix,
            self.subsection_prefix
        )

        self._check_process_output(file_name=self.file_name_small)

    def _check_process_output(self, file_name: str):
        # Check if the output was generated
        output_file_path = os.path.join(self.output_dir, file_name.replace('.txt', '.json'))
        self.assertTrue(os.path.exists(output_file_path))

        # Read the output and check for correct parsing with the reference model
        with open(output_file_path, "r", encoding="utf-8") as f:
            book_json = f.read()
            result_model = BookModel.model_validate_json(book_json)

        reference_file_path = os.path.join(self.input_dir, file_name.replace('.txt', '.json'))
        self.assertTrue(os.path.exists(reference_file_path))

        with open(reference_file_path, "r", encoding="utf-8") as f:
            book_json = f.read()
            reference_mode = BookModel.model_validate_json(book_json)

        self.assertEqual(result_model.model_dump(), reference_mode.model_dump())


if __name__ == '__main__':
    unittest.main()
