#!/bin/bash

cd "$(dirname "$0")"
poetry run python nps/main.py "$@"
