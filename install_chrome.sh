#!/bin/bash

# Update and install Chromium and Chromedriver
apt-get update && apt-get install -y \
    chromium-driver \
    chromium \
    curl \
    unzip

# Clean up to reduce image size
apt-get clean && rm -rf /var/lib/apt/lists/*
