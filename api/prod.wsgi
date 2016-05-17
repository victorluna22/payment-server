# file configuration of apache mod_wsgi
from django.conf import settings
import os, sys, site
from os.path import abspath, join, dirname
project_name = "api"
root_dir = abspath(join(dirname(__file__), '..'))
sys.path.append(root_dir)
sys.path.append(join(root_dir, project_name))
os.environ["DJANGO_SETTINGS_MODULE"]= 'settings.prod'
import django.core.handlers.wsgi
#application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
