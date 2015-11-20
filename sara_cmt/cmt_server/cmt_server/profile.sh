#!/bin/bash

DJANGO_SETTINGS_MODULE=cmt_server.settings python -m cProfile -o cmt_server.profile debugserver.py
