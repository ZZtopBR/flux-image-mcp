#!/usr/bin/env bash
# Run generate_image.py inside the venv
# Usage: ./run.sh "a mountain at sunrise" --output photo.png

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -f "$SCRIPT_DIR/.env" ]; then
    set -a; source "$SCRIPT_DIR/.env"; set +a
fi

source "$SCRIPT_DIR/venv/bin/activate"
python "$SCRIPT_DIR/generate_image.py" "$@"
