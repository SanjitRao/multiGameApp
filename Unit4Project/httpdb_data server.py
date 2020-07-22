import wsgiref.simple_server
import urllib.parse
from cs043_lesson2_2.database import Simpledb


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])

    db = Simpledb('datafile.txt')

    if path == '/insert':
        start_response('200 OK', headers)
        i = db.insert(params['key'][0], params['value'][0])
        if i:
            return ['Inserted'.encode()]
        else:
            return ['Was not inserted properly, try again'.encode()]
    elif path == '/select':  # todo figure out if this works
        start_response('200 OK', headers)
        s = db.select_one(params['key'][0])
        if s[0]:
            return [s[1].encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/delete':  # todo need to complete this function
        start_response('200 OK', headers)
        d = db.delete(params['key'][0])
        if d:
            return ['DELETED'.encode()]
        else:
            return ['NULL'.encode()]
    elif path == '/update':
        start_response('200 OK', headers)
        up = db.update(params['key'][0], params['value'][0])
        if up:
            return ['UPDATED'.encode()]  # todo see if i dont need to encode this and line 32
        else:
            return ['NULL'.encode()]
    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()
