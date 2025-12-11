#!/usr/bin/env python3
"""Hebrew text rendering evaluation across image generation models."""

import os
import fal_client
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from pathlib import Path

# API key should be set via environment variable FAL_KEY

MODELS = [
    ("fal-ai/flux-2", "Flux 2"),
    ("fal-ai/flux-2-pro", "Flux 2 Pro"),
    ("fal-ai/flux/dev", "Flux Dev"),
    ("fal-ai/imagen4/preview", "Imagen 4"),
    ("fal-ai/gemini-3-pro-image-preview", "Gemini 3 Pro"),
    ("fal-ai/nano-banana-pro", "Nano Banana Pro"),
    ("fal-ai/wan-25-preview/text-to-image", "Wan 2.5"),
    ("fal-ai/qwen-image", "Qwen Image"),
    ("fal-ai/ideogram/v2", "Ideogram V2"),
    ("fal-ai/stable-diffusion-v35-large", "SD 3.5 Large"),
    ("fal-ai/recraft/v3/text-to-image", "Recraft V3"),
    ("fal-ai/aura-flow", "Aura Flow"),
]

WORDS = [
    ("shalom", "שלום", "A banner graphic with the word שלום written in large font"),
    ("firgun", "פירגון", "A banner graphic with the word פירגון written in large font"),
]

def normalize_model_name(model_id: str) -> str:
    """Convert model ID to display name."""
    name = model_id.split("/")[-1]
    name = name.replace("-", " ").replace("_", " ")
    return name.title()

def annotate_image(img_path: Path, model_name: str, output_path: Path):
    """Add model name annotation below the image."""
    img = Image.open(img_path)

    # Create new image with white bar at bottom
    bar_height = 60
    new_img = Image.new("RGB", (img.width, img.height + bar_height), "white")
    new_img.paste(img, (0, 0))

    # Add text
    draw = ImageDraw.Draw(new_img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except:
        font = ImageFont.load_default()

    # Center the text
    bbox = draw.textbbox((0, 0), model_name, font=font)
    text_width = bbox[2] - bbox[0]
    x = (new_img.width - text_width) // 2
    y = img.height + (bar_height - (bbox[3] - bbox[1])) // 2

    draw.text((x, y), model_name, fill="black", font=font)
    new_img.save(output_path)
    print(f"  Annotated: {output_path}")

def generate_image(model_id: str, model_name: str, prompt: str, word_name: str):
    """Generate image using fal.ai API."""
    output_dir = Path(f"outputs/{word_name}")
    output_dir.mkdir(parents=True, exist_ok=True)

    safe_name = model_name.lower().replace(" ", "-").replace(".", "-")
    raw_path = output_dir / f"{safe_name}_raw.png"
    final_path = output_dir / f"{safe_name}.png"

    if final_path.exists():
        print(f"  Skipping {model_name} - already exists")
        return True

    print(f"  Generating with {model_name}...")

    try:
        # Different models have different parameter names
        if "imagen" in model_id.lower() or "gemini" in model_id.lower():
            result = fal_client.subscribe(
                model_id,
                arguments={
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                },
            )
        elif "ideogram" in model_id.lower():
            result = fal_client.subscribe(
                model_id,
                arguments={
                    "prompt": prompt,
                    "aspect_ratio": "16:9",
                },
            )
        elif "recraft" in model_id.lower():
            result = fal_client.subscribe(
                model_id,
                arguments={
                    "prompt": prompt,
                    "image_size": {"width": 1920, "height": 1080},
                },
            )
        else:
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

        # Download and save
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))
        img.save(raw_path)

        # Annotate
        annotate_image(raw_path, model_name, final_path)

        # Remove raw file
        raw_path.unlink()

        return True

    except Exception as e:
        print(f"  ERROR with {model_name}: {e}")
        return False

def main():
    print("Hebrew Image Generation Evaluation")
    print("=" * 50)

    results = {}

    for word_name, hebrew_word, prompt in WORDS:
        print(f"\nGenerating images for: {hebrew_word} ({word_name})")
        print("-" * 40)

        results[word_name] = {}

        for model_id, model_name in MODELS:
            success = generate_image(model_id, model_name, prompt, word_name)
            results[word_name][model_name] = success

    # Print summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)

    for word_name, word_results in results.items():
        print(f"\n{word_name}:")
        for model, success in word_results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {model}")

if __name__ == "__main__":
    main()
