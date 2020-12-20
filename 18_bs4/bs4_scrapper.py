from itertools import permutations
from bs4 import *
import argparse
import requests
from urllib.parse import urlparse
import json
import re
import time
from datetime import datetime as dt
import threading
import user_agent

ENGINES = {
    'google': 'https://www.google.com/search?q=',
    'yandex': 'https://yandex.ru/search/?text=',
    'duckduck': 'https://duckduckgo.com/?q=',
}


class Scrapper:

    def __init__(self):
        self.path_file_out = None
        self.search_engine = None
        self.user_agent = user_agent.generate_user_agent()
        self.url_target = None
        self.level = None

    def set_user_agent(self):
        self.user_agent = user_agent.generate_user_agent()

    def get_headers(self, lang=''):
        headers_Get = {
            'User-Agent': self.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        return headers_Get

    def set_url_target(self, url):
        self.url_target = url

    def set_level(self, level):
        self.level = level

    def set_file_output(self, file='scrap_output'):
        self.path_file_out = file

    def set_engine(self, engine):
        self.engine = ENGINES[engine]

    def scrap_responses(self, queries):
        if not self.path_file_out:
            self.set_file_output()
        s = requests.Session()
        for q in queries:
            if len(q) == 0:
                continue
            query = '+'.join(q)
            results = {}
            r = requests.get(self.engine + query, headers=self.get_headers())
            soup = BeautifulSoup(r.text, 'html.parser')
            topics = soup.findAll('div', class_='g')
            for index, t in enumerate(topics):
                try:
                    topic_title = t.find(
                        'div', class_='rc').find(
                        'div', class_='r').find(
                        'a').find(
                        'h3').getText()
                    # if regexp is exist
                    topic_url = t.find(
                        'div', class_='rc').find(
                        'div', class_='r').find('a')['href']
                    topic_index = index
                    results[topic_url] = {
                        'query': query,
                        'title': topic_title,
                        'engine': self.search_engine,
                        'position': topic_index
                    }
                except:
                    continue
            with open(self.path_file_out, 'a') as output:
                json.dump(results, output)
                output.write('\n')
            time.sleep(30)

    def get_queries(self, keywords):
        result = []
        for _ in range(self.level):
            result.extend(permutations(keywords.split(), _))
        return result

    def get_queries_from_file(self, file):
        result = []
        with open(file, 'r') as f:
            json_load = json.load(f)
            keywords = json_load['keywords']
        for _ in range(self.level):
            result.extend(permutations(keywords, _))
        return result


def init_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-kwf', action='store_true',
                        help='укажи имя или часть имени процесса')
    parser.add_argument('-kw', nargs='+', help='', type=str)
    parser.add_argument('-se', help='choose search engine', type=str,
                        choices=['google', 'yandex', 'duckduck'])
    parser.add_argument('-pl', metavar='PERMUTATION_LEVEL', type=int,
                        help='how many permutations you want to check')
    parser.add_argument('-tg', metavar='TARGET_MASK', type=str,
                        help='type mask of target source you want to find',
                        required=True)
    parser.add_argument('-fout', type=str, help='set path to result output file',
                        required=False)
    return parser


def main():
    parser = init_argparser()
    args = parser.parse_arguments()
    scrap = Scrapper()
    if args['pl']:
        scrap.set_level(args['pl'])
    if args['tg']:
        scrap.set_url_target(args['tg'])
    if args['se']:
        scrap.set_engine(args['se'])
    qu = scrap.get_queries(args['kw'])
    while True:
        try:
            tr1 = threading.Thread(target=scrap.scrap_responses, args=(qu,))
            tr1.start()
            print('new thread start at {}...'.format(dt.now().isoformat()))
            tr1.join()
            print('thread killed at {}...'.format(dt.now().isoformat()))
            time.sleep(15)
        except Exception as ex:
            continue
    print('done scrapping at {}...'.format(dt.isoformat()))
    pass


if __name__ == '__main__':
    main()
