#!/bin/bash

# Iniciar el frontend (Vue.js)
echo "Iniciando el frontend (Vue.js)"

# Cambiar al directorio del frontend
cd ./fronted

# Instalar dependencias
npm install

# Compilar solo el frontend sin type-check
npm run build-only

# Mover archivos del build de Vue al backend de Django
echo "Moviendo archivos estáticos de Vue.js a Django"
mkdir -p ../backend/static/
cp -r ./dist/assets ../backend/static/

mkdir -p ../backend/templates/
cp ./dist/index.html ../backend/templates/index.html

# Volver al directorio raíz
cd ../

# Iniciar el backend
echo "Iniciando el backend (Django)"
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate

# Iniciar el servidor de Django (puerto por variable de entorno o 8000 por defecto)
PORT=${PORT:-8000}
echo "Iniciando el servidor de Django en el puerto $PORT"
python ./backend/manage.py runserver 0.0.0.0:$PORT

