CREATE TABLE urls (
	id bigint PRIMARY KEY,
	name varchar(255) NOT NULL,
	created_at timestamp NOT NULL
);
CREATE TABLE url_checks (
	id bigint PRIMARY KEY,
	url_id bigint REFERENCES urls (id),
	status_code int,
	h1 varchar(70),
	title varchar(110),
	description varchar(160),
	created_at timestamp NOT NULL
);
