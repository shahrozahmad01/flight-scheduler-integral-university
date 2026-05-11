#!/usr/bin/env bash
# Usage: ./setup_venv.sh /path/to/python3.11
PYTHON=${1:-python3}
echo "Using Python: $PYTHON"
"$PYTHON" --version || { echo "Python not found"; exit 1; }
VENV_DIR=".venv"
echo "Creating venv in $VENV_DIR"
"$PYTHON" -m venv "$VENV_DIR" || { echo "Failed to create venv"; exit 1; }
VENV_PY="$VENV_DIR/bin/python"
echo "Upgrading pip..."
"$VENV_PY" -m pip install --upgrade pip
echo "Installing requirements..."
"$VENV_PY" -m pip install -r "$(dirname "$0")/../requirements.txt"
echo "Done. Activate: source $VENV_DIR/bin/activate"
