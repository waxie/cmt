from wsgiref.simple_server import make_server
#from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application
httpd = make_server('', 8000, get_wsgi_application())
httpd.serve_forever()
