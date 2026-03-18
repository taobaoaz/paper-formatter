#!/bin/bash
cd "$(dirname "$0")"
nohup python3 launcher.py > /dev/null 2>&1 &
disown
exit
