#!/bin/bash

# Update package lists and install necessary packages
apt-get update
apt-get install -y wget gnupg unzip

# Download and install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -f install -y

# Ensure Google Chrome is available in the PATH
ln -s /usr/bin/google-chrome-stable /usr/local/bin/google-chrome

# Download and install ChromeDriver
CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv -f chromedriver /usr/local/bin/chromedriver
chmod 0755 /usr/local/bin/chromedriver
