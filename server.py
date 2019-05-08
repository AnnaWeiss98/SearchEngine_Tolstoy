#!/usr/bin/env python
from http.server import HTTPServer,BaseHTTPRequestHandler


body = '''
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=cp1251" />
        <title>Поиск</title>
    </head>
    <body>
     <form method='POST'>
     Искомое слово: <input type="text" name="findstr">
    <input type="submit" value="Найти">
    <p>
    <br>
    {}
    </p>
</form>
    </body>
</html>
'''

class web_server(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200) #responce that all ok
        self.end_headers()
        result = ''
        self.wfile.write(bytes(body.format(result),'cp1251'))

    def do_POST(self):
        self.do_GET()


if __name__== '__main__':

    print ('Start server.')
    httpd = HTTPServer(('localhost', 80), web_server)
    httpd.serve_forever()
