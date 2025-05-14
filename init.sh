#!/bin/bash

# 1. Iniciar el frontend (Vue.js) - Crear el build para producción

cd fronted/               # Cambiar al directorio del frontend
npm install               # Instalar las dependencias del frontend
npm run build             # Crear el build de producción

# 2. Copiar los archivos estáticos de Vue.js al backend
# Si decides servir los archivos estáticos desde Django, puedes copiar los archivos del build (dist/) a la carpeta estática de Django.
cp -r dist/* ../backend/static/

# 3. Regresar al directorio raíz
cd ../

# 4. Ejecutar comandos para Django

python ./backend/manage.py makemigrations
python ./backend/manage.py migrate
# python ./backend/script_final.py  # Descomenta si tienes algún script que ejecutar antes de iniciar el servidor.

# 5. Iniciar el servidor de Django en el puerto adecuado (usando la variable PORT proporcionada por Render)
echo "Iniciando el servidor de Django en el puerto $PORT"
python ./backend/manage.py runserver 0.0.0.0:$PORT
