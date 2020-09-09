import os
import sys
import json
import re
import http.server
import socketserver


def parse_json_commands(file):
    with open(file, 'r') as f:
        config = json.load(f)
    return config['buttons']

def get_html_template(path):
    with open(path, 'r') as html:
        content = html.read()
    return content

def generate_html(file):
    html_template = get_html_template('./index_template.html')
    config = parse_json_commands(file)
    buttons = []
    button_html = '<input type="button" value="{}" onclick="{}">'
    for item in config:
        buttons.append(button_html.format(item['title'], item['action']))
    return re.sub(r'REPLACE_IT', '\n'.join(buttons), html_template)


def run_server():
    PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()


def main(args):
    print(generate_html(args[1]))
    run_server()


if __name__ == '__main__':
    main(sys.argv)
