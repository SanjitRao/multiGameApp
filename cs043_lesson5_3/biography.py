import html
import wsgiref.simple_server


def application(environ, start_response):
   # headers = [('Content-Type', 'text/html; charset=utf-8')]
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    path = environ['PATH_INFO']

    if path == '/biography':
        page = '''<!DOCTYPE html>
        <html>
        <head><title>Biography</title></head>
        <body>
        <h1>This Great Story of Mine</h1>
        <h2>Intro</h2>
        <p> "This is the story of will the g0" </p>
        <h1> Amen </h1>
        </body>
        </html>'''

    return [page.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
