#!/bin/sh
gunicorn app:app --threads 10 -b 0.0.0.0:5000