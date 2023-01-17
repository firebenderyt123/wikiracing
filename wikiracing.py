from typing import List
from urllib.parse import unquote
from bs4 import BeautifulSoup
import requests
from time import sleep

from custom_list import CustomList

requests_per_minute = 100
links_per_page = 200


class WikiRacer:

    def __init__(self, lang='uk'):
        self.domain = f'https://{lang}.wikipedia.org'
        self.page_url = f'{self.domain}/wiki/'
        self.url = f'{self.domain}/w/index.php?title=Спеціальна:Посилання_сюди/{{PAGE}}&limit={links_per_page}' # noqa

    def find_path(self, start: str, finish: str) -> List[str]:
        self.cL = CustomList()
        self.path = []

        u_start = start.replace(' ', '_')
        u_finish = finish.replace(' ', '_')

        if (not WikiRacer.is_url_exists(self.page_url + u_start)
                or not WikiRacer.is_url_exists(self.page_url + u_finish)):
            raise Exception("Нажаль, якась зі сторінок не існує, тому ми не зможемо побудувати шлях :(") # noqa

        self.cL.append_level()
        self.cL.append_data({'title': u_start, 'parent': ''})
        self.cL.append_level()
        self.cL.append_data({'title': u_finish, 'parent': ''})

        res = self.links_finder()

        if res is not True:
            return []

        return self.build_path(u_start)

    def links_finder(self) -> List[str]:

        # check links starting from last node
        self.cL.insert_level(self.cL._curr_level)
        pages = self.cL.get_title(self.cL._curr_level + 1)

        self.parse_pages(pages)
        
        # compare links
        self.dublicate_link = self.cL.compare()

        if self.dublicate_link is not False:
            return True

        # run again

        return self.links_finder()

    def parse_pages(self, pages: List[str]):
        for page in pages:
            self.page = page
            url = self.url.replace('{PAGE}', self.page)
            resp = requests.get(url)
            
            soup = BeautifulSoup(resp.text, 'html.parser')
            list = soup.select('#mw-whatlinkshere-list')[0]
            li_elems = list.find_all('li')

            for li in li_elems:
                a = li.find('a')
                title = a.get('title').replace(' ', '_')

                self.cL.append_data({
                    'title': title,
                    'parent': self.page
                })

    def build_path(self, title: str) -> List[str]:
        for obj in self.cL._data[self.cL._curr_level]:
            if obj['title'] == title:
                self.path.append(title.replace('_', ' '))
                if self.cL._curr_level == self.cL._total_levels - 1:
                    return self.path
                
                self.cL._curr_level += 1
                return self.build_path(obj['parent'])

    @staticmethod
    def is_url_exists(url: str) -> bool:
        return requests.get(url).status_code == 200


if __name__ == '__main__':
    wR = WikiRacer('uk')
    words = ('Дружба', 'Рим')
    path = wR.find_path(words[0], words[1])
    print(path)
