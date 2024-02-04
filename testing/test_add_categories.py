import unittest
from unittest.mock import patch
from ttk.models.text_models import BookModel, ChunkModel, ChapterModel
from ttk.models.config_models import ConfigBaseModel
from ttk.llm_processing.add_categories import add_categories


class TestAddCategories(unittest.TestCase):

    def setUp(self):
        self.config = ConfigBaseModel(
            api_key='test_key',
            url='https://api.test.xyz/v1',
            model="test-model",
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )

        self.book = BookModel(
            book_title='Testbuch',
            authors=['Max Muster'],
            chapters=[ChapterModel(chapter='Kapitel 1', chapter_id=1, num_chunks=1,
                                   chunks=[
                                  ChunkModel(
                                      chunk_id=1,
                                      text='Dies ist ein Testtext für Kapitel 1, Abschnitt 1.',
                                      num_words=10
                                  )])])
        # Pfad zur Testdatei
        self.file_path = 'test_book.json'

    def _check_categories(self):
        self.assertEqual(self.book.chapters[0].chunks[0].category.categories, ['test_category'])
        self.assertEqual(self.book.chapters[0].chunks[0].category.keywords, ['test_keyword'])

    @patch('ttk.llm_processing.add_categories.request_llm')
    def test_add_categories(self, mock_request_llm):
        mock_request_llm.return_value = '{"categories": ["test_category"], "keywords": ["test_keyword"]}'
        add_categories(self.book, self.config, self.file_path, save_to_file=False)
        self._check_categories()

    @patch('ttk.llm_processing.add_categories.request_llm')
    def test_add_categories_json_quotes_1(self, mock_request_llm):
        mock_request_llm.return_value = """```json
        {"categories": ["test_category"], "keywords": ["test_keyword"]}```
        """
        add_categories(self.book, self.config, self.file_path, save_to_file=False)
        self._check_categories()

    @patch('ttk.llm_processing.add_categories.request_llm')
    def test_add_categories_json_quotes_2(self, mock_request_llm):
        mock_request_llm.return_value = """'''json
        {"categories": ["test_category"], "keywords": ["test_keyword"]}'''
        """
        add_categories(self.book, self.config, self.file_path, save_to_file=False)
        self._check_categories()


if __name__ == '__main__':
    unittest.main()
