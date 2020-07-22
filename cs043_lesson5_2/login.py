import wsgiref.simple_server
import urllib.parse
import sqlite3

connection = sqlite3.connect('newUSERS.db')
connection.execute('CREATE TABLE IF NOT EXISTS regUsers (username, password)')
cursor = connection.cursor()

def application(environ, start_response):
    headers = [('Content-Type', 'text/plain; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None
    print(str(un + pw))
    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM regUsers WHERE username = ? AND password = ?', [un, pw])### YOUR CODE HERE TO CHECK IF USERNAME IS TAKEN ###
        userList = user.fetchall()
        if len(userList) == 0:

            connection.execute('INSERT INTO regUsers VALUES (?, ?)', [un, pw])
            connection.commit()
            start_response('200 OK', headers)
            return ['Username {} was successfully registered'.format(un).encode()]

        else:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]



    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM regUsers WHERE username = ? AND password = ?', [un, pw])
        userList=user.fetchall()

        if len(userList) >1:
            start_response('200 OK', headers)
            return ['User {} successfully logged in'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['[LOGIN] Incorrect username or password'.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]

httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()