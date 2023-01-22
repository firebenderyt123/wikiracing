from typing import List

import asyncio
import asyncpg  # type: ignore
from asyncpg.connection import Connection  # type: ignore


class Database:

    @staticmethod
    async def connect() -> Connection:
        return await asyncpg.connect(
            database='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
        )

    @staticmethod
    async def disconnect(conn: Connection):
        await conn.close()

    @staticmethod
    async def insert_title(title: str) -> int:
        conn = await Database.connect()
        try:
            res = await conn.fetchval(
                'INSERT INTO pages (title) VALUES ($1) RETURNING page_id',
                title
            )
        except Exception:
            res = await conn.fetchval(
                'SELECT page_id FROM pages WHERE title = $1',
                title
            )
        await Database.disconnect(conn)
        return res

    @staticmethod
    async def get_title(page_id: int) -> str:
        conn = await Database.connect()
        res = await conn.fetchval(
            'SELECT title FROM pages WHERE page_id = $1', page_id
        )
        await Database.disconnect(conn)
        return res

    @staticmethod
    async def insert_relation(title: str, parent: str) -> int:
        t_id = await Database.insert_title(title)
        p_id = await Database.insert_title(parent)
        conn = await Database.connect()
        try:
            res = await conn.fetchval(
                '''INSERT INTO relations (page_id, parent_id)
                    VALUES ($1, $2) RETURNING rel_id''',
                t_id, p_id
            )
        except Exception:
            res = await conn.fetchval(
                '''SELECT rel_id FROM relations
                    WHERE page_id = $1 and parent_id = $2''',
                t_id, p_id
            )
        await Database.disconnect(conn)
        return res

    @staticmethod
    async def get_parent(title: str) -> str:
        conn = await Database.connect()
        res = await conn.fetchval(
            '''SELECT
                q.title as parent
            FROM relations as r
            INNER JOIN pages as p ON p.page_id = r.page_id
            INNER JOIN pages as q ON q.page_id = r.parent_id
            WHERE p.title = $1''',
            title
        )
        await Database.disconnect(conn)
        return res

    @staticmethod
    async def get_titles(parent: str) -> List[str]:
        conn = await Database.connect()
        res = await conn.fetch(
            '''SELECT
                q.title as title
            FROM relations as r
            INNER JOIN pages as p ON p.page_id = r.parent_id
            INNER JOIN pages as q ON q.page_id = r.page_id
            WHERE p.title = $1''',
            parent
        )
        await Database.disconnect(conn)
        return [elem[0] for elem in res]

    @staticmethod
    async def recurse_path_finder(start: str, finish: str, level: int = 4) -> List[str]:  # noqa
        conn = await Database.connect()
        res = await conn.fetchval(
            '''
            WITH RECURSIVE t AS (
                (
                    SELECT DISTINCT
                        q.title as title,
                        p.title as parent,
                        1 as level,
                        ARRAY[q.title]::VARCHAR[] as way
                    FROM relations as r
                    INNER JOIN pages as p ON p.page_id = r.parent_id
                    INNER JOIN pages as q ON q.page_id = r.page_id
                    WHERE q.title = $1
                ) UNION ALL (
                    SELECT DISTINCT
                        q.title as title,
                        p.title as parent,
                        t.level + 1 as level,
                        way || q.title
                    FROM relations as r
                    INNER JOIN pages as p ON p.page_id = r.parent_id
                    INNER JOIN pages as q ON q.page_id = r.page_id
                    INNER JOIN t ON t.title = p.title
                    WHERE NOT (q.title = ANY(way))
                    AND p.title <> $2 and level < $3
                )
            )
            SELECT way FROM t
            WHERE $2 = ANY(way)
            ORDER BY level LIMIT 1;
            ''',
            start, finish, level
        )
        await Database.disconnect(conn)
        return res


async def test():
    # rel_id1 = await Database.insert_relation('test1', 'parent_test')
    # rel_id2 = await Database.insert_relation('test2', 'parent_test')
    # rel_id3 = await Database.insert_relation('test3', 'parent_test')
    # print(rel_id1, rel_id2, rel_id3)
    # title = await Database.get_titles('parent_test')
    # print(title)
    res = await Database.recurse_path_finder('Фестиваль', 'Пілястра', 4)
    print(res)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test())
    loop.close()
