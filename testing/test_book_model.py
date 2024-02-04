import unittest
from ttk.models.text_models import BookModel, ChapterModel, CategoryModel, QuestionModel, QuestionMetaModel


class TestBookModel(unittest.TestCase):

    def setUp(self):
        # Set up a basic BookModel instance for testing
        self.book_model = BookModel(
            authors=["Author 1", "Author 2"],
            publishing="Publishing House",
            book_title="The Great Book",
            chapters=[
                ChapterModel(chapter="Chapter 1", chapter_id=1, num_chunks=1),
                ChapterModel(chapter="Chapter 2", chapter_id=2, num_chunks=2)
            ]
        )

    def test_initialization(self):
        self.assertEqual(self.book_model.authors, ["Author 1", "Author 2"])
        self.assertEqual(self.book_model.publishing, "Publishing House")
        self.assertEqual(self.book_model.book_title, "The Great Book")
        self.assertEqual(len(self.book_model.chapters), 2)

    def test_authors_update(self):
        new_authors = ["Author 3"]
        self.book_model.authors = new_authors
        self.assertEqual(self.book_model.authors, new_authors)

    def test_publishing_update(self):
        new_publishing = "New Publishing House"
        self.book_model.publishing = new_publishing
        self.assertEqual(self.book_model.publishing, new_publishing)

    def test_book_title_update(self):
        new_book_title = "The Greatest Book"
        self.book_model.book_title = new_book_title
        self.assertEqual(self.book_model.book_title, new_book_title)

    def test_chapters_update(self):
        new_chapters = [
            ChapterModel(chapter="Chapter 3", chapter_id=3, num_chunks=3)
        ]
        self.book_model.chapters = new_chapters
        self.assertEqual(len(self.book_model.chapters), 1)
        self.assertEqual(self.book_model.chapters[0].chapter, "Chapter 3")

    def test_count_questions(self):

        self.book_model.questions["first"] = QuestionMetaModel(questions=[QuestionModel(question="Hi?")]*4)
        self.book_model.chapters[0].questions["first"] = QuestionMetaModel(questions=[QuestionModel(question="Hi?")]*2)
        self.book_model.chapters[1].questions["second"] = QuestionMetaModel(questions=[QuestionModel(question="Hi?")]*3)
        expected_count = 3 + 2 + 4  # Sum of chapter questions and book specific questions
        self.assertEqual(self.book_model.count_questions(), expected_count)

    def test_build_category_from_chapters(self):
        self.book_model.chapters[0].category = CategoryModel(categories=["Fiction"], keywords=["sample", "text"])
        self.book_model.chapters[1].category = CategoryModel(categories=["Mystery"], keywords=["puzzle", "clue"])
        self.book_model.build_category_from_chapters()
        self.assertIsNotNone(self.book_model.category)
        self.assertEqual(sorted(self.book_model.category.categories), ["Fiction", "Mystery"])
        self.assertEqual(sorted(self.book_model.category.keywords), ["clue", "puzzle", "sample", "text"])


if __name__ == '__main__':
    unittest.main()
