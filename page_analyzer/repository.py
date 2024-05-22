import datetime
import psycopg2
from psycopg2.extras import NamedTupleCursor


class UrlsRepository:
    conn = None

    def __init__(self, database_url):
        try:
            self.conn = psycopg2.connect(database_url)
            print('Connection to database is OK')
        except psycopg2.OperationalError as e:
            print(f'Unable to connect!\n{e}')

    def __get_next_id(self, table):
        select_query = f'SELECT MAX(id) FROM {table};'
        with self.conn.cursor() as curs:
            curs.execute(select_query)
            record = curs.fetchone()
        id = record[0]
        result = 1 if id is None else id + 1
        return result

    def add_url(self, url):
        new_id = self.__get_next_id('urls')
        current_date = datetime.datetime.now()
        insert_query = """INSERT INTO urls (id, name, created_at) VALUES """
        """(%s, %s, %s);"""
        item_tuple = (new_id, url, current_date)

        with self.conn.cursor() as curs:
            curs.execute(insert_query, item_tuple)
        self.conn.commit()
        print(f'1 запись успешно вставлена. id={new_id}')
        result = self.find(name=url)
        return result

    def find_urls(self, id=None, name=None):
        result = None
        key, value = None, None
        if id:
            key, value = 'id', str(id)
        elif name:
            key, value = 'name', str(name)
        if key:
            with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(f"SELECT * from urls WHERE {key}=%s", (value,))
                result = curs.fetchall()
        return result

    def find_one_url(self, id=None, name=None):
        result = self.find_urls(id, name)
        if result:
            result = result[0]
        return result

    def get_all_url(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            query = """SELECT urls.id, urls.name, urls.created_at,
                max(url_checks.created_at) as last_check
                FROM urls LEFT JOIN url_checks on url_checks.url_id = urls.id
                GROUP BY urls.id, urls.name, urls.created_at
                ORDER BY urls.id DESC;"""
            curs.execute(query)
            result = curs.fetchall()
        return result

    def add_check(self, url):
        new_id = self.__get_next_id('url_checks')
        current_date = datetime.datetime.now()
        url_id = self.find_urls(name=url)[0].id
        insert_query = """INSERT INTO url_checks (id, url_id, created_at)
                    VALUES (%s, %s, %s);"""
        item_tuple = (new_id, url_id, current_date)

        with self.conn.cursor() as curs:
            curs.execute(insert_query, item_tuple)
        self.conn.commit()
        print(f'проверка сайта {url} проведена.')
        return True

    def find_checks(self, id=None, url=None):
        result, value = None, None
        if id:
            value = str(id)
        elif url:
            url_item = self.find_one_url(name=url)
            if url_item:
                value = url_item.id
        print('value =', value)
        if value:
            with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
                curs.execute(f'{"SELECT * from url_checks"
                             " WHERE url_id=%s"}', (value,))
                result = curs.fetchall()
        return result
