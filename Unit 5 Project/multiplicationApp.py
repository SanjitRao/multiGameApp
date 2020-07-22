import wsgiref.simple_server
import urllib.parse
import sqlite3
import http.cookies
import random

connection = sqlite3.connect('users.db')
stmt = "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
cursor = connection.cursor()
result = cursor.execute(stmt)
r = result.fetchall()
if (r == []):
    exp = 'CREATE TABLE users (username,password)'
    connection.execute(exp)


def application(environ, start_response):
    headers = [('Content-Type', 'text/html; charset=utf-8')]

    path = environ['PATH_INFO']
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    un = params['username'][0] if 'username' in params else None
    pw = params['password'][0] if 'password' in params else None

    if path == '/register' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ?', [un]).fetchall()
        if user:
            start_response('200 OK', headers)
            return ['Sorry, username {} is taken'.format(un).encode()]
        else:
            connection.execute('INSERT INTO users VALUES (?, ?)', [un, pw])
            headers.append(('Set-Cookie', 'counter=0:0'))
            connection.commit()
            start_response('200 OK', headers)
            return ['Username {} was been successfully registered. <a href="/">Login</a>'.format(un).encode()]
            #[INSERT CODE HERE. Use SQL commands to insert the new username and password into the table that has been created. Print a message saying the username was created successfully]

    elif path == '/login' and un and pw:
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()
        if user:
            headers.append(('Set-Cookie', 'session={}:{}'.format(un, pw)))
            start_response('200 OK', headers)
            return ['User {} successfully logged in. <a href="/account">Account</a>'.format(un).encode()]
        else:
            start_response('200 OK', headers)
            return ['Incorrect username or password'.encode()]

    elif path == '/logout':
        headers.append(('Set-Cookie', 'session=0; expires=Thu, 01 Jan 1970 00:00:00 GMT'))
        start_response('200 OK', headers)
        return ['Logged out. <a href="/">Login</a>'.encode()]

    elif path == '/account':
        start_response('200 OK', headers)

        if 'HTTP_COOKIE' not in environ:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        cookies = http.cookies.SimpleCookie()
        cookies.load(environ['HTTP_COOKIE'])
        if 'session' not in cookies:
            return ['Not logged in <a href="/">Login</a>'.encode()]

        [un, pw] = cookies['session'].value.split(':')
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', [un, pw]).fetchall()

        #This is where the game begins. This section of code is only executed if the login form works, and if the user is successfully logged in
        if user:

            #cookies = http.cookies.SimpleCookie()
            if 'HTTP_COOKIE' in environ:
                cookies = http.cookies.SimpleCookie()
                cookies.load(environ['HTTP_COOKIE'])
                if 'counter' not in cookies:
                    headers.append(('Set-Cookie', 'counter=0:0'))
            correct = int(cookies['counter'].value.split(':')[0])
            wrong = int(cookies['counter'].value.split(':')[1])

                #[INSERT CODE FOR COOKIES HERE]

            page = '<!DOCTYPE html><html><head><title>Multiply with Score</title></head><body>'
            if 'factor1' in params and 'factor2' in params and 'answer' in params:
                if int(params['factor1'][0])*int(params['factor2'][0]) == int(params['answer'][0]):
                    page = '<p style="background-color: lightgreen"> CORRECT! {} * {} = {}</p><hr>'.format(params['factor1'], params['factor2'], params['answer'])
                    correct +=1
                    headers.append(('Set-Cookie', 'counter={}:{}'.format(correct, wrong)))

                else:
                    page ='<p style="background-color: red"> INCORRECT! {} * {} DOESN\'T EQUAL {}</p><hr>'.format(params['factor1'], params['factor2'], params['answer'])
                    wrong +=1
                    headers.append(('Set-Cookie', 'counter={}:{}'.format(correct, wrong)))

            elif 'reset' in params:
                correct = 0
                wrong = 0

            headers.append(('Set-Cookie', 'score={}:{}'.format(correct, wrong)))

            f1 = random.randrange(10) + 1
            f2 = random.randrange(10) + 1

            page = page + '<h1>What is {} x {}</h1>'.format(f1, f2)
            answer = f1*f2
            answerList = [answer]
            for i in range(3):
                a = random.randint(0,101)
                answerList.append(a)
            #[INSERT CODE HERE. Create a list that stores f1*f2 (the right answer) and 3 other random answers]
            random.shuffle(answerList)

            hyperlink = '<a href="/account?username={}&amp;password={}&amp;factor1={}&amp;factor2={}&amp;answer={}">{}:{}</a><br>'

            #page = ''' <{#hyperlink[answer={}]}>{Letter}:{randomanswer from list}</a><br> #todo this the format for the hyperlinks
            letterList = ['A','B','C','D']
            for i in range(len(letterList)):
                page += hyperlink.format(un,pw,f1,f2,answerList[i], letterList[i], answerList[i])

            #[INSERT CODE HERE. Create the 4 answer hyperlinks here using string formatting.]

            page += '''<h2>Score</h2>
            Correct: {}<br>
            Wrong: {}<br>
            <a href="/account?reset=true">Reset</a>
            </body></html>'''.format(correct, wrong)

            return [page.encode()]
        else:
            return ['Not logged in. <a href="/">Login</a>'.encode()]

    elif path == '/':
        page = '''<form action = "/login"
                style = "background-color:gold" >
                <h1> Login </h1>
                Username <input type = "text" name = "username"> <br>
                Password <input type = "password" name = "password"> <br>
                <input type = "submit" value = "Log in">
            </form>
            <hr>
            <form action = "/register" style = "background-color:gold">
            <h1> Register </h1>
            Username <input type = "text" name = "username"> <br>
            Password <input type = "password" name = "password"> <br>
            <input type = "submit" value = "Register">
            </form>'''

        ###INSERT CODE HERE. Create two forms. One is to log in with a username and password, the other to register a new username and password.###
        start_response('200 OK', headers)
        return [page.encode()]

    else:
        start_response('404 Not Found', headers)
        return ['Status 404: Resource not found'.encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
httpd.serve_forever()