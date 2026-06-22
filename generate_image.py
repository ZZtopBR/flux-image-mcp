#!/usr/bin/env python3
"""
Standalone CLI — generate images with FLUX.1-schnell without Claude.
Usage: python generate_image.py "a mountain at sunrise" --output photo.png
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from huggingface_hub import InferenceClient

OUTPUT_DIR = Path.home() / "generated_images"
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"
PROVIDER   = "nscale"

_SIZE_DIMS = {
    "1:1":  (1024, 1024),
    "16:9": (1360, 768),
    "9:16": (768,  1360),
    "4:3":  (1024, 768),
    "3:4":  (768,  1024),
}


def get_api_key() -> str:
    key = os.environ.get("HF_TOKEN", "").strip()
    if not key:
        print(
            "Error: HF_TOKEN environment variable is not set.\n"
            "Get your token at https://huggingface.co/settings/tokens\n"
            "Then: export HF_TOKEN=hf_your_token_here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def generate(prompt: str, output: str | None, count: int, size: str) -> list[str]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    client = InferenceClient(provider=PROVIDER, api_key=get_api_key())
    width, height = _SIZE_DIMS[size]

    print(f"Generating {count} image(s) with {MODEL_NAME}...")
    saved = []
    for i in range(count):
        img = client.text_to_image(prompt, model=MODEL_NAME, width=width, height=height)
        if output and count == 1:
            filename = OUTPUT_DIR / output
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = OUTPUT_DIR / f"image_{ts}_{i + 1}.png"
        img.save(str(filename))
        saved.append(str(filename))
        print(f"Saved: {filename}")
    return saved


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images with FLUX.1-schnell")
    parser.add_argument("prompt", help="Image description")
    parser.add_argument("--output", "-o", help="Output filename")
    parser.add_argument("--count", "-n", type=int, default=1, choices=[1, 2, 3, 4])
    parser.add_argument("--size", "-s", default="1:1",
                        choices=["1:1", "16:9", "9:16", "4:3", "3:4"],
                        help="Image aspect ratio")
    args = parser.parse_args()
    paths = generate(args.prompt, args.output, args.count, args.size)
    sys.exit(0 if paths else 1)
