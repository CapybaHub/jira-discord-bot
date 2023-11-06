#!/usr/bin/env bash

# Create .env file
if [ ! -f .env ]; then
    cp env.example .env
fi

docker-compose build

# Create migrations
docker-compose run --rm web python manage.py makemigrations

# Run migrations
docker-compose run --rm web python manage.py migrate