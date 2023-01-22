-- Топ 5 найпопулярніших статей (ті що мають найбільшу кількість посилань на себе)
SELECT
	p.title as title,
	count(p.title) as count
FROM relations as r
INNER JOIN pages as p ON p.page_id = r.page_id
GROUP BY title
ORDER BY count DESC LIMIT 5;

-- Топ 5 статей з найбільшою кількістю посилань на інші статті
SELECT
	p.title as title,
	count(p.title) as count
FROM relations as r
INNER JOIN pages as p ON p.page_id = r.parent_id
GROUP BY title
ORDER BY count DESC LIMIT 5;

-- Для заданної статті знайти середню кількість потомків другого рівня
SELECT
	avg(a.count)
FROM (
	SELECT
		p.title as parent,
		count(q.title) as count
	FROM relations as r
	INNER JOIN pages as p ON p.page_id = r.parent_id
	INNER JOIN pages as q ON q.page_id = r.page_id
	WHERE p.title IN (
		SELECT
			q.title as title
		FROM relations as r
		INNER JOIN pages as p ON p.page_id = r.parent_id
		INNER JOIN pages as q ON q.page_id = r.page_id
		WHERE p.title = '12 листопада'
	)
	GROUP BY parent
) as a;

/*
	(На додаткові бали) Запит, що має параметр - N,
	повертає до п’яти маршрутів переходу довжиною N.
	Сторінки в шляху не мають повторюватись.
*/

WITH RECURSIVE t AS (
	(
		SELECT
			q.title as title,
			p.title as parent,
			1 as level,
			ARRAY[q.title]::VARCHAR[] as way
		FROM relations as r
		INNER JOIN pages as p ON p.page_id = r.parent_id
		INNER JOIN pages as q ON q.page_id = r.page_id
		WHERE r.parent_id = (
			SELECT parent_id
			FROM relations
			ORDER BY random()
			LIMIT 1
		)
		LIMIT 1600 /* these limits are making requests faster (you can try to remove them)
		but who knows how long it'll be processed.
		Moreover, sometimes the length of the path could be smaller than N
		*/
	) UNION ALL (
		SELECT 
			q.title as title,
			p.title as parent,
			t.level + 1 as level,
			way || q.title
		FROM relations as r
		INNER JOIN pages as p ON p.page_id = r.parent_id
		INNER JOIN pages as q ON q.page_id = r.page_id
		INNER JOIN t ON t.title = p.title
		WHERE NOT (q.title = ANY(way))
		AND t.level < 8 -- N = 8
		ORDER BY t.level
		LIMIT 1600 /* these limits are making requests faster (you can try to remove them)
		but who knows how long it'll be processed.
		Moreover, sometimes the length of the path could be smaller than N
		*/
	)
)
SELECT way FROM t ORDER BY level DESC LIMIT 5;