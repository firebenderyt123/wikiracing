from typing import List
import requests
import asyncio

from custom_list import CustomList
from wikipedia import Wikipedia
from database import Database as db

requests_per_minute = 100
links_per_page = 200
max_path_len_check = 4  # affects only a quick search of the database 

wiki = Wikipedia("uk", requests_per_minute)


class WikiRacer:

    def __init__(self, lang='uk'):
        self.domain = f'https://{lang}.wikipedia.org'
        self.page_url = f'{self.domain}/wiki/'

    async def find_path(self, start: str, finish: str) -> List[str]:
        self.cL = CustomList()
        self.path: List[str] = []
        self.checked: List[str] = []
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

        res = await self.fast_check(start, finish)
        if res:
            return res
        
        res = await self.links_finder()  # type: ignore

        if res is not True:
            return []

        return self.build_path()

    async def links_finder(self) -> List[str] | bool:
        #
        # p.s
        # if a page has no links, 
        # it will be rechecked again after rescaning
        #

        self.curr_level += 1
        if self.curr_level > max_path_len_check - 1:
            # need up to 40 000 links to check
            return False

        # check links starting from first node
        self.cL.insert_level(self.cL._curr_level)
        pages = self.cL.get_title(self.cL._curr_level - 1)

        for page in pages:

            if page in self.checked:
                continue

            titles = await db.get_titles(page)
            # print(self.curr_level)
            # print('db:', page)
            
            if not titles:
                
                # print('url:', page)
                obj = wiki.get_links(page, links_per_page)
                titles = wiki.parse_links_titles(obj)
                
                for title in titles:
                    await db.insert_relation(title, page)

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

        return await self.links_finder()

    def build_path(self) -> List[str]:
        for arr in self.cL._data[1:-1]:
            for obj in arr:
                if obj['title'] == self.dublicate_title:
                    self.path.insert(0, obj['title'])
                    self.dublicate_title = obj['parent']
                    
                    if self.dublicate_title == self.cL._data[0][0]['title']:
                        self.path.insert(0, str(self.dublicate_title))
                        return self.path

                    return self.build_path()
        return []

    async def fast_check(self, start: str, finish: str) -> List[str]:
        res = await db.recurse_path_finder(
            start, finish, max_path_len_check
        )
        return res if res is not None else []

    @staticmethod
    def is_url_exists(url: str) -> bool:
        return requests.get(url).status_code == 200


async def start():
    wR = WikiRacer('uk')
    words = ('Дружина (військо)', '6 жовтня')
    path = await wR.find_path(words[0], words[1])
    print(path)

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(start())
    loop.close()
