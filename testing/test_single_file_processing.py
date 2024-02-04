import unittest
from unittest.mock import patch, mock_open
from ttk.file_parser import process_single_file

book_sample_content = """The Philosophy of Freedom
Rudolf Steiner, Marie Steiner
Berlin, 1905
= Chapter 1
== Section 1.1
Some introductory text.
=== Subsection 1.1.1
More detailed text.
"""


class TestProcessSingleFile(unittest.TestCase):
    @patch('ttk.file_parser.os.path')
    @patch('ttk.file_parser.open', new_callable=mock_open, read_data=book_sample_content)
    @patch('ttk.file_parser.write_output')
    @patch('ttk.file_parser.parse_book')
    def test_process_single_file(self, mock_parse_book, mock_write_output, mock_file_open, mock_os_path):
        # Mocks für os.path.join und os.path.splitext
        mock_os_path.join.side_effect = lambda *args: '/'.join(args)
        mock_os_path.splitext.side_effect = lambda x: (x.split('.')[0], x.split('.')[1])

        # Wir setzen hier unser Testbuch als Rückgabewert des parse_book Mocks
        mock_parse_book.return_value = 'TestBookModel'

        # Pfadangaben für den Test
        input_dir = 'data'
        output_dir = '.'
        file_name = 'book_sample.txt'
        chapter_prefix = '='
        section_prefix = '=='
        subsection_prefix = '==='

        # Die eigentliche Testausführung
        process_single_file(file_name, input_dir, output_dir, chapter_prefix, section_prefix,
                            subsection_prefix)

        # Überprüfung, ob die Funktionen mit den erwarteten Argumenten aufgerufen wurden
        mock_file_open.assert_called_once_with('data/book_sample.txt', 'r', encoding='utf-8')
        mock_parse_book.assert_called_once()
        mock_write_output.assert_called_once_with('./book_sample.json', 'TestBookModel')


if __name__ == '__main__':
    unittest.main()
