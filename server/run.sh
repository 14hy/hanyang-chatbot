#!/usr/bin/env bash

docker-compose up -d --force-recreate --build
docker-compose logs -f