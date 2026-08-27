"""Unit tests for PromptNormalizer."""

import unittest

from backend.firewall.normalizer import PromptNormalizer


class TestPromptNormalizer(unittest.TestCase):
    """Tests for prompt text normalization behavior."""

    def setUp(self) -> None:
        self.normalizer = PromptNormalizer()

    def test_normal_text(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("hello world"),
            "hello world",
        )

    def test_uppercase_text(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("HELLO WORLD"),
            "hello world",
        )

    def test_leading_and_trailing_whitespace(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("  hello world  "),
            "hello world",
        )

    def test_multiple_spaces(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("hello    world"),
            "hello world",
        )

    def test_tabs(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("hello\tworld"),
            "hello world",
        )

    def test_newlines(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("hello\nworld"),
            "hello world",
        )

    def test_mixed_whitespace(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("  hello \t\n  world  "),
            "hello world",
        )

    def test_empty_input(self) -> None:
        self.assertEqual(self.normalizer.normalize(""), "")

    def test_whitespace_only_input(self) -> None:
        self.assertEqual(self.normalizer.normalize("   \t\n  "), "")

    def test_punctuation_preserved(self) -> None:
        self.assertEqual(
            self.normalizer.normalize("Hello, World!"),
            "hello, world!",
        )


if __name__ == "__main__":
    unittest.main()
