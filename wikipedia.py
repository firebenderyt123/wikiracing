from typing import List, Dict
import requests
import json
import time

JsonType = Dict[
    str, Dict[
        str, Dict[
            str, Dict[
                str, str
            ]
        ]
    ]
]


class Wikipedia:

    def __init__(self, lang: str = "uk", req_per_min: int = 200):
        self.url = f'https://{lang}.wikipedia.org/w/api.php'
        self.delay = 60 / req_per_min

    def get_links(self, title: str, limit: int = 200) -> JsonType:
        return self.request({
            "action": "query",
            "format": "json",
            "generator": "links",
            "gplnamespace": str(0),
            "titles": title,
            "gpllimit": str(limit)
        })

    def request(self, params: Dict[str, str]) -> JsonType:
        start_time = time.perf_counter()
        obj = requests.get(self.url, params=params).json()
        exec_time = time.perf_counter() - start_time
        if self.delay > exec_time:
            time.sleep(self.delay - exec_time)
        return obj

    def print_json(self, obj: Dict[str, JsonType]):
        print(json.dumps(obj, indent=4, ensure_ascii=False))

    def parse_links_titles(self, json: JsonType) -> List[str]:
        if 'query' not in json:
            return []

        titles = []
        for key in json['query']['pages'].keys():
            titles.append(json['query']['pages'][key]['title'])
        return titles


if __name__ == '__main__':
    wiki = Wikipedia()
    obj = wiki.get_links("Бароко")
    print(wiki.parse_links_titles(obj))
