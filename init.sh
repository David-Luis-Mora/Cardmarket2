#!/bin/bash
# Iniciar el frontend (Node.js)
cd fronted/               # Cambiar al directorio del frontend
npm install               # Instalar las dependencias del frontend
npm run dev -- --port 8000 &   # Ejecutar el servidor de desarrollo en segundo plano en el puerto 8000

# Regresar al directorio raíz
cd ../

# Ejecutar comandos para Django
echo "Iniciando el backend (Django)"
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate
# python ./backend/script_final.py

# Iniciar el servidor de Django (en el puerto 8000)
python ./backend/manage.py runserver 0.0.0.0:8000
