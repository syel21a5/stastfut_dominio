import os
import sys

# Adiciona o diretório atual ao sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importa a aplicação WSGI do Django localizada em core/wsgi.py
from core.wsgi import application
