# AGENTS.md

## Project purpose
This repository contains a small Python project that generates Instagram carousel images using Pillow (PIL).

## Structure
- `src/carousel_generator/processor.py`  
  Core image functions:
  - `resize_to_4_5(image)` -> center-crop + resize to 1080x1350
  - `add_gradient(image, start_color, end_color)` -> top-to-bottom RGBA overlay
  - `add_text(image, text, style)` -> wrapped, centered caption near bottom
- `src/carousel_generator/cli.py`  
  Command-line interface for one-step slide generation.
- `requirements.txt`  
  Python dependency list.

## Setup
1. Create/activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run
Use module mode so imports resolve cleanly from repository root:

```bash
PYTHONPATH=src python -m carousel_generator.cli input.jpg output.jpg --text "Your caption"
```

Example with custom font options:

```bash
PYTHONPATH=src python -m carousel_generator.cli input.jpg output.jpg \
  --text "Slide title" \
  --font-size 84 \
  --font-path ./fonts/YourFont.ttf \
  --gradient-alpha 180
```

## Development notes for agents
- Keep output dimensions at 4:5 (`1080x1350`) unless task requirements change.
- Preserve function-level composability in `processor.py` (single-responsibility helpers first, pipeline wrappers second).
- When extending text rendering, keep line wrapping based on pixel width rather than character count.
- Prefer adding tests for image dimensions, mode, and deterministic output behavior where practical.
