#!/usr/bin/env zsh

source $HOME/.zshrc
source $(venv)/bin/activate

$(venv)/bin/uwsgi --socket 127.0.0.1:8080 -w wsgi:app
