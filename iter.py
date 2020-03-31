import json
import requests
import hashlib
from loger_to_file import loger_to_file


class CountriesIter:

    def __init__(self, path):
        self._start = -1
        self.session = requests.Session()
        with open(path, mode='r', encoding='utf-8') as file:
            data = json.load(file)
            self.countries_names = [iteam['name']['common'] for iteam in data]

    def __iter__(self):
        return self

    def __next__(self):
        self._start += 1
        try:
            country_name = self.countries_names[self._start]
            print(f'{self._start + 1} of {len(self.countries_names)}')
            return f'{country_name} - {self.get_url(country_name)}'
        except IndexError:
            raise StopIteration

    @loger_to_file('log.txt')
    def get_url(self, country_name):
        URL = 'https://en.wikipedia.org/w/api.php'
        PARAMS = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srlimit': 1,
            'srsearch': country_name
        }
        respose = self.session.get(url=URL, params=PARAMS)
        page_id = respose.json()['query']['search'][0]['pageid']

        PARAMS = {
            'action': 'query',
            'format': 'json',
            'prop': 'info',
            'pageids': page_id,
            'inprop': 'url'
        }
        respose = self.session.get(url=URL, params=PARAMS)
        return respose.json()['query']['pages'][str(page_id)]['canonicalurl']


def md5_iter(path):
    with open(path, mode='r', encoding='utf-8') as file:
        for line in file:
            yield hashlib.md5(line.encode(encoding='utf-8')).hexdigest()


if __name__ == '__main__':
    countries = CountriesIter('countries.json')
    with open('out.txt', mode='w', encoding='utf-8') as file:
        for country in countries:
            file.write(country + '\n')
    for line in md5_iter('out.txt'):
        print(line)
