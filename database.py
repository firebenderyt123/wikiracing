from typing import List, Set

import psycopg2
from psycopg2 import errors
from psycopg2.errorcodes import UNIQUE_VIOLATION

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='postgres',
    host='localhost'
)

conn.autocommit = True


class Database:

    @staticmethod
    def insert_title(title: str) -> int:
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    'INSERT INTO pages (title) VALUES (%s) RETURNING page_id',
                    (title,)
                )
            except errors.lookup(UNIQUE_VIOLATION):
                cursor.execute(
                    'SELECT page_id FROM pages WHERE title = %s',
                    (title,)
                )
            return cursor.fetchone()[0]

    @staticmethod
    def get_title(page_id: int) -> str:
        with conn.cursor() as cursor:
            cursor.execute(
                'SELECT title FROM pages WHERE page_id = %s', (page_id,)
            )
            res = cursor.fetchone()
            if not res:
                return None
            return res[0]

    @staticmethod
    def insert_relation(title: str, parent: str) -> int:
        t_id = Database.insert_title(title)
        p_id = Database.insert_title(parent)
        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    '''INSERT INTO relations (page_id, parent_id)
                        VALUES (%s, %s) RETURNING rel_id''',
                    (t_id, p_id)
                )
            except errors.lookup(UNIQUE_VIOLATION):
                cursor.execute(
                    '''SELECT rel_id FROM relations
                        WHERE page_id = %s and parent_id = %s''',
                    (t_id, p_id)
                )
            return cursor.fetchone()[0]

    @staticmethod
    def get_parent(title: str) -> str:
        with conn.cursor() as cursor:
            cursor.execute(
                '''SELECT
                    q.title as parent
                FROM relations as r
                INNER JOIN pages as p ON p.page_id = r.page_id
                INNER JOIN pages as q ON q.page_id = r.parent_id
                WHERE p.title = %s''',
                (title,)
            )
            res = cursor.fetchone()
            if not res:
                return None
            return res[0]

    @staticmethod
    def get_titles(parent: str) -> str:
        with conn.cursor() as cursor:
            cursor.execute(
                '''SELECT
                    q.title as title
                FROM relations as r
                INNER JOIN pages as p ON p.page_id = r.parent_id
                INNER JOIN pages as q ON q.page_id = r.page_id
                WHERE p.title = %s''',
                (parent,)
            )
            res = cursor.fetchall()
            return [elem[0] for elem in res]


if __name__ == '__main__':
    rel_id = Database.insert_relation('test1', 'parent_test')
    rel_id = Database.insert_relation('test2', 'parent_test')
    rel_id = Database.insert_relation('test3', 'parent_test')
    title = Database.get_titles('parent_test')
    print(title)
