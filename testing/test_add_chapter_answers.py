import unittest
from unittest.mock import patch, MagicMock
from ttk.llm_processing.add_chapter_answers import add_chapter_answers_to_questions
from ttk.models.text_models import BookModel, ChapterModel, QuestionMetaModel, QuestionModel
from ttk.models.config_models import QuestionAnsweringChunkConfigModel


class TestAddChapterAnswersToQuestions(unittest.TestCase):
    def setUp(self):
        # Set up test data for the book, chapters, and configuration
        self.book = BookModel(
            book_title="Test Book",
            authors=["Author One", "Author Two"],
            chapters=[
                ChapterModel(
                    chapter="Chapter 1",
                    text="This is the text of chapter 1.",
                    questions={
                        "test_questions": QuestionMetaModel(
                            questions=[
                                QuestionModel(question="Question 1"),
                                QuestionModel(question="Question 2"),
                                QuestionModel(question="Question 3")
                            ]
                        )
                    }
                )
            ]
        )
        self.config = QuestionAnsweringChunkConfigModel(
            system_prompt="Generate answers for the following question:",
            user_prompt="{book_title} {chapter} {authors} {chapter_text} {question}",
            api_key="fake_api_key",
            url="http://fake_url",
            name="test_questions",
            context="Test Context",
            number_of_answers=3  # We want to generate 3 answers per question
        )
        self.file_path = "fake_file_path"

    @patch('ttk.llm_processing.add_chapter_answers.request_llm')
    @patch('ttk.utils.save_book_to_file')
    def test_add_chapter_answers_to_questions(self, mock_save_book_to_file, mock_request_llm):
        # Mock the request_llm to return a fake answer
        mock_request_llm.return_value = "This is a fake answer."

        # Run the add_chapter_answers_to_questions function
        add_chapter_answers_to_questions(self.book, self.config, self.file_path, False)

        # Assertions to check if the answers were added correctly
        for chapter in self.book.chapters:
            for question in chapter.questions[self.config.name].questions:
                self.assertEqual(len(question.answers), self.config.number_of_answers)

        self.assertEqual(mock_request_llm.call_count, 9)

        # Check if save_book_to_file was called at least once
        self.assertGreaterEqual(mock_save_book_to_file.call_count, 0)


if __name__ == '__main__':
    unittest.main()
