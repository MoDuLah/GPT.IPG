from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtWidgets import QApplication, QMessageBox

from image_prompt_builder import (
    ImagePromptBuilder,
    SECTIONS,
    SubjectProfilesField,
    sanitize_prompt_text,
    validate_allowed_file_path,
)


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


class SubjectProfilesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.app = QApplication.instance() or QApplication([])

    def test_subject_profiles_follow_count_and_save_names(self) -> None:
        profiles = SubjectProfilesField()
        profiles.set_count(3)
        profiles.profiles[0]["name"].setText("Neo")
        profiles.profiles[1]["name"].setText("Trinity")
        profiles.profiles[2]["name"].setText("Morpheus")

        data = profiles.data()

        self.assertEqual([item["name"] for item in data], ["Neo", "Trinity", "Morpheus"])
        self.assertEqual(profiles.tabs.tabText(1), "Trinity")

    def test_subject_profiles_render_named_prompt_blocks(self) -> None:
        profiles = SubjectProfilesField()
        profiles.set_count(2)
        profiles.set_data(
            [
                {"name": "Neo", "role": "hero", "action": "dodging bullets"},
                {"name": "Agent Smith", "role": "antagonist", "expression": {"selected": "Authoritative"}},
            ]
        )

        rendered = profiles.value()

        self.assertIn("Subject 1: Neo", rendered)
        self.assertIn("- Action: dodging bullets", rendered)
        self.assertIn("Subject 2: Agent Smith", rendered)
        self.assertIn("- Expression: Authoritative", rendered)

    def test_subject_profiles_restore_hidden_profiles_when_count_increases(self) -> None:
        profiles = SubjectProfilesField()
        profiles.set_count(3)
        profiles.profiles[1]["name"].setText("Trinity")
        profiles.set_count(1)
        profiles.set_count(3)

        self.assertEqual(profiles.profiles[1]["name"].text(), "Trinity")


class PresetVocabularyTests(unittest.TestCase):
    def test_preset_selected_values_exist_in_builder_controls(self) -> None:
        try:
            result = subprocess.run(
                ["git", "ls-files", "presets/*.json"],
                check=True,
                capture_output=True,
                text=True,
            )
        except (OSError, subprocess.CalledProcessError):
            self.skipTest("Tracked preset discovery requires Git")
        preset_paths = [Path(line) for line in result.stdout.splitlines() if line.strip()]
        if not preset_paths:
            self.skipTest("No tracked preset JSON files in this checkout")

        field_defs = {}
        for _section, definitions in SECTIONS.items():
            for key, _label, field_type, config in definitions:
                field_defs[key] = (field_type, config)

        combo_options = {
            key: set(config)
            for key, (field_type, config) in field_defs.items()
            if field_type == "combo"
        }
        option_values = {
            key: {item for group in config.values() for item in group}
            for key, (field_type, config) in field_defs.items()
            if field_type == "options"
        }
        missing = []

        for path in preset_paths:
            data = json.loads(path.read_text(encoding="utf-8"))
            for key, value in data.get("fields", {}).items():
                if key in combo_options:
                    selected = value.get("selected") if isinstance(value, dict) else value
                    if isinstance(selected, str) and selected.strip() and selected.strip() not in combo_options[key]:
                        missing.append(f"{path.name}:{key}:{selected.strip()}")
                elif key in option_values:
                    selected_items = value.get("selected") if isinstance(value, dict) else []
                    if isinstance(selected_items, str):
                        selected_items = [
                            item.strip()
                            for item in selected_items.replace(";", ",").split(",")
                            if item.strip()
                        ]
                    for item in selected_items or []:
                        item = str(item).strip()
                        if item and item not in option_values[key]:
                            missing.append(f"{path.name}:{key}:{item}")

        self.assertEqual([], missing)


if __name__ == "__main__":
    unittest.main()
