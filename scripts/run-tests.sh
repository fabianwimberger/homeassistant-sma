#!/bin/bash
# Run the project's unit tests

echo "=== Running unit tests ==="
cd "$(dirname "$0")/.."

# Check if pytest is available
if command -v pytest &> /dev/null; then
    pytest tests/ -v
elif [ -f ".venv/bin/pytest" ]; then
    .venv/bin/pytest tests/ -v
else
    echo "pytest not found. Trying to install dependencies..."
    if command -v uv &> /dev/null; then
        uv pip install -e .
        uv pip install -r requirements_test.txt
        uv run pytest tests/ -v
    elif command -v pip &> /dev/null; then
        pip install -e .
        pip install -r requirements_test.txt
        pytest tests/ -v
    else
        echo "Error: Cannot find pytest or package manager."
        exit 1
    fi
fi
