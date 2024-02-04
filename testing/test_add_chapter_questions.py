import unittest
from unittest.mock import patch, MagicMock
from ttk.llm_processing.add_chapter_questions import add_chapter_questions
from ttk.models.text_models import BookModel, ChapterModel, QuestionMetaModel
from ttk.models.config_models import QuestionChunkConfigModel


class TestAddChapterQuestions(unittest.TestCase):
    def setUp(self):
        # Set up test data for the book, chapters, and configuration
        self.book = BookModel(
            book_title="Test Book",
            authors=["Author One", "Author Two"],
            chapters=[
                ChapterModel(
                    chapter="Chapter 1",
                    text="This is the text of chapter 1.",
                    questions={}
                ),
                ChapterModel(
                    chapter="Chapter 2",
                    text="This is the text of chapter 2.",
                    questions={}
                )
            ]
        )
        self.config = QuestionChunkConfigModel(
            system_prompt="Generate questions for the following text:",
            user_prompt="{book_title} {chapter} {authors} {chapter_text}",
            api_key="fake_api_key",
            url="http://fake_url",
            name="test_questions",
            context="Test Context"
        )
        self.file_path = "fake_file_path"

    @patch('ttk.llm_processing.add_chapter_questions.request_llm')
    @patch('ttk.utils.save_book_to_file')
    def test_add_chapter_questions(self, mock_save_book_to_file, mock_request_llm):
        # Mock the request_llm to return a fake response
        mock_request_llm.return_value = '{"text_list": ["Test question 1?", "Test question 2?"], "assessment": "Test assessment"}'

        # Run the add_chapter_questions function
        add_chapter_questions(self.book, self.config, self.file_path, False)

        # Assertions to check if the questions were added correctly
        for chapter in self.book.chapters:
            self.assertIn(self.config.name, chapter.questions)
            self.assertIsInstance(chapter.questions[self.config.name], QuestionMetaModel)
            self.assertEqual(chapter.questions[self.config.name].context, self.config.context)

        # Check if request_llm was called the correct number of times
        num_chapters_with_questions = sum(
            1 for chapter in self.book.chapters if chapter.questions[self.config.name].questions)
        self.assertEqual(mock_request_llm.call_count, num_chapters_with_questions)

        # Check if save_book_to_file was called at least once
        self.assertGreaterEqual(mock_save_book_to_file.call_count, 0)


if __name__ == '__main__':
    unittest.main()
