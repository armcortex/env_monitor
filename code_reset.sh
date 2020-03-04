#!/bin/sh

pipenv run esptool.py --port /dev/ttyUSB0 erase_flash

# pipenv run esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 ./ref/esp8266-20190529-v1.11.bin            # old version
pipenv run esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect -fm dio 0 ./ref/esp8266-20190529-v1.11.bin      # new version

sleep 3

