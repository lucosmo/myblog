import os
import sys
from urllib.parse import unquote
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

load_dotenv()

sys.path.append(os.getcwd())

DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")

def application(environ, start_response):
    environ["PATH_INFO"] = (
        unquote(environ["PATH_INFO"]).encode("utf-8").decode("iso-8859-1")
    )
    _application = get_wsgi_application()
    return _application(environ, start_response)
