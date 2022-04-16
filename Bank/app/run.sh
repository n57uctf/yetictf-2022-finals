#!/bin/bash
gunicorn -b 0.0.0.0:8080 main:app & gunicorn  -b 127.0.0.1:8081 history:app
