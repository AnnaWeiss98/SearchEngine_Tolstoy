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
     <table>
     {}
     <tr>
     <td>Искомое слово:</td>
     <td><input type="text" name="findstr"></td>
     <td><input type="submit" value="Найти"></td>
     </tr>
     </table>
    {}
    </form>
    </body>
</html>
'''

form_limit ='''
     <tr>
     <td colspan="2" align="center"> Для файла {} </td>
     </tr>
     <tr>
     <td>Начальная запись:</td>
     <td><input type="text" name="doc{}offset" value="{}" size="4"></td>
     </tr>
     <tr>
     <td>Число результатов на странице:</td>
     <td><input type="text" name="doc{}limit" value="{}" size="4"></td>
     </tr>
'''

class custom_handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Creates a simple HTML page with a field and a button.
        """
        self.send_response(200)
        self.end_headers()
        result = ''
        limit_str =''
        for l in range (0,self.server.countKeys):
            limit_str += form_limit.format(str(l), str(l), "0", str(l), "10")

        self.wfile.write(bytes(body.format(limit_str, result), 'cp1251'))

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

        limit_str, result = self.gen_page(postvars)
        self.wfile.write(bytes(body.format(limit_str, result), 'cp1251'))

    def gen_page(self, postvars):

        result = ''
        limit_str =''

        findstr = postvars['findstr'][0]
        res = self.server.search_engine.find_supplemented_window(findstr, 2)
        
        """
        i - step number in cycle for dynamic formation of the input field
        """
        for i,k in enumerate(res.keys()):
            filename = k
            filename += '<ul>'    
            count = 0
            limit = int(postvars['doc'+str(i)+'limit'][0])
            offset = int(postvars['doc'+str(i)+'offset'][0])
            limit_str += form_limit.format(str(i), str(i), str(offset), str(i), str(limit))
            for v in res[k]:
                if offset <= count < offset + limit:
                    if filename != '':
                        if result != '':
                            result += '</ul>'
                        result += filename
                        filename = ''
                    result += '<li>' + v.get_BB_string() + '</li>'
                elif count > offset + limit - 1:
                    break

                count += 1

        return limit_str, result


if __name__ == '__main__':

    httpd = HTTPServer(('localhost', 80), custom_handler)
    httpd.search_engine = SearchEngine('database')
    httpd.countKeys =  len(httpd.search_engine.database.get('Толстой')) #countKeys - a number of files in db
    print ('Start server.')
    httpd.serve_forever()
