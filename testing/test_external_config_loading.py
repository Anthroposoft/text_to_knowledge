import unittest
from ttk.external_config_loader import load_external_config_from_file, load_external_config_from_file_exec
from ttk.models.config_models import ConfigBaseModel


class TestExternalConfigLoader(unittest.TestCase):

    def _validate_config(self, config: ConfigBaseModel):
        self.assertIsNotNone(config)
        self.assertEqual(config.max_tokens, 16768)
        self.assertEqual(config.frequency_penalty, 0)
        self.assertEqual(config.temperature, 0.3)
        self.assertEqual(config.num_context_chunks, 10)

    def test_load_external_config_from_file(self):
        """Test loading external config using importlib"""
        config = load_external_config_from_file('data/add_chunk_summary_config.py')
        self._validate_config(config)

    def test_load_external_config_from_file_exec(self):
        """Test loading external config using exec"""
        config = load_external_config_from_file_exec('data/add_chunk_summary_config.py')
        self._validate_config(config)


if __name__ == '__main__':
    unittest.main()
