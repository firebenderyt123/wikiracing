CREATE TABLE IF NOT EXISTS pages (
	page_id serial PRIMARY KEY,
	title VARCHAR (255) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS relations (
	rel_id serial PRIMARY KEY,
	page_id INT NOT NULL,
	parent_id INT NOT NULL,
	FOREIGN KEY (page_id)
		REFERENCES pages (page_id),
	FOREIGN KEY (parent_id)
		REFERENCES pages (page_id),
	UNIQUE (page_id, parent_id)
);