#!/bin/bash


# Wait for containers to be up and running
sleep 5

# Create a virtual environment
python3 -m venv spoofpy

# Activate the virtual environment
source spoofpy/bin/activate

# Install dependencies
pip install -r requirements.txt 

# Run the application
python3 spoof.py