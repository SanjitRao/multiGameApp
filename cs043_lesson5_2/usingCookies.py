import wsgiref.simple_server
import http.cookies


def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8'),

               ('Set-Cookie', 'favoriteColor=red'),
               ('Set-Cookie', 'favoriteNumber=4'),
               ('Set-Cookie', 'name=Jason'),

               ]
    start_response('200 OK', headers)
    cookies = http.cookies.SimpleCookie()
    cookies.load('favoriteColor=red;favoriteNumber=4;name=Jason')
    response = ''
    for key in cookies:
        response += str(key+': '+ cookies[key].value +'\n')
    return [response.encode()]
    #Cookie parser goes here . . .


httpd = wsgiref.simple_server.make_server('', 8000, application)
debug = input('Please enter something: ')

print("Serving on port 8000...")

httpd.serve_forever()