#!/bin/sh
cd /app/data
git pull origin master
python /app/update.py