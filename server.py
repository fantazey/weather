import os
import sqlite3
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

PATH = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(PATH, 'db.sqlite')
SELECT_QUERY = """
SELECT * FROM (
    SELECT * FROM temperature 
    ORDER BY date DESC 
    LIMIT 100
) ORDER BY date ASC
"""


class MyHandler(BaseHTTPRequestHandler):
    def set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_HEAD(self):
        self.set_headers()

    def do_GET(self):
        connection = sqlite3.connect(DB)
        cursor = connection.execute(SELECT_QUERY)
        data = cursor.fetchall()
        result = []
        for row in data:
            result.append({
                'date': row[0],
                'temperature': row[1],
                'humidity': row[2]
            })
        json_data = json.dumps(result)
        with open(os.path.join(PATH, 'index.html')) as template_file:
            template = template_file.read()
        template = template.replace('__DATA__', json_data)
        self.set_headers()
        self.wfile.write(bytes(template, "utf-8"))


def run():
    server_address = ('', 8085)
    httpd = HTTPServer(server_address, MyHandler)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
