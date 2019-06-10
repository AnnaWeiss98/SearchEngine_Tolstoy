from http.server import HTTPServer,BaseHTTPRequestHandler
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
from searchengine import SearchEngine

#from tokenwindow import Windows

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
        """
        Creates a simple HTML page with a field and a button.
        """

        self.send_response(200)
        self.end_headers()
        result = ''
        self.wfile.write(bytes(body.format(result),'cp1251'))


    def do_POST(self):
        """
        Seends search results in response to the search query.
        """

        global search_engine

        postvars = {}
        ctype, pdict = parse_header(self.headers['content-type'])

        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)

        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            str_ =  self.rfile.read(length).decode()
            postvars = parse_qs(str_, keep_blank_values=1, strict_parsing=False, encoding='cp1251')

        self.send_response(200)
        self.end_headers()

        findstr = postvars['findstr'][0]
        result = ''

        res = search_engine.find_supplemented_window(findstr, 2)
        for k in res:
            result += k
            result += '<ul>'
            for v in res[k]:
                result += '<li>'+v.get_BB_string()+'</li>'

            result +='</ul>'
        self.wfile.write(bytes(body.format(result),'cp1251'))


if __name__== '__main__':

    search_engine = SearchEngine('database')
    print ('Start server.')
    httpd = HTTPServer(('localhost', 80), web_server)
    httpd.serve_forever()
