"""Core image-processing functions for Instagram carousel slides."""

from __future__ import annotations

from dataclasses import dataclass

from PIL import Image, ImageDraw, ImageFont

TARGET_WIDTH = 1080
TARGET_HEIGHT = 1350


@dataclass(frozen=True)
class TextStyle:
    """Configuration for text rendering."""

    fill: tuple[int, int, int] = (255, 255, 255)
    size: int = 72
    margin: int = 80
    font_path: str | None = None


def resize_to_4_5(image: Image.Image) -> Image.Image:
    """
    Resize + crop an image to Instagram's 4:5 portrait ratio.

    Output size defaults to 1080x1350, which is carousel friendly.
    """
    target_ratio = TARGET_WIDTH / TARGET_HEIGHT
    source_ratio = image.width / image.height

    if source_ratio > target_ratio:
        # Source is wider than target ratio. Crop horizontally.
        new_width = int(image.height * target_ratio)
        left = (image.width - new_width) // 2
        box = (left, 0, left + new_width, image.height)
    else:
        # Source is taller than target ratio. Crop vertically.
        new_height = int(image.width / target_ratio)
        top = (image.height - new_height) // 2
        box = (0, top, image.width, top + new_height)

    cropped = image.crop(box)
    return cropped.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)


def add_gradient(
    image: Image.Image,
    start_color: tuple[int, int, int, int] = (0, 0, 0, 0),
    end_color: tuple[int, int, int, int] = (0, 0, 0, 170),
) -> Image.Image:
    """Overlay a top-to-bottom gradient on an image."""
    base = image.convert("RGBA")
    gradient = Image.new("RGBA", base.size, color=0)
    draw = ImageDraw.Draw(gradient)
    width, height = base.size

    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(int(start_color[i] + (end_color[i] - start_color[i]) * t) for i in range(4))
        draw.line([(0, y), (width, y)], fill=color)

    return Image.alpha_composite(base, gradient)


def add_text(
    image: Image.Image,
    text: str,
    style: TextStyle | None = None,
) -> Image.Image:
    """Add centered caption text near the bottom of the image."""
    if not text:
        return image

    style = style or TextStyle()
    output = image.convert("RGBA")
    draw = ImageDraw.Draw(output)
    if style.font_path:
        font = ImageFont.truetype(style.font_path, style.size)
    else:
        try:
            # DejaVu is bundled with Pillow and is available in most setups.
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", style.size)
        except OSError:
            font = ImageFont.load_default()

    # Keep text inside the image by wrapping on pixel width.
    max_text_width = output.width - (style.margin * 2)
    wrapped_lines: list[str] = []
    current_words: list[str] = []

    for word in text.split():
        candidate = " ".join([*current_words, word]).strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_text_width:
            current_words.append(word)
            continue

        if current_words:
            wrapped_lines.append(" ".join(current_words))
        current_words = [word]

    if current_words:
        wrapped_lines.append(" ".join(current_words))

    if not wrapped_lines:
        wrapped_lines = [text]

    line_height = draw.textbbox((0, 0), "Ag", font=font)[3]
    spacing = 12
    block_height = (line_height * len(wrapped_lines)) + (spacing * (len(wrapped_lines) - 1))
    y = output.height - style.margin - block_height

    for line in wrapped_lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_width = bbox[2] - bbox[0]
        x = (output.width - line_width) // 2
        draw.text((x, y), line, fill=style.fill, font=font)
        y += line_height + spacing

    return output


def build_slide(image: Image.Image, text: str = "") -> Image.Image:
    """Convenience pipeline: resize to 4:5, add gradient, then add text."""
    resized = resize_to_4_5(image)
    with_gradient = add_gradient(resized)
    return add_text(with_gradient, text=text)
