# Instagram Carousel Generator (Python + PIL)

Small project for generating Instagram carousel images.

## Features

- Resize/crop source images to Instagram 4:5 format (`1080x1350`)
- Add a vertical black gradient overlay
- Add centered caption text near the bottom

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
PYTHONPATH=src python -m carousel_generator.cli input.jpg output.jpg \
  --text "Your headline here" \
  --font-size 72 \
  --gradient-alpha 170
```

### Optional arguments

- `--font-path /path/to/font.ttf`: use a custom TrueType font
- `--margin 80`: control caption spacing from edges/bottom

## Programmatic usage

```python
from PIL import Image
from carousel_generator.processor import resize_to_4_5, add_gradient, add_text

image = Image.open("input.jpg")
image = resize_to_4_5(image)
image = add_gradient(image)
image = add_text(image, "Slide title")
image.convert("RGB").save("output.jpg")
```