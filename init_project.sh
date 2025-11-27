#!/bin/bash
echo "🚀 Initializing spacecraft-dynamics-control project..."

# Create virtual environment if it doesn't exist
if [ ! -d "../.venv" ]; then
    echo "Creating virtual environment..."
    python -m venv ../.venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ../.venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Try different installation methods
echo "Installing project..."
if python setup.py develop 2>/dev/null; then
    echo "✅ Installed via setup.py develop"
elif pip install -e . 2>/dev/null; then
    echo "✅ Installed via pip install -e ."
else
    echo "⚠️  Using manual installation..."
    python install_manual.py
fi

# Run verification
echo "Running project verification..."
python check_project.py

echo "🎉 Project initialization complete!"
echo "To activate the environment: source ../.venv/bin/activate"
