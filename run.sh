#!/bin/bash

echo "\n#Installing dependencies..\n"
cat requirements.txt
pip install -r requirements.txt > /dev/null

echo "\n#Starting Redis\n"
docker run -d -p 6379:6379 redis:alpine >/dev/null

echo "\n#Starting Reverse Proxy Flask server\n"
python src/reverseProxyApp.py

