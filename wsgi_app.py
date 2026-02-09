import os
import sys
from pathlib import Path

# Adiciona o diretório atual ao path para garantir que 'core' seja encontrado
# quando o gunicorn roda a partir da raiz
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
