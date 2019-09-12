from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from cgi import parse_header, parse_multipart
from searchengine import SearchEngine

body = '''
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=cp1251" />
        <title>Поиск</title>
    </head>
    <body>
     <form method='POST'>
     Начальная запись: <input type="text" name="offset" value="0" size="4"><br>
     Число результатов на странице: <input type="text" name="limit" value="1" size="4"><br>
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
        self.wfile.write(bytes(body.format(result), 'cp1251'))

    def do_POST(self):
        """
        Seends search results in response to the search query.
        """
        postvars = {}
        ctype, pdict = parse_header(self.headers['content-type'])

        if ctype == 'multipart/form-data':
            postvars = parse_multipart(self.rfile, pdict)

        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            str_ = self.rfile.read(length).decode()
            postvars = parse_qs(str_, keep_blank_values=1, strict_parsing=False, encoding='cp1251')

        self.send_response(200)
        self.end_headers()

        findstr = postvars['findstr'][0]
        limit = int(postvars['limit'][0])
        offset = int(postvars['offset'][0])
        result = self.gen_page(findstr, limit, offset)
        self.wfile.write(bytes(body.format(result), 'cp1251'))

    def gen_page(self, findstr, limit, offset):

        global search_engine

        result = ''
        res = search_engine.find_supplemented_window(findstr, 2)
        count = 0

        for k in res:
            filename = k
            filename += '<ul>'
            for v in res[k]:
                if count >= offset and count < offset + limit:
                    if filename != '':
                        if result != '':
                            result += '</ul>'
                        result += filename
                        filename = ''
                    result += '<li>' + v.get_BB_string() + '</li>'
                elif count > offset + limit - 1:
                    break

                count += 1

            if count > offset + limit - 1:
                break

        return result


if __name__ == '__main__':
    search_engine = SearchEngine('database')
    print ('Start server.')
    httpd = HTTPServer(('localhost', 80), web_server)
    httpd.serve_forever()
