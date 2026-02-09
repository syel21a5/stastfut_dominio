import os
import sys

# Adiciona o diretório atual ao path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Configura o settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Cria a aplicação
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
