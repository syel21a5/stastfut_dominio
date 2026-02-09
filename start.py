import os
import sys

# Garante que o diretório atual está no path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Configura as settings do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Obtém a aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
