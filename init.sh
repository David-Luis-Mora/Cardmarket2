#!/bin/bash

# Iniciar el frontend (Vue.js)
echo "Iniciando el frontend (Vue.js)"

# Cambiar al directorio del frontend (ajustar el nombre si es necesario)
cd ./fronted

# Instalar las dependencias de Vue.js
npm install

# Si realmente necesitas npm-run-all, descomenta la siguiente línea
npm install npm-run-all --save-dev

# Compilar los archivos estáticos de Vue.js
npm run build-only

# Mover los archivos estáticos compilados de Vue.js a la carpeta static de Django
echo "Moviendo archivos estáticos de Vue.js a la carpeta static de Django"
cp -r dist/* ../backend/static/

# Regresar al directorio raíz
cd ../

# Ejecutar comandos para Django
echo "Iniciando el backend (Django)"

# Realizar las migraciones de la base de datos
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate

# Ejecutar cualquier script adicional de Django (si lo tienes)
# python ./backend/script_final.py

# Iniciar el servidor de Django
echo "Iniciando el servidor de Django en el puerto $PORT"
python ./backend/manage.py runserver 0.0.0.0:$PORT

