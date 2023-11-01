#!/usr/bin/env bash

if [ ! -d venv ]; then
    mkdir venv && python3 -m venv venv
fi

source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
