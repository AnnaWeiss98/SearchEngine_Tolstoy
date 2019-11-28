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
     <tr>
     <td>Searchword:</td>
     <td><input type="text" name="findstr" value="{0}">
         <input type="hidden" name="prev_findstr" value="{0}">
     </td>
     <td><input type="submit" value="Search"></td>
     <tr>
     <td><input type="submit" name="action" value="begin" {5} ></td>
     <td><input type="submit" name="action" value="back" {5} ></td>
     <td><input type="submit" name="action" value="forward" {4} ></td> 
     <td><input type="hidden" name="offset" value="{1}" size="4"></td>
     </tr>
     <tr>
     <td>Count tom:</td>
     <td><input type="text" name="limit" value="{2}" size="4">
         <input type="hidden" name="limit_prev" value="{2}" size="4">
     </td>
     </tr>
     </table>
     {3}
    </form>
    </body>
</html>
'''

form_limit = '''
     <table>
     <tr>
     <td colspan="2" align="center"> Для файла {0} </td>
     </tr>
     <tr>
     <td><input type="submit" name="action{1}" value="begin" {6} ></td>
     <td><input type="submit" name="action{1}" value="back" {6} ></td>
     <td><input type="submit" name="action{1}" value="forward" {5} ></td> 
     <td><input type="hidden" name="doc{1}offset" value="{2}" size="4"></td>
     </tr>
     <tr>
     <td>a number of results on the page:</td>
     <td><input type="text" name="doc{1}limit" value="{3}" size="4">
         <input type="hidden" name="doc{1}limit_prev" value="{3}" size="4">
     </td>
     </table>
     {4}
 '''


class custom_handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """
        Creates a simple HTML page with a field and a button.
        """
        self.send_response(200)
        self.end_headers()
        result = ''
        self.wfile.write(bytes(body.format('', '0', '4', result, 'disabled', 'disabled'), 'cp1251'))

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

        print (postvars)
        self.wfile.write(bytes(self.gen_page(postvars), 'cp1251'))

    def get_int(self, value, def_value):
        result = def_value
        try:
            result = int(value)
        except ValueError:
            pass
        return result

    def get_offset(self, act, offset, delta):

        res = offset
        if act == 'forward':
            res += delta
        elif act == 'back':
            res -= delta
        elif act == 'begin':
            res = 0

        if res < 0:
            res = 0

        return res

    def gen_page(self, postvars):

        result = ''  # Result boby page
        isNew = False  # Flag is New data for findstr or action for files or limits for files

        findstr = postvars['findstr'][0]
        limit = self.get_int(postvars['limit'][0], 4)
        offset = self.get_int(postvars['offset'][0], 0)

        # if  press button navigation in files parametrs
        if 'action' in postvars:
            offset = self.get_offset(postvars['action'][0], offset, limit)
            isNew = True

        # if  findstr is changed or limits for files canged
        if postvars['findstr'][0] != postvars['prev_findstr'][0] or postvars['limit'][0] != postvars['limit_prev'][0]:
            offset = 0
            isNew = True

        o = []
        l = []
        for ind in range(0, limit + 1):
            if 'doc' + str(ind) + 'offset' in postvars:

                limit_doc = self.get_int(postvars['doc' + str(ind) + 'limit'][0], 5)
                offset_doc = self.get_int(postvars['doc' + str(ind) + 'offset'][0], 0)

                # if press button navigation in quote
                if 'action' + str(ind) in postvars:
                    offset_doc = self.get_offset(postvars['action' + str(ind)][0], offset_doc, limit_doc)

                # if changed limits in currend quotes
                if postvars['doc' + str(ind) + 'limit_prev'][0] != postvars['doc' + str(ind) + 'limit_prev'][0]:
                    offset_doc = 0

                if isNew:
                    offset_doc = 0
                    limit_doc = 5


                o.append(offset_doc)
                l.append(limit_doc + 1)
            else:
                o.append(0)
                l.append(6)

        limits = list(zip(o, l))

        res = self.server.search_engine.find_supplemented_window_lim(findstr, 2, offset, limit + 1, limits)

        disabled_f = ''
        if limit >= len(res.keys()):
            disabled_f = 'disabled'

        disabled_b = ''
        if offset == 0:
            disabled_b = 'disabled'

        for i, k in enumerate(res.keys()):

            if i == limit:
                break

            limit_doc = limits[i][1] - 1
            offset_doc = limits[i][0]

            re = '<ul>'

            disabled_f_doc = ''
            if limit_doc >= len(res[k]):
                disabled_f_doc = 'disabled'

            disabled_b_doc = ''
            if offset_doc == 0:
                disabled_b_doc = 'disabled'

            for j, v in enumerate(res[k]):
                if j == limit_doc:
                    break
                re += '<li>' + v.get_BB_string() + '</li>'

            re += '</ul>'

            result += form_limit.format(k, str(i), str(offset_doc), str(limit_doc), re, disabled_f_doc, disabled_b_doc)

        ret_result = body.format(postvars['findstr'][0], str(offset), str(limit), result, disabled_f, disabled_b)

        return ret_result


if __name__ == '__main__':
    httpd = HTTPServer(('localhost', 80), custom_handler)
    httpd.search_engine = SearchEngine('database')
    print ('Start server.')
    httpd.serve_forever()
