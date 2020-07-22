import urllib.parse
import wsgiref.simple_server

def application(environ, start_response):
    fortune = [
        'Be a generous friend and a fair enemy.',
        '傷心有多少 在乎就有多少',
        'A bargain is something you don\'t need at a price you can\'t resist.',
        'A single conversation with a wise man is better than ten years of study.',
        'All the water in the world can\'t sink a ship unless it gets inside.',
        'Ask a friend to join you on your next voyage.',
        'Back away from individuals who are impulsive.',
        'Bad luck and misfortune will follow you all your days.',
        'Be a good friend and a fair enemy.',
        'Bread today is better than cake tomorrow.',
        'Circumstance does not make the man; it reveals him to himself.',
        'Cookie says, "You crack me up".',
        'Do not be covered in sadness or be fooled in happiness they both must exist.',
        'Do not fear what you don\'t know.',
        'Do not follow where the path may lead. Go where there is no path...and leave a trail.']

    headers = [('Content-Type', 'text/plain; charset=utf-8')]


    start_response('200 OK', headers)
    cookie = urllib.parse.parse_qs(environ['QUERY_STRING'])
    cookie_number = int(cookie['id'][0])
    return [fortune[cookie_number].encode()]


httpd = wsgiref.simple_server.make_server('', 8000, application)
print('This task was successful')
httpd.serve_forever()
