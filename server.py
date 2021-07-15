import os
import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PATH = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(PATH, 'db.sqlite')


class MyHandler(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self.set_headers()

    def do_GET(self):
        connector = sqlite3.connect(DB)
        handler = connector.execute('select * from temperature limit 144')
        data = handler.fetchall()
        print(data)
        result = []
        for row in data:
            result.append({
                'date': row[0],
                'temperature': row[1],
                'humidity': row[2]
            })
        json_data = json.dumps(result)
        template_file = open(os.path.join(PATH, 'index.html'))
        template = template_file.readlines()
        template = "".join(template)
        template_file.close()
        template = template.replace('__DATA__', str(json_data))
        self.set_headers()
        self.wfile.write(bytes(template, "utf-8"))


def run():
    server_address = ('', 8085)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
