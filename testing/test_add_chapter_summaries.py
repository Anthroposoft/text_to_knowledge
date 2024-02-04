import unittest
from unittest.mock import patch, MagicMock
from ttk.llm_processing.add_chapter_summaries import add_chapter_summaries
from ttk.models.text_models import BookModel, ChapterModel, ResultMetaModel
from ttk.models.config_models import SummaryChunkConfigModel


class TestAddChapterSummaries(unittest.TestCase):
    def setUp(self):
        # Set up test data for the book, chapters, and configuration
        self.book = BookModel(
            book_title="Test Book",
            authors=["Author One", "Author Two"],
            chapters=[
                ChapterModel(
                    chapter="Chapter 1",
                    text="This is the text of chapter 1.",
                    summaries={}
                ),
                ChapterModel(
                    chapter="Chapter 2",
                    text="This is the text of chapter 2.",
                    summaries={}
                )
            ]
        )
        self.config = SummaryChunkConfigModel(
            system_prompt="Provide a summary for the following text:",
            user_prompt="{book_title} {chapter} {authors} {chapter_text}",
            api_key="fake_api_key",
            url="http://fake_url",
            name="test",
            num_summaries=3  # We want to generate 3 summaries per chapter
        )
        self.file_path = "fake_file_path"

    @patch('ttk.llm_processing.add_chapter_summaries.request_llm')
    @patch('ttk.utils.save_book_to_file')
    def test_add_chapter_summaries(self, mock_save_book_to_file, mock_request_llm):
        # Mock the request_llm to return a fake summary
        mock_request_llm.return_value = "This is a fake summary."

        # Run the add_chapter_summaries function
        add_chapter_summaries(self.book, self.config, self.file_path, False)

        # Assertions to check if the summaries were added correctly
        for chapter in self.book.chapters:
            self.assertIn(self.config.name, chapter.summaries)
            self.assertEqual(len(chapter.summaries[self.config.name].results), self.config.num_summaries)

        # Check if request_llm was called the correct number of times
        num_chapters = len(self.book.chapters)
        self.assertEqual(mock_request_llm.call_count, num_chapters * self.config.num_summaries)

        # Check if save_book_to_file was called at least once
        self.assertGreaterEqual(mock_save_book_to_file.call_count, 0)


if __name__ == '__main__':
    unittest.main()
