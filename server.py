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
     <form method='POST'> #tells that we send a request into server by method POST
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

        self.send_response(200) #responce that all ok, 200 - successful request
        self.end_headers()
        result = ''
        self.wfile.write(bytes(body.format(result),'cp1251'))

    def do_POST(self): #preform for realisation method POST
        self.do_GET()


if __name__== '__main__': 
    '''it's for pythons working by itself, if we use the programm like plug-ins (added modul), 
    this part doesn't work'''

    print ('Start server.')
    httpd = HTTPServer(('localhost', 80), web_server) #the creation of server itself with adress localhost and port 80(standart)
    ''' web_server inherits from klass BaseHTTPRequestHandler, hear we redefine two methods do_POST and do_GET, we 
    can work with requests by ourself'''
    httpd.serve_forever() #this method lets the server working by helps of brauser
