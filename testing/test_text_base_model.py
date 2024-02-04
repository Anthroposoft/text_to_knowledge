import unittest
from ttk.models.text_models import (
    TextBaseModel, ResultMetaModel, QuestionModel, QuestionMetaModel, ResultModel, LLMRequestModel, LLMRequestStatus, CategoryModel
)


class TestTextBaseModel(unittest.TestCase):

    def setUp(self):
        # Set up a sophisticated data structure for ResultMetaModel and QuestionModel
        self.llm_request = LLMRequestModel(
            system="test_system",
            user="test_user",
            assistant="test_assistant",
            status=LLMRequestStatus.success
        )

        self.result_meta_model = ResultMetaModel(
            context="Test context for results",
            results=[
                ResultModel(
                    text="Result text 1",
                    assessment="Good",
                    quality=None,
                    llm_request=self.llm_request
                ),
                ResultModel(
                    text="Result text 2",
                    assessment="Average",
                    quality=None,
                    llm_request=self.llm_request
                )
            ],
            chunk_id=1,
            previous_chunk_ids=[0],
            llm_request=self.llm_request
        )

        self.question_model = QuestionModel(
            question="What is the purpose of unittests?",
            answers=[
                ResultModel(
                    text="To verify that a piece of code works as expected",
                    assessment="Correct",
                    quality=None,
                    llm_request=self.llm_request
                ),
                ResultModel(
                    text="To break the code",
                    assessment="Incorrect",
                    quality=None,
                    llm_request=self.llm_request
                )
            ]
        )

        self.text_base_model = TextBaseModel(
            text="This is a test text",
            category=None,
            summaries={"summary1": self.result_meta_model},
            questions={"question1": QuestionMetaModel(
                context="Test context for questions",
                questions=[self.question_model],
                assessment="Good",
                chunk_id=1,
                previous_chunk_ids=[0],
                category=CategoryModel(categories=["unittest"]),
                llm_request=self.llm_request
            )},
            num_characters=18,
            num_words=5,
            num_questions=1,
            llm_request=self.llm_request
        )

    def test_text_base_model_initialization(self):
        self.assertEqual(self.text_base_model.text, "This is a test text")
        self.assertIsNone(self.text_base_model.category)
        self.assertIn("summary1", self.text_base_model.summaries)
        self.assertIn("question1", self.text_base_model.questions)
        self.assertEqual(self.text_base_model.num_characters, 18)
        self.assertEqual(self.text_base_model.num_words, 5)
        self.assertEqual(self.text_base_model.num_questions, 1)
        self.assertEqual(self.text_base_model.llm_request, self.llm_request)

    def test_text_base_model_summaries(self):
        summary = self.text_base_model.summaries["summary1"]
        self.assertIsInstance(summary, ResultMetaModel)
        self.assertEqual(summary.context, "Test context for results")
        self.assertEqual(len(summary.results), 2)
        self.assertEqual(summary.results[0].text, "Result text 1")
        self.assertEqual(summary.results[1].text, "Result text 2")

    def test_text_base_model_questions(self):
        question_meta = self.text_base_model.questions["question1"]
        self.assertIsInstance(question_meta, QuestionMetaModel)
        self.assertEqual(question_meta.context, "Test context for questions")
        self.assertEqual(len(question_meta.questions), 1)
        self.assertEqual(question_meta.questions[0].question, "What is the purpose of unittests?")
        self.assertEqual(len(question_meta.questions[0].answers), 2)

    def test_text_base_model_category(self):
        # Testing the category after assigning a new CategoryModel
        new_category = CategoryModel(categories=["testing"], keywords=["unittest", "python"])
        self.text_base_model.category = new_category
        self.assertIsNotNone(self.text_base_model.category)
        self.assertEqual(self.text_base_model.category.categories, ["testing"])
        self.assertEqual(self.text_base_model.category.keywords, ["unittest", "python"])


if __name__ == '__main__':
    unittest.main()
