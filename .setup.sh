#!/bin/bash

set -e

VENV_DIR=".venv"

echo "Iniciando setup del entorno Python..."

if ! command -v python3 &> /dev/null
then
    echo "❌ Python3 no está instalado. Por favor instálalo antes de continuar."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Creando entorno virtual en ./$VENV_DIR ..."
    python3 -m venv "$VENV_DIR"
else
    echo "Entorno virtual ya existe."
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

# Verificar que requirements.txt exista
if [ ! -f "requirements.txt" ]; then
    echo "No se encontró requirements.txt, omitiendo instalación de dependencias."
else
    echo "Instalando dependencias desde requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

echo "Setup completado. Entorno listo para usar."
