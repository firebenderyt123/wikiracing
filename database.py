import asyncio
import asyncpg


async def prepare():
    global conn
    conn = await asyncpg.connect(
        database='postgres',
        user='postgres',
        password='postgres',
        host='localhost',
    )
db_loop = asyncio.new_event_loop()
db_loop.run_until_complete(prepare())


class Database:

    @staticmethod
    async def insert_title(title: str) -> int:
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
        return res

    @staticmethod
    async def get_title(page_id: int) -> str:
        res = await conn.fetchval(
            'SELECT title FROM pages WHERE page_id = $1', page_id
        )
        return res

    @staticmethod
    async def insert_relation(title: str, parent: str) -> int:
        t_id = await Database.insert_title(title)
        p_id = await Database.insert_title(parent)
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
        return res

    @staticmethod
    async def get_parent(title: str) -> str:
        res = await conn.fetchval(
            '''SELECT
                q.title as parent
            FROM relations as r
            INNER JOIN pages as p ON p.page_id = r.page_id
            INNER JOIN pages as q ON q.page_id = r.parent_id
            WHERE p.title = $1''',
            title
        )
        return res

    @staticmethod
    async def get_titles(parent: str) -> str:
        res = await conn.fetch(
            '''SELECT
                q.title as title
            FROM relations as r
            INNER JOIN pages as p ON p.page_id = r.parent_id
            INNER JOIN pages as q ON q.page_id = r.page_id
            WHERE p.title = $1''',
            parent
        )
        return [elem[0] for elem in res]


async def test():
    rel_id1 = await Database.insert_relation('test1', 'parent_test')
    rel_id2 = await Database.insert_relation('test2', 'parent_test')
    rel_id3 = await Database.insert_relation('test3', 'parent_test')
    print(rel_id1, rel_id2, rel_id3)
    title = await Database.get_titles('parent_test')
    print(title)


if __name__ == '__main__':
    db_loop.run_until_complete(test())
