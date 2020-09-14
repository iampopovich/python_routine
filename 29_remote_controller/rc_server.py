import os
import sys
import json
import re
import http.server
import socketserver
from io import BytesIO


class CustomHandler(http.server.BaseHTTPRequestHandler):

    def _send_cors_headers(self):
        """ Sets headers required for CORS """
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers",
                         "x-api-key,Content-Type")

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        with open('index.html', 'rb') as index:
            self.wfile.write(index.read())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        os.system(body.decode())
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
        response = BytesIO()
        response.write('{}: executed'.format(body).encode('utf-8'))
        self.wfile.write(response.getvalue())


def parse_json_commands(file):
    with open(file, 'rb') as f:
        config = json.load(f)
    return config['buttons']


def get_html_template(path):
    with open(path, 'r') as html:
        content = html.read()
    return content


def generate_index_html(file=None):
    if file:
        html_template = get_html_template('./index_template.html')
        config = parse_json_commands(file)
        buttons = []
        button_html = '<button class="btn btn-secondary \
            btn-lg btn-block" onclick=sendRequest(this) \
            argument="{}" type="button">{}</button>'
        for item in config:
            buttons.append(button_html.format(item['action'], item['title']))
        with open('index.html', 'w') as index:
            index.write(
                re.sub(r'REPLACE_IT', '\n'.join(buttons), html_template))
        return True
    else:
        if not os.path.exists('./index.html'):
            print('index.html does not exist')
            return False
        else:
            print('index.html is already generated')
            return True


def run_server(config):
    PORT = 8080
    if generate_index_html(config):
        Handler = CustomHandler
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()


def main(args):
    try:
        config = args[1]
    except:
        config = None
    run_server(config)


if __name__ == '__main__':
    main(sys.argv)
