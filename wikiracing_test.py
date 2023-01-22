import unittest 
from unittest import IsolatedAsyncioTestCase

from wikiracing import WikiRacer


class WikiRacerTest(IsolatedAsyncioTestCase):

    racer = WikiRacer()

    async def test_1(self):
        path = await self.racer.find_path('Дружба', 'Рим')
        self.assertEqual(
            path, ['Дружба', 'Якопо Понтормо', 'Рим']
        )

    async def test_2(self):
        path = await self.racer.find_path('Мітохондріальна ДНК', 'Вітамін K')
        self.assertEqual(
            path, ['Мітохондріальна ДНК', 'Бактерії', 'Вітамін K']
        )

    async def test_3(self):
        path = await self.racer.find_path('Марка (грошова одиниця)', 'Китайський календар') # noqa
        self.assertEqual(
            path, ['Марка (грошова одиниця)', '1549', 'Китайський календар']
        )

    async def test_4(self):
        #
        # if use some more than 200 links per page path will be
        # Фестиваль -> Бароко -> Пілястра
        #
        path = await self.racer.find_path('Фестиваль', 'Пілястра')
        self.assertEqual(
            path, ['Фестиваль', 'Бароко', 'Архітектурний ордер', 'Пілястра']
        )

    async def test_5(self):
        path = await self.racer.find_path('Дружина (військо)', '6 жовтня')
        self.assertEqual(
            path, ['Дружина (військо)', 'Друга світова війна', '6 жовтня']
        )


if __name__ == '__main__':
    unittest.main()
