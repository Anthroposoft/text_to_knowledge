import unittest
from unittest.mock import patch
from ttk.models.text_models import BookModel, ChapterModel, ChunkModel
from ttk.models.config_models import SummaryChunkConfigModel
from ttk.llm_processing.add_chunk_summaries import add_chunk_summaries


class TestAddSummaries(unittest.TestCase):

    def _reset_test_data(self):

        self.book = BookModel(
            book_title="Test Book",
            authors=["Author 1"],
            chapters=[
                ChapterModel(
                    chapter="Chapter 1",
                    chapter_id=0,
                    chunks=[
                        ChunkModel(chunk_id=0, text="Chunk 1 text"),
                        ChunkModel(chunk_id=1, text="Chunk 2 text")
                    ]
                )
            ]
        )

    def setUp(self):
        self._reset_test_data()
        # Set up mock objects and test data
        self.config = SummaryChunkConfigModel(
            system_prompt="System prompt",
            user_prompt="User prompt with {book_title} and {chapter}",
            api_key="test_api_key",
            url="http://test_url",
            num_summaries=3,
            name="short",
            context="Short summaries"
        )
        self.file_path = "test_file_path.json"
        self.summary_response = {
            "response": "This is a summary.",
            "assessment": "Confident"
        }

        self.response_formats = [
            """```json
            {"response": "This is a summary.", "assessment": "Confident"}
            ```
            """,
            """
            Here is your requested summary with assessment.
            ```json
            {"response": "This is a summary.", "assessment": "Confident"}
            ```
            """
        ]

    def check_mocking(self, mock_open, mock_request_llm, mock_openai):
        # Check that the file was opened for writing
        mock_open.assert_called_with(self.file_path, "w", encoding="utf-8")
        # Check that the request_llm was called with the correct parameters
        mock_request_llm.assert_called()
        # Check that the OpenAI client was created with the correct API key and URL
        mock_openai.assert_called_with(api_key=self.config.api_key, base_url=self.config.url)

    def run_add_summaries_short_test(self, mock_request_llm, expected_response):
        # Mock the request_llm to return a summary response
        mock_request_llm.return_value = expected_response
        # Call the add_summaries function with the mocked objects
        add_chunk_summaries(book=self.book, config=self.config, file_path=self.file_path, save_to_file=True)
        # Check that the summary was added to the chunks
        for chapter in self.book.chapters:
            for chunk in chapter.chunks:
                self.assertEqual(len(chunk.summaries[self.config.name].results), 3)
                self.assertEqual(chunk.summaries[self.config.name].results[0].text, self.summary_response["response"])
                self.assertEqual(chunk.summaries[self.config.name].results[0].assessment,
                                 self.summary_response["assessment"])
                self.assertEqual(chunk.summaries[self.config.name].results[1].text, self.summary_response["response"])
                self.assertEqual(chunk.summaries[self.config.name].results[1].assessment,
                                 self.summary_response["assessment"])
                self.assertEqual(chunk.summaries[self.config.name].results[2].text, self.summary_response["response"])
                self.assertEqual(chunk.summaries[self.config.name].results[2].assessment,
                                 self.summary_response["assessment"])
            self.assertEqual(chapter.chunks[0].summaries[self.config.name].previous_chunk_ids, [])
            self.assertEqual(chapter.chunks[1].summaries[self.config.name].previous_chunk_ids, [0])
            self.assertEqual(chapter.chunks[1].summaries[self.config.name].context, self.config.context)

    @patch('ttk.llm_processing.add_chunk_summaries.request_llm')
    @patch('ttk.llm_processing.add_chunk_summaries.OpenAI')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_add_summaries_short_1(self, mock_open, mock_openai, mock_request_llm):
        for response in self.response_formats:
            self._reset_test_data()
            with self.subTest(response=response):
                self.run_add_summaries_short_test(mock_request_llm, response)
        self.check_mocking(mock_open, mock_request_llm, mock_openai)

    @patch('ttk.llm_processing.add_chunk_summaries.request_llm')
    @patch('ttk.llm_processing.add_chunk_summaries.OpenAI')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_add_summaries_short_2(self, mock_open, mock_openai, mock_request_llm):
        self._reset_test_data()
        for response in self.response_formats:
            with self.subTest(response=response):
                self.run_add_summaries_short_test(mock_request_llm, response)
        self.check_mocking(mock_open, mock_request_llm, mock_openai)


if __name__ == '__main__':
    unittest.main()
