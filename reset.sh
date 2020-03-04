#!/bin/sh

echo ''
echo 'Hard reset...'
pipenv run ampy --port /dev/ttyUSB0 --delay 1 reset --hard