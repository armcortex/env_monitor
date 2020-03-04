#!/bin/sh

sudo chmod 777 /dev/ttyUSB0
cd env_monitor

echo ''
echo 'Start uploading code...'
# Envi monitor
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put boot.py
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put main.py
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put config.py
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put config.json
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put sht20.py
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put wdt_simple.py
pipenv run ampy --port /dev/ttyUSB0 --baud 115200 put influxdb.py

pipenv run ampy --port /dev/ttyUSB0 --delay 1 ls

