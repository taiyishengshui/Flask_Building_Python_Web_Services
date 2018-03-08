#/usr/bin/python3
from wsgiref.simple_server import make_server
from crimemap import app
httpd = make_server('', 8000, app)
print('Servring HTTP on port 8000..')
httpd.serve_forever()
