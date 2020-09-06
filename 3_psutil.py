import os
import sys
import argparse
import re
import psutil


def init_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', metavar='PROCESS_NAME', type=str,
                        help='укажи имя или часть имени процесса')
    parser.add_argument('-k', help='set it if killing process is necessary',
                        action='store_true')
    parser.add_argument('-s', help='set it if process activity alerting is necessary',
                        action='store_true')
    parser.add_argument('-e', help='show psutil example', action='store_true')
    return parser


def kill_process(name):
    while True:
        for proc in psutil.process_iter():
            if name.lower() in proc.name().lower():
                proc.terminate()
                return None


def search_process(name):
    while True:
        for proc in psutil.process_iter():
            try:
                if name.lower() in proc.name().lower():
                    print('Process {} now running wit PID: {}'.format(
                        name, proc.pid))
            except Exception as ex:
                print(ex)
                return None


def main():
    parser = init_argparser()
    args = parser.parse_args()
    if args.p:
        if args.k:
            kill_process(args.p)
        if args.s:
            search_process(args.p)
    else:
        print('Не указано имя процесса')
        return None


if __name__ == '__main__':
    main()
