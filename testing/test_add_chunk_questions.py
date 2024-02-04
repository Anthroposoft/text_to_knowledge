import unittest
from unittest.mock import patch, MagicMock
from ttk.models.text_models import BookModel, ChunkModel, ChapterModel
from ttk.models.config_models import QuestionChunkConfigModel
from ttk.llm_processing.add_chunk_questions import add_chunk_questions


class TestAddQuestions(unittest.TestCase):

    def setUp(self):
        # Set up a basic configuration for testing
        self.config = QuestionChunkConfigModel(
            system_prompt="System prompt",
            user_prompt="{book_title} {chapter} {authors} {context_chunks} {chunk_text}",
            api_key="test_api_key",
            url="http://test_url",
            number_of_questions_div=10,
            context="Test context",
            name="simple"
        )

        # Set up a basic book model for testing
        self.book = BookModel(
            book_title="Test Book",
            authors=["Author One", "Author Two"],
            chapters=[
                ChapterModel(
                    chapter="Chapter One",
                    chapter_id=1,
                    chunks=[
                        ChunkModel(text="Chunk text one.", num_words=20),
                        ChunkModel(text="Chunk text two.", num_words=20)
                    ]
                )
            ]
        )

        # Mock file path for testing
        self.file_path = "test_book.json"

    @patch('ttk.llm_processing.add_chunk_questions.OpenAI')
    @patch('ttk.llm_processing.add_chunk_questions.request_llm')
    @patch('builtins.open')
    def test_add_questions(self, mock_open, mock_request_llm, mock_openai_client):
        # Mock the response from the LLM
        mock_request_llm.return_value = '{"text_list": ["Test question 1?", "Test question 2?"], "assessment": "Test assessment"}'

        # Mock the OpenAI client
        mock_openai_client.return_value = MagicMock()

        # Call the function under test
        add_chunk_questions(book=self.book, config=self.config, file_path=self.file_path)

        # Assert that the request_llm function was called with the expected parameters
        mock_request_llm.assert_called()

        # Assert that the file was opened for writing
        mock_open.assert_called_with(self.file_path, "w", encoding="utf-8")

        # Assert that the book model was updated with questions
        self.assertEqual(len(self.book.chapters[0].chunks[0].questions[self.config.name].questions), 2)
        self.assertEqual(len(self.book.chapters[0].chunks[1].questions[self.config.name].questions), 2)
        self.assertEqual(self.book.chapters[0].chunks[0].questions[self.config.name].questions[0].question,
                         "Test question 1?")
        self.assertEqual(self.book.chapters[0].chunks[0].questions[self.config.name].questions[1].question,
                         "Test question 2?")
        self.assertEqual(self.book.chapters[0].chunks[1].questions[self.config.name].questions[0].question,
                         "Test question 1?")
        self.assertEqual(self.book.chapters[0].chunks[1].questions[self.config.name].questions[1].question,
                         "Test question 2?")

        # Assert that the book model was saved to the file
        mock_open.return_value.__enter__().write.assert_called()


if __name__ == '__main__':
    unittest.main()
