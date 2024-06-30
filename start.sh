#!/bin/bash

# Install Playwright browsers
python3 -m playwright install
python3 -m playwright install-deps

# Start the Flask server
python3 api.py
