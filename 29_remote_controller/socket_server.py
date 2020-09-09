import socket
import os
import sys
import json
import re


HTML_PAGE_TEMPLATE = '<!DOCTYPE HTML > \
        <html >\
        <head >\
        <meta charset = "utf-8" >\
        <title > Тег BUTTON </title >\</head >\
    <body >\
    <form>\
       REPLACE_IT\
    </form>\
    </body >\
</html >'


def parse_json_commands(file):
    with open(file, 'r') as f:
        config = json.load(f)
    return config['buttons']
        # buttons - object(title, actopn)


def generate_html(file):
    config = parse_json_commands(file)
    buttons = []
    button_html = '<input type="button" value="{}" onclick="{}">'
    for item in config:
        buttons.append(button_html.format(item['title'], item['action']))
    return re.sub(r'REPLACE_IT', '\n'.join(buttons), HTML_PAGE_TEMPLATE)


def init_server():
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    conn, addr = sock.accept()
    return conn, addr


def run_server(connection):
    try:
        print('server started...')
        while True:
            data = connection.recv(1024)
            if not data:
                break
            os.system('cmd {}'.format(data))
            connection.send(data.upper())

    except Exception as ex:
        connection.close()
        raise ex
    finally:
        connection.close()


def main(args):
    print(generate_html(args[1]))
    # conn, addr = init_server()
    # run_server(conn, addr)


if __name__ == '__main__':
    main(sys.argv)
