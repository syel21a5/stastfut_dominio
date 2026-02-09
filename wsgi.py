import os
import sys

# Add the project root to the python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

from core.wsgi import application
