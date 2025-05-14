#!/bin/bash

npm install

npm run dev &

python ./backend/manage.py makemigrations

python ./backend/manage.py migrate

python ./backend/script_final.py

python ./backend/manage.py runserver
