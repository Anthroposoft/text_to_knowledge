import unittest
from ttk.models.text_models import ChunkModel


class TestChunkModel(unittest.TestCase):

    def setUp(self):
        # Set up a basic ChunkModel instance for testing
        self.chunk_model = ChunkModel(
            chunk_id=0,
            section="Section 1",
            subsection="Subsection A"
        )

    def test_chunk_id_assignment(self):
        self.assertEqual(self.chunk_model.chunk_id, 0)

    def test_section_assignment(self):
        self.assertEqual(self.chunk_model.section, "Section 1")

    def test_subsection_assignment(self):
        self.assertEqual(self.chunk_model.subsection, "Subsection A")

    def test_chunk_id_update(self):
        new_chunk_id = 2
        self.chunk_model.chunk_id = new_chunk_id
        self.assertEqual(self.chunk_model.chunk_id, new_chunk_id)

    def test_section_update(self):
        new_section = "Section 2"
        self.chunk_model.section = new_section
        self.assertEqual(self.chunk_model.section, new_section)

    def test_subsection_update(self):
        new_subsection = "Subsection B"
        self.chunk_model.subsection = new_subsection
        self.assertEqual(self.chunk_model.subsection, new_subsection)


if __name__ == '__main__':
    unittest.main()
