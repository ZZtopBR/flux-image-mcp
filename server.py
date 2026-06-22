#!/usr/bin/env python3
"""
MCP server — exposes FLUX.1-schnell image generation as a native Claude tool.

Each user needs their own HF_TOKEN (free at huggingface.co/settings/tokens).
Set it in the Claude Desktop config or in a .env file next to this script.
"""

import os
from datetime import datetime
from pathlib import Path

from huggingface_hub import InferenceClient
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

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

mcp = FastMCP(
    "flux-image-generator",
    instructions=(
        "Use the generate_image tool whenever the user asks to create, draw, "
        "generate, or visualize an image. Pass the user's description as the "
        "prompt. Choose the size based on context: 16:9 for landscapes/wallpapers, "
        "9:16 for phone wallpapers/portraits, 1:1 for general use. "
        "After calling the tool, respond ONLY with a single short sentence confirming "
        "the image was generated (in the same language the user used), followed by the "
        "saved path on a new line. Do NOT describe the image content."
    ),
)


def _is_desktop() -> bool:
    return not (os.environ.get("TERM") or os.environ.get("TERM_PROGRAM"))


def _get_client() -> InferenceClient:
    key = os.environ.get("HF_TOKEN", "").strip()
    if not key:
        raise RuntimeError(
            "HF_TOKEN is not set.\n"
            "Get your free token at https://huggingface.co/settings/tokens\n"
            "and add it to the Claude Desktop config (see README)."
        )
    return InferenceClient(provider=PROVIDER, api_key=key)


@mcp.tool()
def generate_image(prompt: str, size: str = "1:1") -> list[TextContent]:
    """
    Generate an image from a text description using FLUX.1-schnell.

    Args:
        prompt: Detailed description of the image to generate.
        size:   Aspect ratio. Options: 1:1 | 16:9 | 9:16 | 4:3 | 3:4.
    """
    if size not in _SIZE_DIMS:
        raise ValueError(f"Invalid size '{size}'. Choose from: {', '.join(_SIZE_DIMS)}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    client = _get_client()
    width, height = _SIZE_DIMS[size]
    img = client.text_to_image(prompt, model=MODEL_NAME, width=width, height=height)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"image_{ts}.png"
    img.save(str(filename))

    if _is_desktop():
        try:
            os.startfile(str(filename))
        except Exception:
            pass

    return [TextContent(type="text", text=f"Image saved to: {filename}")]


if __name__ == "__main__":
    mcp.run()
