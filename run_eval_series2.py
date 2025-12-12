#!/usr/bin/env python3
"""
Series 2: Hebrew text rendering evaluation with HEBREW prompts.
Testing if models respond better when the entire prompt is in Hebrew.
"""

import os
import fal_client
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from pathlib import Path

# Subset of models to test in Series 2
MODELS = [
    ("fal-ai/nano-banana-pro", "Nano Banana Pro"),
    ("fal-ai/wan-25-preview/text-to-image", "Wan 2.5"),
    ("fal-ai/flux-2", "Flux 2"),
    ("fal-ai/flux/dev", "Flux Dev"),
]

# Hebrew prompts - entire prompt in Hebrew
WORDS = [
    ("shalom", "שלום", "גרפיקה עם המילה שלום בגופן גדול"),
    ("firgun", "פירגון", "גרפיקה עם המילה פירגון בגופן גדול"),
]

OUTPUT_BASE = Path("outputs-series2")


def annotate_image(img_path: Path, model_name: str, output_path: Path):
    """Add model name annotation below the image."""
    img = Image.open(img_path)

    bar_height = 60
    new_img = Image.new("RGB", (img.width, img.height + bar_height), "white")
    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), model_name, font=font)
    text_width = bbox[2] - bbox[0]
    x = (new_img.width - text_width) // 2
    y = img.height + (bar_height - (bbox[3] - bbox[1])) // 2

    draw.text((x, y), model_name, fill="black", font=font)
    new_img.save(output_path)
    print(f"  Annotated: {output_path}")


def generate_image(model_id: str, model_name: str, prompt: str, word_name: str):
    """Generate image using fal.ai API."""
    output_dir = OUTPUT_BASE / word_name
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = model_name.lower().replace(" ", "-").replace(".", "-")
    raw_path = output_dir / f"{safe_name}_raw.png"
    final_path = output_dir / f"{safe_name}.png"

    if final_path.exists():
        print(f"  Skipping {model_name} - already exists")
        return True

    print(f"  Generating with {model_name}...")
    print(f"  Prompt: {prompt}")

    try:
        result = fal_client.subscribe(
            model_id,
            arguments={
                "prompt": prompt,
                "image_size": {"width": 1920, "height": 1080},
            },
        )

        # Get image URL from result
        if isinstance(result, dict):
            if "images" in result and len(result["images"]) > 0:
                img_url = result["images"][0].get("url") or result["images"][0]
            elif "image" in result:
                img_url = result["image"].get("url") or result["image"]
            elif "output" in result:
                img_url = result["output"]
            else:
                print(f"  Unexpected result format: {result.keys()}")
                return False
        else:
            img_url = str(result)

        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img.save(raw_path)

        annotate_image(raw_path, model_name, final_path)
        raw_path.unlink()

        return True

    except Exception as e:
        print(f"  ERROR with {model_name}: {e}")
        return False


def main():
    print("=" * 60)
    print("Series 2: Hebrew Prompts Evaluation")
    print("Testing with prompts written entirely in Hebrew")
    print("=" * 60)

    results = {}

    for word_name, hebrew_word, prompt in WORDS:
        print(f"\nGenerating images for: {hebrew_word} ({word_name})")
        print(f"Hebrew prompt: {prompt}")
        print("-" * 50)

        results[word_name] = {}

        for model_id, model_name in MODELS:
            success = generate_image(model_id, model_name, prompt, word_name)
            results[word_name][model_name] = success

    print("\n" + "=" * 60)
    print("SERIES 2 SUMMARY")
    print("=" * 60)

    for word_name, word_results in results.items():
        print(f"\n{word_name}:")
        for model, success in word_results.items():
            status = "✓ generated" if success else "✗ failed"
            print(f"  {status} - {model}")


if __name__ == "__main__":
    main()
