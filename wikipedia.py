from typing import Union, List, Dict, Any
import requests
import json

JsonType = Union[None, int, str, bool, List[Any], Dict[str, Any]]


class Wikipedia:

    def __init__(self):
        self.url = 'https://en.wikipedia.org/w/api.php'

    def get_page(self, titles: str, limit: int = 200, lang: str = "uk") -> JsonType:
        params = {
            "action": "query",
            "format": "json",
            "titles": titles,
            "prop": "langlinks",
            "lllimit": limit,
            "lllang": lang,
            "llinlanguagecode": lang
        }
        print(params)
        resp = requests.get(self.url, params=params)
        json_res = json.dumps(resp.json(), indent=4)
        print(json_res)


if __name__ == '__main__':
    wiki = Wikipedia()
    wiki.get_page("Театр Крусібл")
