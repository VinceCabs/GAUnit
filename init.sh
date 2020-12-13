#!/usr/bin/env bash

# From https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5

# https://developers.supportbee.com/blog/setting-up-cucumber-to-run-with-Chrome-on-Linux/
# https://gist.github.com/curtismcmullan/7be1a8c1c841a9d8db2c
# https://stackoverflow.com/questions/10792403/how-do-i-get-chrome-working-with-selenium-using-php-webdriver
# https://stackoverflow.com/questions/26133486/how-to-specify-binary-path-for-remote-chromedriver-in-codeception
# https://stackoverflow.com/questions/40262682/how-to-run-selenium-3-x-with-chrome-driver-through-terminal
# https://askubuntu.com/questions/760085/how-do-you-install-google-chrome-on-ubuntu-16-04

#Versions
# SELENIUM_STANDALONE_VERSION=3.9.1
# SELENIUM_SUBDIR=$(echo "$SELENIUM_STANDALONE_VERSION" | cut -d"." -f-2)

# Remove existing downloads and binaries so we can start from scratch.
# apt-get remove -y google-chrome-stable
# # rm ~/selenium-server-standalone-*.jar
# rm /usr/local/bin/chromedriver
# rm /usr/local/bin/selenium-server-standalone.jar

# Install dependencies.
apt-get update
apt-get install -y unzip default-jre xvfb libxi6 libgconf-2-4

# Install Chrome.
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "deb https://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y install google-chrome-stable

# # Install GeckoDriver
# # WIP 
# GECKO_DRIVER_VERSION=`curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest`
# wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
# tar -xvzf geckodriver* 
# chmod +x geckodriver

# Install ChromeDriver.
CHROME_DRIVER_VERSION=`curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P ~/
unzip ~/chromedriver_linux64.zip -d ~/
rm ~/chromedriver_linux64.zip
mv -f ~/chromedriver /usr/local/bin/chromedriver
chown root:root /usr/local/bin/chromedriver
chmod 0755 /usr/local/bin/chromedriver
# PATH="/chromedriver:${PATH}"

# Install BrowserMob Proxy
BMP_VERSION=2.1.4
# wget -O browsermob-proxy.zip https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-$BMP_VERSION/browsermob-proxy-$BMP_VERSION-bin.zip
wget -N https://github.com/lightbody/browsermob-proxy/releases/download/browsermob-proxy-$BMP_VERSION/browsermob-proxy-$BMP_VERSION-bin.zip -P ~/
unzip -q ~/browsermob-proxy-$BMP_VERSION-bin.zip -d ~/
rm ~/browsermob-proxy-$BMP_VERSION-bin.zip

mv -f ~/browsermob-proxy-$BMP_VERSION/bin ~/browsermob-proxy-$BMP_VERSION/lib ~/browsermob-proxy-$BMP_VERSION/ssl-support /usr/local/
