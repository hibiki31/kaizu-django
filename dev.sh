#!/bin/bash
docker-compose down
docker-compose build
docker-compose up -d
docker-compose run kaizu-app python3 manage.py migrate
docker-compose run kaizu-app python3 manage.py collectstatic