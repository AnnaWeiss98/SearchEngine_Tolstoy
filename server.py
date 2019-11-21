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
     <td><input type="text" name="findstr" value={0}>
         <input type="hidden" name="prev_findstr" value={0}>
     </td>
     <td><input type="submit" value="Search"></td>
     <tr>
     <td><input type="submit" name="action" value="begin"></td>
     <td><input type="submit" name="action" value="back"></td>
     <td><input type="submit" name="action" value="forward"></td> 
     <td><input type="hidden" name="offset" value="{1}" size="4"></td>
     </tr>
     <tr>
     <td>Count tom:</td>
     <td><input type="text" name="limit" value="{2}" size="4"></td>
     </tr>
     </table>
     {3}
    </form>
    </body>
</html>
'''

form_limit ='''
     <table>
     <tr>
     <td colspan="2" align="center"> Для файла {0} </td>
     </tr>
     <tr>
     <td><input type="submit" name="action{1}" value="begin"></td>
     <td><input type="submit" name="action{1}" value="back"></td>
     <td><input type="submit" name="action{1}" value="forward"></td> 
     <td><input type="hidden" name="doc{1}offset" value="{2}" size="4"></td>
     </tr>
     <tr>
     <td>a number of results on the page:</td>
     <td><input type="text" name="doc{3}limit" value="{4}" size="4"></td>
     </table>
     {5}
 '''

class custom_handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """
        Creates a simple HTML page with a field and a button.
        """
        self.send_response(200)
        self.end_headers()
        result = ''
        self.wfile.write(bytes(body.format('','0','4',result), 'cp1251'))

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
        result = self.gen_page(postvars)

        limit =  self.get_int(postvars['limit'][0],4)
        offset = self.get_int(postvars['offset'][0],0)
        if 'action' in postvars:
            offset = self.get_offset(postvars['action'][0],offset,limit)
        
        if postvars['findstr'][0] !=  postvars['prev_findstr'][0]:
           offset = 0
        
        self.wfile.write(bytes(body.format(postvars['findstr'][0],str(offset),str(limit),result), 'cp1251'))

    def get_int(self,value, def_value):
        result = def_value
        try:
            result = int(value)
        except ValueError:
            pass
        return result

    def get_offset(self, act, offset,delta):

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

        result = ''
        findstr = postvars['findstr'][0]
        limit = self.get_int(postvars['limit'][0], 4)

        offset = self.get_int(postvars['offset'][0],0)
        if 'action' in postvars:
            offset = self.get_offset(postvars['action'][0],offset,limit)

        if postvars['findstr'][0] !=  postvars['prev_findstr'][0]:
           offset = 0

        o = []
        l = []
        for ind in range(offset, offset+limit):
            if 'doc'+str(ind)+'offset' in postvars:
               
                limit_doc = self.get_int(postvars['doc' + str(ind) + 'limit'][0],5)
                offset_doc = self.get_int(postvars['doc'+str(ind)+'offset'][0],0)
                if 'action'+str(ind) in postvars:                
                    offset_doc = self.get_offset(postvars['action'+str(ind)][0], offset_doc,limit_doc)

                if postvars['findstr'][0] !=  postvars['prev_findstr'][0]:
                      offset_doc = 0

                o.append(offset_doc)
                l.append(limit_doc)
            else:
                o.append(0)
                l.append(5)

        limits = list(zip(o,l))

        res = self.server.search_engine.find_supplemented_window_lim(findstr, 2, offset, limit, limits)

        for i,k in enumerate(res.keys()):
            limit_doc = 5
            offset_doc = 0
               
            if 'doc'+str(i+offset)+'limit' in postvars:

                limit_doc = self.get_int(postvars['doc'+str(i+offset)+'limit'][0],5)

                offset_doc = self.get_int(postvars['doc'+str(i+offset)+'offset'][0],0)

                if 'action'+str(i+offset) in postvars:                
                    offset_doc = self.get_offset(postvars['action'+str(i+offset)][0], offset_doc,limit_doc)

                if postvars['findstr'][0] !=  postvars['prev_findstr'][0]:
                      offset_doc = 0
            re = '<ul>'
            for v in res[k]:
                re += '<li>' + v.get_BB_string() + '</li>'
            re += '</ul>'

            result += form_limit.format(k, str(i+offset), str(offset_doc), str(i+offset), str(limit_doc), re)


        return result


if __name__ == '__main__':

    httpd = HTTPServer(('localhost', 80), custom_handler)
    httpd.search_engine = SearchEngine('database')
    print ('Start server.')
    httpd.serve_forever()
