#!/usr/bin/env bash
branch=$1

git fetch --all
git reset --hard origin/"$branch"
docker-compose down
docker-compose up -d
