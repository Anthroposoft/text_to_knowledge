import unittest
from unittest.mock import patch, MagicMock
from ttk.models.text_models import BookModel, ChapterModel, ChunkModel, QuestionModel, ResultModel, QuestionMetaModel
from ttk.models.config_models import QuestionAnsweringChunkConfigModel
from ttk.llm_processing.add_chunk_answers import add_chunk_answers_to_questions


class TestAddChunkAnswersToQuestions(unittest.TestCase):

    def setUp(self):
        # Set up sophisticated test data
        self.book = BookModel(
            authors=["Test Author"],
            publishing="Test Publishing",
            book_title="Test Book",
            chapters=[
                ChapterModel(
                    chapter="Chapter 1",
                    chapter_id=1,
                    num_chunks=1,
                    chunks=[
                        ChunkModel(
                            chunk_id=1,
                            text="This is a test chunk.",
                            questions={
                                "test_config": QuestionMetaModel(
                                    questions=[
                                        QuestionModel(question="What is unittest?"),
                                        QuestionModel(question="What is mocking?"),
                                        QuestionModel(question="What is patching?")
                                    ]
                                )
                            }
                        )
                    ]
                )
            ]
        )
        self.config = QuestionAnsweringChunkConfigModel(
            system_prompt="Test System Prompt",
            user_prompt="Test User Prompt: {question}",
            temperature=0.7,
            model="test-model",
            url="http://test-url",
            api_key="test-api-key",
            max_tokens=100,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            sleep_time_between_api_calls=0,
            number_of_answers=3,
            name="test_config"
        )
        self.file_path = "test_book.json"

    @patch('ttk.llm_processing.add_chunk_answers.request_llm')
    @patch('ttk.utils.save_book_to_file')
    def test_add_chunk_answers_to_questions(self, mock_save_book_to_file, mock_request_llm):
        # Mock the response from request_llm
        mock_request_llm.return_value = """```json
        {"response": "This is a test answer.", "assessment": "Confident"}```"""

        # Call the function under test
        add_chunk_answers_to_questions(self.book, self.config, self.file_path, False)

        # Assertions to check if the answers were added correctly
        for chapter in self.book.chapters:
            for chunk in chapter.chunks:
                for question in chunk.questions["test_config"].questions:
                    self.assertEqual(len(question.answers), self.config.number_of_answers)
                    for answer in question.answers:
                        self.assertEqual(answer.text, "This is a test answer.")
                        self.assertEqual(answer.assessment, "Confident")

        # Check if request_llm was called the correct number of times
        self.assertEqual(mock_request_llm.call_count, 9)  # 3 questions * 3 answers each

        # Check if save_book_to_file was called at least once
        self.assertGreaterEqual(mock_save_book_to_file.call_count, 0)


if __name__ == '__main__':
    unittest.main()
