#!/bin/bash

# Update and install Chromium and Chromedriver
apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    curl \
    unzip

# Set environment variables for Chromium and Chromedriver
export CHROME_BIN=/usr/bin/chromium
export CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Clean up to reduce image size
apt-get clean && rm -rf /var/lib/apt/lists/*
