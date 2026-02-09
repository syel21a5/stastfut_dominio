import os
import sys

# Adiciona o diretório do projeto ao sys.path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Obtém a aplicação WSGI diretamente do Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
