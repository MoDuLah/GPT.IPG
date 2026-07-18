# Image Prompt Builder

A PySide6 desktop app for building structured image-generation prompts, negative prompts, editing instructions, continuity notes, and compact prompt variants.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python image_prompt_builder.py
```

Or double-click `run_image_prompt_builder.bat`.

The app can save and load JSON presets, export generated prompt data, copy the active output tab to the clipboard, and save output tabs as text files. File dialogs are scoped to app-owned folders: `presets/` for presets, `outputs/` for text output, and `exports/` for generated JSON exports.

Image Setup includes a monitor-position picker. Subject appearance, hair, eyes, clothing, and accessories include checkbox option pickers with optional custom notes.
