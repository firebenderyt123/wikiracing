from typing import Union, List, Dict, Any
import requests
import json

from datetime import datetime
from time import sleep

JsonType = Union[None, int, str, bool, List[Any], Dict[str, Any]]


class Wikipedia:

    def __init__(self, lang: str = "uk", req_per_min: int = 200):
        self.url = f'https://{lang}.wikipedia.org/w/api.php'
        self.delay = 60 / req_per_min

    def get_links(self, title: str, limit: int = 200) -> JsonType:
        return self.request({
            "action": "query",
            "format": "json",
            "generator": "links",
            "gplnamespace": 0,
            "titles": title,
            "gpllimit": limit
        })

    def request(self, params: Dict[str, str]) -> JsonType:
        start_time = datetime.now()
        obj = requests.get(self.url, params=params).json()
        req_time = (datetime.now() - start_time).total_seconds()
        if self.delay > req_time:
            sleep(self.delay - req_time)
        return obj

    def print_json(self, obj: Dict[str, JsonType]):
        print(json.dumps(obj, indent=4, ensure_ascii=False))

    def parse_links_titles(self, json: Dict[str, JsonType]) -> List[str]:
        if 'query' not in json:
            return []

        titles = []
        for key in json['query']['pages'].keys():
            titles.append(json['query']['pages'][key]['title'])
        return titles


if __name__ == '__main__':
    wiki = Wikipedia()
    obj = wiki.get_links("Дружба")
    print(wiki.parse_links_titles(obj))
