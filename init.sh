#!/bin/bash
cd fronted/
npm install
npm run dev &
cd ../

python ./backend/manage.py makemigrations

python ./backend/manage.py migrate

python ./backend/script_final.py

python ./backend/manage.py runserver
