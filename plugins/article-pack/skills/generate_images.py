#!/usr/bin/env python3
"""
Generate images using OpenRouter

Usage:
    python generate_images.py --prompt "your prompt" --output image.png
    python generate_images.py --prompt "your prompt" --output image.png --model pro

Models:
    gemini (default) - Gemini 3 Pro: best for text, infographics, editorial
    pro              - FLUX 2 Pro: stylized, illustrated
    flex             - FLUX 2 Flex: photorealistic
"""

import argparse
import base64
import os
import re
import requests
import json

MODELS = {
    "pro": "black-forest-labs/flux.2-pro",
    "flex": "black-forest-labs/flux.2-flex",
    "gemini": "google/gemini-3-pro-image-preview",
}


def save_base64_image(data_url: str, output_path: str) -> None:
    """Save a base64 data URL to file."""
    if data_url.startswith("data:"):
        match = re.match(r'data:image/\w+;base64,(.+)', data_url)
        if match:
            image_data = base64.b64decode(match.group(1))
        else:
            raise ValueError("Invalid data URL format")
    else:
        image_data = base64.b64decode(data_url)

    with open(output_path, "wb") as f:
        f.write(image_data)
    print(f"✓ Saved to {output_path}")


def generate_image(prompt: str, output_path: str, model: str = "gemini") -> str:
    """Generate image using OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set")

    model_id = MODELS.get(model, model)  # Allow full model ID too
    print(f"Using model: {model_id}")

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "modalities": ["image", "text"]
        })
    )
    response.raise_for_status()
    result = response.json()

    if result.get("choices"):
        message = result["choices"][0]["message"]
        if message.get("images"):
            for image in message["images"]:
                image_url = image["image_url"]["url"]  # Base64 data URL
                save_base64_image(image_url, output_path)
                return output_path
        else:
            raise RuntimeError(f"No images in response: {message}")
    else:
        raise RuntimeError(f"Unexpected response format: {result}")


def main():
    parser = argparse.ArgumentParser(description="Generate images via OpenRouter (Gemini/FLUX)")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt")
    parser.add_argument("--output", "-o", required=True, help="Output file path")
    parser.add_argument("--model", "-m", default="gemini", choices=["pro", "flex", "gemini"],
                        help="Model to use: gemini (default), pro, or flex")

    args = parser.parse_args()

    print(f"Generating: {args.prompt[:60]}{'...' if len(args.prompt) > 60 else ''}")
    generate_image(args.prompt, args.output, args.model)


if __name__ == "__main__":
    main()
