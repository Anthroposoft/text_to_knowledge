import unittest
from unittest.mock import patch
import logging

from ttk.utils import extract_yaml_from_text, extract_json_from_text


class TestExtractYamlFromText(unittest.TestCase):

    def test_extract_yaml_present(self):
        text = "Some text before YAML block.\n```yaml\nname: Test\nvalue: 42\n```\nSome text after."
        expected_yaml = "name: Test\nvalue: 42"
        self.assertEqual(extract_yaml_from_text(text), expected_yaml)

    def test_extract_yaml_absent(self):
        text = "There is no YAML block here."
        self.assertIsNone(extract_yaml_from_text(text))

    def test_extract_yaml_no_end(self):
        text = "Some text before YAML block.\n```yaml\nname: Test\nvalue: 42\n"
        with patch('logging.error') as mock_logging_error:
            self.assertEqual(extract_yaml_from_text(text), "name: Test\nvalue: 42")
            mock_logging_error.assert_called_once()

    def test_extract_yaml_empty(self):
        text = "```yaml\n```\n"
        self.assertEqual(extract_yaml_from_text(text), "")

    def test_extract_yaml_with_additional_backticks(self):
        text = "```yaml\nname: Test\nvalue: 42\n``````\n"
        expected_yaml = "name: Test\nvalue: 42"
        self.assertEqual(extract_yaml_from_text(text), expected_yaml)


class TestExtractJsonFromText(unittest.TestCase):

    def test_extract_json_with_backticks(self):
        text = "Some text before JSON block.\n```json\n{\"key\": \"value\"}\n```\nSome text after."
        expected_json = "{\"key\": \"value\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)

    def test_extract_json_with_single_quotes(self):
        text = "Some text before JSON block.\n'''json\n{\"key\": \"value\"}\n'''\nSome text after."
        expected_json = "{\"key\": \"value\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)

    def test_extract_json_within_python_block(self):
        text = "Some text before JSON block.\n```python\n{\"key\": \"value\"}\n```\nSome text after."
        expected_json = "{\"key\": \"value\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)

    def test_extract_json_with_missing_end_backticks(self):
        text = "Some text before JSON block.\n```json\n{\"key\": \"value\"}\n"
        with patch('logging.error') as mock_logging_error:
            self.assertEqual(extract_json_from_text(text), "")
            mock_logging_error.assert_called_once()

    def test_extract_json_with_missing_end_single_quotes(self):
        text = "Some text before JSON block.\n'''json\n{\"key\": \"value\"}\n"
        with patch('logging.error') as mock_logging_error:
            self.assertEqual(extract_json_from_text(text), "")
            mock_logging_error.assert_called_once()

    def test_extract_json_no_json_block(self):
        text = "There is no JSON block here."
        self.assertEqual(extract_json_from_text(text), text)

    def test_extract_json_empty_json_block(self):
        text = "```json\n```\n"
        self.assertEqual(extract_json_from_text(text), "")

    def test_extract_json_with_nested_delimiters(self):
        text = "```json\n{\"key\": \"value with `backticks` inside\"}\n```\n"
        expected_json = "{\"key\": \"value with `backticks` inside\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)

    def test_extract_json_with_text_after_closing_delimiter(self):
        text = "```json\n{\"key\": \"value\"}\n```\nSome text after closing delimiter."
        expected_json = "{\"key\": \"value\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)

    def test_extract_json_with_multiple_json_blocks(self):
        text = "```json\n{\"key1\": \"value1\"}\n```\nSome text.\n```json\n{\"key2\": \"value2\"}\n```\n"
        expected_json = "{\"key1\": \"value1\"}"
        self.assertEqual(extract_json_from_text(text), expected_json)


if __name__ == '__main__':
    unittest.main()
