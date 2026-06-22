# FLUX Image Generator — MCP Tool for Claude

Generate images directly inside Claude using [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) — one of the best open-source image models available today.

Claude doesn't generate images natively. This tool bridges that gap: install it once and Claude will be able to create images on demand from any conversation.

---

## How it works

This is an **MCP server** (Model Context Protocol — Anthropic's open standard for extending Claude with external tools). Once installed, Claude detects image requests automatically and calls this server in the background. You just talk to Claude normally.

```
You: "Generate a photo of a futuristic city at night, 16:9"
Claude: [calls generate_image tool] → saves the image locally and confirms
```

---

## Prerequisites

- **Python 3.10+** — check with `python3 --version`
- **Claude Desktop** or **Claude Code CLI**
- **HuggingFace account** (free) — for your API token

---

## Installation

### 1. Clone and set up

```bash
git clone https://github.com/ZZtopBR/flux-image-mcp.git
cd flux-image-mcp
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get your HuggingFace token

1. Create a free account at [huggingface.co](https://huggingface.co)
2. Go to [Settings → Tokens](https://huggingface.co/settings/tokens)
3. Create a **Read** token and copy it
4. Accept the [FLUX.1-schnell license](https://huggingface.co/black-forest-labs/FLUX.1-schnell)

### 3. Connect to Claude

#### Claude Code CLI

```bash
export HF_TOKEN=hf_your_token_here
claude mcp add flux-image-generator -s user \
  -- /path/to/flux-image-mcp/venv/bin/python \
     /path/to/flux-image-mcp/server.py
```

#### Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flux-image-generator": {
      "command": "/path/to/flux-image-mcp/venv/bin/python",
      "args": ["/path/to/flux-image-mcp/server.py"],
      "env": { "HF_TOKEN": "hf_your_token_here" }
    }
  }
}
```

Restart Claude Desktop. A hammer icon confirms the tool is connected.

---

## Usage

Just ask Claude naturally:

```
"Generate an image of an astronaut riding a horse on Mars"
"Create a 16:9 wallpaper of a Japanese temple in autumn"
"Draw a minimalist logo for a coffee shop"
```

### Aspect ratios

| Option | Resolution  | Best for                        |
|--------|-------------|---------------------------------|
| `1:1`  | 1024 × 1024 | Social media, general use       |
| `16:9` | 1360 × 768  | Wallpapers, YouTube thumbnails  |
| `9:16` | 768 × 1360  | Phone wallpapers, Stories       |
| `4:3`  | 1024 × 768  | Presentations, classic photos   |
| `3:4`  | 768 × 1024  | Portraits, book covers          |

Images are saved to `~/generated_images/`.

---

## Standalone CLI

Works without Claude too:

```bash
python generate_image.py "a futuristic city" --size 16:9 --count 2
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Tool not in Claude Code | Run from inside repo folder; check `echo $HF_TOKEN` |
| No hammer in Desktop | Quit + relaunch; verify absolute paths; check JSON syntax |
| `HF_TOKEN is not set` | Export token or add to Desktop config `env` block |
| 403 from HuggingFace | Accept the model license on the HF model page |
| Slow generation | 10–30s is normal for the free API |

---

## License

MIT

---

*Built with [FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) by Black Forest Labs and [MCP](https://modelcontextprotocol.io) by Anthropic.*
