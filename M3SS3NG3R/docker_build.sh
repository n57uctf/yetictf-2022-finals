#!/bin/bash

docker-compose up --build -d
docker-compose exec web alembic revision --autogenerate -m "commit"
docker-compose exec web alembic upgrade head
