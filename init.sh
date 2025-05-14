#!/bin/bash

npm install

npm run dev &

python ./backend/manage.py runserver
