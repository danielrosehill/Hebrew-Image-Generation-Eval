#!/usr/bin/env python3
"""Create hero composite image for README with proper RTL Hebrew text."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def reverse_hebrew(text):
    """Reverse Hebrew text for proper visual display in LTR rendering context."""
    # PIL renders LTR, so Hebrew characters need to be reversed for correct visual order
    return text[::-1]

def create_hero_composite():
    # Images to include: 2 good (top row), 2 bad (bottom row)
    images_info = [
        # (path, model_name, is_good)
        ("outputs/shalom/gemini-3-pro.png", "Gemini 3 Pro", True),
        ("outputs/firgun/wan-2-5.png", "Wan 2.5", True),
        ("outputs/shalom/ideogram-v2.png", "Ideogram V2", False),
        ("outputs/firgun/recraft-v3.png", "Recraft V3", False),
    ]

    # Configuration
    thumb_width = 800
    thumb_height = 450  # 16:9 aspect
    label_height = 50
    padding = 8
    cols = 2
    rows = 2

    # Calculate total dimensions
    total_width = cols * thumb_width + (cols + 1) * padding
    total_height = rows * (thumb_height + label_height) + (rows + 1) * padding

    # Create composite image
    composite = Image.new('RGB', (total_width, total_height), color='black')
    draw = ImageDraw.Draw(composite)

    # Try to load a good font for Hebrew
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansHebrew-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    ]

    font = None
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, 28)
            break
        except:
            continue

    if font is None:
        font = ImageFont.load_default()

    # Small font for checkmarks
    small_font = None
    for fp in font_paths:
        try:
            small_font = ImageFont.truetype(fp, 60)
            break
        except:
            continue

    for idx, (img_path, model_name, is_good) in enumerate(images_info):
        row = idx // cols
        col = idx % cols

        x = padding + col * (thumb_width + padding)
        y = padding + row * (thumb_height + label_height + padding)

        # Load and resize image
        img = Image.open(img_path)
        img = img.resize((thumb_width, thumb_height), Image.LANCZOS)

        # Paste image
        composite.paste(img, (x, y))

        # Add checkmark or X overlay
        check_x = x + thumb_width - 70
        check_y = y + thumb_height - 70
        if is_good:
            draw.text((check_x, check_y), "✓", fill=(0, 255, 0), font=small_font)
        else:
            draw.text((check_x, check_y), "✗", fill=(255, 0, 0), font=small_font)

        # Add label with white background
        label_y = y + thumb_height
        draw.rectangle([x, label_y, x + thumb_width, label_y + label_height], fill='black')

        # Create label text - just model name
        label_text = model_name

        # Center the text
        bbox = draw.textbbox((0, 0), label_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_x = x + (thumb_width - text_width) // 2
        text_y = label_y + (label_height - (bbox[3] - bbox[1])) // 2

        draw.text((text_x, text_y), label_text, fill='white', font=font)

    # Save
    output_path = "samples/hero-composite.png"
    composite.save(output_path, quality=95)
    print(f"Created: {output_path}")

if __name__ == "__main__":
    create_hero_composite()
