import unittest
from ttk.models.text_models import ChapterModel, ChunkModel, CategoryModel, QuestionMetaModel, QuestionModel


class TestChapterModel(unittest.TestCase):

    def setUp(self):
        # Set up a basic ChapterModel instance for testing
        self.chapter_model = ChapterModel(
            chapter="Chapter 1",
            chapter_id=0,
            num_chunks=2,
            chunks=[
                ChunkModel(chunk_id=0, section="Section 1", subsection="Subsection A"),
                ChunkModel(chunk_id=1, section="Section 2", subsection="Subsection B")
            ]
        )

    def test_initialization(self):
        self.assertEqual(self.chapter_model.chapter, "Chapter 1")
        self.assertEqual(self.chapter_model.chapter_id, 0)
        self.assertEqual(self.chapter_model.num_chunks, 2)
        self.assertEqual(len(self.chapter_model.chunks), 2)

    def test_chapter_update(self):
        new_chapter = "Chapter 2"
        self.chapter_model.chapter = new_chapter
        self.assertEqual(self.chapter_model.chapter, new_chapter)

    def test_chapter_id_update(self):
        new_chapter_id = 2
        self.chapter_model.chapter_id = new_chapter_id
        self.assertEqual(self.chapter_model.chapter_id, new_chapter_id)

    def test_num_chunks_update(self):
        new_num_chunks = 3
        self.chapter_model.num_chunks = new_num_chunks
        self.assertEqual(self.chapter_model.num_chunks, new_num_chunks)

    def test_chunks_update(self):
        new_chunks = [
            ChunkModel(chunk_id=3, section="Section 3", subsection="Subsection C")
        ]
        self.chapter_model.chunks = new_chunks
        self.assertEqual(len(self.chapter_model.chunks), 1)
        self.assertEqual(self.chapter_model.chunks[0].chunk_id, 3)

    def test_count_questions(self):
        self.chapter_model.chunks[0].num_questions = 3
        self.chapter_model.chunks[1].num_questions = 2
        self.chapter_model.questions["first"] = QuestionMetaModel(questions=[QuestionModel(question="Hi?")]*4)
        expected_count = 3 + 2 + 4  # Sum of chunk questions and simple questions
        self.assertEqual(self.chapter_model.count_questions(), expected_count)

    def test_build_category_from_chunks(self):
        self.chapter_model.chunks[0].category = CategoryModel(categories=["Fiction"], keywords=["sample", "text"])
        self.chapter_model.chunks[1].category = CategoryModel(categories=["Mystery"], keywords=["puzzle", "clue"])
        self.chapter_model.build_category_from_chunks()
        self.assertIsNotNone(self.chapter_model.category)
        self.assertEqual(sorted(self.chapter_model.category.categories), ["Fiction", "Mystery"])
        self.assertEqual(sorted(self.chapter_model.category.keywords), ["clue", "puzzle", "sample", "text"])


if __name__ == '__main__':
    unittest.main()
