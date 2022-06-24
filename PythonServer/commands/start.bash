#!/bin/bash

nohup gunicorn --bind 0.0.0.0:5000 wsgi:app &

# Last Result -
# nohup <venv>/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app &