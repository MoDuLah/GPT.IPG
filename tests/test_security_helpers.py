from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMessageBox

from image_prompt_builder import ImagePromptBuilder, sanitize_prompt_text, validate_allowed_file_path


class PathValidationTests(unittest.TestCase):
    def test_allows_files_inside_allowed_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp)
            resolved = validate_allowed_file_path("prompt.txt", allowed)

        self.assertEqual(resolved, allowed.resolve() / "prompt.txt")

    def test_rejects_parent_directory_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp)
            with self.assertRaises(ValueError):
                validate_allowed_file_path(allowed / ".." / "outside.txt", allowed)

    def test_rejects_absolute_path_outside_allowed_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp) / "allowed"
            allowed.mkdir()
            outside = Path(tmp) / "outside.txt"
            with self.assertRaises(ValueError):
                validate_allowed_file_path(outside, allowed)

    def test_rejects_missing_parent_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp)
            with self.assertRaises(ValueError):
                validate_allowed_file_path(allowed / "missing" / "prompt.txt", allowed)


class PromptSanitizationTests(unittest.TestCase):
    def test_removes_control_and_hidden_format_characters(self) -> None:
        sanitized = sanitize_prompt_text(" title\x00\r\nnext\u202ehidden\ttext ")

        self.assertEqual(sanitized, "title\nnexthidden text")

    def test_single_line_mode_collapses_newlines(self) -> None:
        sanitized = sanitize_prompt_text("  one\r\ntwo\tthree  ", preserve_newlines=False)

        self.assertEqual(sanitized, "one two three")

    def test_truncates_to_requested_length(self) -> None:
        sanitized = sanitize_prompt_text("abcdef", max_chars=4)

        self.assertEqual(sanitized, "abcd")


class FileSinkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self) -> None:
        self._critical = QMessageBox.critical
        QMessageBox.critical = lambda *args, **kwargs: None

    def tearDown(self) -> None:
        QMessageBox.critical = self._critical

    def test_write_text_rejects_outside_path_without_writing(self) -> None:
        window = ImagePromptBuilder()
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp) / "allowed"
            allowed.mkdir()
            outside = Path(tmp) / "outside.txt"

            window.write_text(outside, "blocked", allowed)

            self.assertFalse(outside.exists())

    def test_write_text_allows_inside_path(self) -> None:
        window = ImagePromptBuilder()
        with tempfile.TemporaryDirectory() as tmp:
            allowed = Path(tmp)
            inside = allowed / "inside.txt"

            window.write_text(inside, "ok", allowed)

            self.assertEqual(inside.read_text(encoding="utf-8"), "ok")


if __name__ == "__main__":
    unittest.main()
