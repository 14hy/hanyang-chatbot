#!/usr/bin/env bash
branch=$1

git fetch --all
git reset --hard origin/"$branch"
docker run -d -v "$PWD":/app -p 5000:5000 -e env=prod --name hanyang-chatbot hanyang-chatbot python app.py
