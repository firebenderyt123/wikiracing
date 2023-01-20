from typing import List
import requests

from custom_list import CustomList
from wikipedia import Wikipedia
from database import Database as db

requests_per_minute = 100
links_per_page = 200

wiki = Wikipedia("uk", requests_per_minute)


class WikiRacer:

    def __init__(self, lang='uk'):
        self.domain = f'https://{lang}.wikipedia.org'
        self.page_url = f'{self.domain}/wiki/'

    def find_path(self, start: str, finish: str) -> List[str]:
        self.cL = CustomList()
        self.path = []
        self.checked = []
        self.curr_level = 0

        u_start = start.replace(' ', '_')
        u_finish = finish.replace(' ', '_')

        if (not WikiRacer.is_url_exists(self.page_url + u_start)
                or not WikiRacer.is_url_exists(self.page_url + u_finish)):
            raise Exception("Нажаль, якась зі сторінок не існує, тому ми не зможемо побудувати шлях :(") # noqa

        self.cL.append_level()
        self.cL.append_data({'title': start, 'parent': ''})
        self.cL.append_level()
        self.cL.append_data({'title': finish, 'parent': ''})

        res = self.links_finder()

        if res is not True:
            return []

        return self.build_path()

    def links_finder(self) -> List[str]:

        self.curr_level += 1
        if self.curr_level > 3:
            return False

        # check links starting from first node
        self.cL.insert_level(self.cL._curr_level)
        pages = self.cL.get_title(self.cL._curr_level - 1)

        for page in pages:

            if page in self.checked:
                continue

            titles = db.get_titles(page)
            print(self.curr_level)
            print('db:', page)
            
            if not titles:
                
                print('url:', page)
                obj = wiki.get_links(page, links_per_page)
                titles = wiki.parse_links_titles(obj)
                
                for title in titles:
                    db.insert_relation(title, page)

            arr = [{'title': title, 'parent': page} for title in titles]

            self.cL.append_array(arr)
            self.checked.append(page)
        
        # search dublicate
        for arr in self.cL._data[1:-1]:
            for obj in arr:
                if obj['title'] == self.cL._data[-1][0]['title']:
                    self.dublicate_title = obj['title']
                    return True

        self.cL._curr_level += 1

        return self.links_finder()

    def build_path(self) -> List[str]:
        for arr in self.cL._data[1:-1]:
            for obj in arr:
                if obj['title'] == self.dublicate_title:
                    self.path.insert(0, obj['title'])
                    self.dublicate_title = obj['parent']
                    
                    if self.dublicate_title == self.cL._data[0][0]['title']:
                        self.path.insert(0, self.dublicate_title)
                        return self.path

                    return self.build_path()

    @staticmethod
    def is_url_exists(url: str) -> bool:
        return requests.get(url).status_code == 200


if __name__ == '__main__':
    wR = WikiRacer('uk')
    words = ('Фестиваль', 'Пілястра')
    path = wR.find_path(words[0], words[1])
    print(path)
