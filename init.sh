#!/bin/bash
# 1. Iniciar el frontend (Vue.js) - Crear el build para producción
echo "Creando el build del frontend (Vue.js)"
cd fronted/               # Cambiar al directorio del frontend
npm install               # Instalar las dependencias del frontend
npm run build             # Crear el build de producción

# 2. Verificar si la carpeta static/ existe en el backend (si no, crearla)
echo "Verificando y creando la carpeta static en el backend"
if [ ! -d "../backend/static" ]; then
  mkdir -p ../backend/static  # Crear la carpeta si no existe
  echo "Carpeta static creada"
else
  echo "La carpeta static ya existe"
fi

# 3. Mover los archivos estáticos generados de Vue.js a la carpeta static/ en el backend (Django)
echo "Moviendo archivos estáticos de Vue.js a la carpeta static de Django"
cp -r dist/* ../backend/static/  # Copiar todo el contenido de dist/ a static/

# 4. Regresar al directorio raíz
cd ../

# 5. Ejecutar comandos para Django
echo "Iniciando el backend (Django)"
python ./backend/manage.py makemigrations
python ./backend/manage.py migrate
# python ./backend/script_final.py  # Descomenta si tienes algún script que ejecutar antes de iniciar el servidor.

# 6. Iniciar el servidor de Django en el puerto adecuado (usando la variable PORT proporcionada por Render)
echo "Iniciando el servidor de Django en el puerto $PORT"
python ./backend/manage.py runserver 0.0.0.0:$PORT
