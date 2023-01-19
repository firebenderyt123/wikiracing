from typing import List
from urllib.parse import unquote
from bs4 import BeautifulSoup
import requests
from time import sleep

from custom_list import CustomList
from wikipedia import Wikipedia

requests_per_minute = 100
links_per_page = 200

wiki = Wikipedia()


class WikiRacer:

    def __init__(self, lang='uk'):
        self.domain = f'https://{lang}.wikipedia.org'
        self.page_url = f'{self.domain}/wiki/'

    def find_path(self, start: str, finish: str) -> List[str]:
        self.cL = CustomList()
        self.path = []

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

        # check links starting from first node
        self.cL.insert_level(self.cL._curr_level)
        pages = self.cL.get_title(self.cL._curr_level - 1)

        for page in pages:
            print(page)
            obj = wiki.get_links(page, links_per_page)
            titles = wiki.parse_links_titles(obj)
            arr = [{'title': title, 'parent': page} for title in titles]
            self.cL.append_array(arr)
        
        # compare links
        self.dublicate_link = self.cL.compare()

        if self.dublicate_link is not False:
            return True

        self.cL._curr_level += 1

        # check links starting from last node
        self.cL.insert_level(self.cL._curr_level)
        pages = self.cL.get_title(self.cL._curr_level + 1)

        for page in pages:
            print(page)
            obj = wiki.get_linkshere(page, links_per_page)
            titles = wiki.parse_links_titles(obj)
            arr = [{'title': title, 'parent': page} for title in titles]
            self.cL.append_array(arr)
        
        # compare links
        self.dublicate_link = self.cL.compare()

        if self.dublicate_link is not False:
            return True

        return self.links_finder()

    def build_path(self) -> List[str]:
        title = self.dublicate_link
        curr_level = self.cL._curr_level
        if self.cL._total_levels % 2 == 0:
            # last links parsed normal (go back)
            n = -1
        else:
            #  last links parsed reverse (go forward)
            n = 1
        
        while (self.cL._curr_level != -1
                and self.cL._curr_level != self.cL._total_levels):
            braked = False
            for obj in self.cL._data[self.cL._curr_level]:
                if obj['title'] == title:
                    if n == -1:
                        self.path.insert(0, title)
                    else:
                        self.path.append(title)

                    self.cL._curr_level += n
                    title = obj['parent']
                    braked = True
                    break

            if not braked:
                self.cL._curr_level += n

        n = -n
        self.cL._curr_level = curr_level + n
        title = self.dublicate_link
        while (self.cL._curr_level != -1
                and self.cL._curr_level != self.cL._total_levels):
            braked = False
            for obj in self.cL._data[self.cL._curr_level]:
                if obj['title'] == title:
                    if title not in self.path:
                        if n == -1:
                            self.path.insert(0, title)
                        else:
                            self.path.append(title)

                    self.cL._curr_level += n
                    title = obj['parent']
                    braked = True
                    break

            if not braked:
                self.cL._curr_level += n

        return self.path

    @staticmethod
    def is_url_exists(url: str) -> bool:
        return requests.get(url).status_code == 200


if __name__ == '__main__':
    wR = WikiRacer('uk')
    words = ('Дружба', 'Рим')
    path = wR.find_path(words[0], words[1])
    print(path)
