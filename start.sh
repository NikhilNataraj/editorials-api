#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python3 -m playwright install
python3 -m playwright install-deps
