"""Command-line entry point for generating carousel slides."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

from .processor import TextStyle, add_gradient, add_text, resize_to_4_5


def build_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate an Instagram carousel image (4:5) from a source image."
    )
    parser.add_argument("input", type=Path, help="Path to input image")
    parser.add_argument("output", type=Path, help="Path to output image")
    parser.add_argument("--text", default="", help="Caption text to add")
    parser.add_argument("--font-path", default=None, help="Optional .ttf font file path")
    parser.add_argument("--font-size", type=int, default=72, help="Caption font size")
    parser.add_argument(
        "--margin", type=int, default=80, help="Text margin from edges/bottom in pixels"
    )
    parser.add_argument(
        "--gradient-alpha",
        type=int,
        default=170,
        help="Bottom alpha value (0-255) for black gradient overlay",
    )
    return parser


def main() -> None:
    """Run CLI workflow."""
    parser = build_parser()
    args = parser.parse_args()

    if not args.input.exists():
        raise SystemExit(f"Input file does not exist: {args.input}")

    if not 0 <= args.gradient_alpha <= 255:
        raise SystemExit("gradient-alpha must be between 0 and 255")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(args.input) as source:
        resized = resize_to_4_5(source)
        with_gradient = add_gradient(
            resized,
            start_color=(0, 0, 0, 0),
            end_color=(0, 0, 0, args.gradient_alpha),
        )
        styled = add_text(
            with_gradient,
            text=args.text,
            style=TextStyle(size=args.font_size, margin=args.margin, font_path=args.font_path),
        )
        styled.convert("RGB").save(args.output)

    print(f"Saved carousel slide to: {args.output}")


if __name__ == "__main__":
    main()
