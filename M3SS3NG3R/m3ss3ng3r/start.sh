#!/bin/bash

sleep 5
uvicorn main:app --reload --host 0.0.0.0 --port 8000
alembic revision --autogenerate -m commit
alembic upgrade head


