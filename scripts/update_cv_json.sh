#!/bin/zsh

# Script to update the CV JSON file from the markdown CV
# Author: Yuan Chen

echo "$(clear)"

# Set the base directory to the repository root
#BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Define file paths
CV_JSON="_data/cv.json"
CONFIG_FILE="_config.yml"

# Check if the Python script exists
PYTHON_SCRIPT="scripts/cv_markdown_to_json.py"
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "Error: Python script not found at $PYTHON_SCRIPT"
  exit 1
fi

# Check if the markdown CV exists
#if [ ! -f "$CV_MARKDOWN" ]; then
#  echo "Error: Markdown CV not found at $CV_MARKDOWN"
#  exit 1
#fi

#echo "base_dir: "
#echo "cv_json: $CV_JSON"
#echo "config: $CONFIG_FILE"
#echo "cv_markdown: $CV_MARKDOWN"
#echo "\n"
#echo "python_script: $PYTHON_SCRIPT"
#echo "python version: $(python3 --version)"
#echo "pip list: $(python3 -m pip list)"

# Run the Python script to generate cv
echo "Generating CV..."
python3 "$PYTHON_SCRIPT" --output "$CV_JSON" --config "$CONFIG_FILE"

# Check if the conversion was successful
#if [ $? -eq 0 ]; then
#  echo "Successfully updated CV JSON file at $CV_JSON"

#  # Optional: Build the Jekyll site to see the changes
#  echo "Would you like to build the Jekyll site to see the changes? (y/n)"
#  read -r answer
#  if [[ "$answer" =~ ^[Yy]$ ]]; then
#    echo "Building Jekyll site..."
#    cd "" && bundle exec jekyll serve
#  fi
#else
#  echo "Error: Failed to update CV JSON file"
#  exit 1
#fi

exit 0
