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

    def add(self, url):
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

    def find(self, id=None, name=None):
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

    def get_all(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as curs:
            curs.execute(f'{"SELECT * from urls ORDER BY id DESC"}')
            result = curs.fetchall()
        return result
