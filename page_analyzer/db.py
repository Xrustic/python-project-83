import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime
import os


DATABASE_URL = os.getenv('DATABASE_URL')


class DatabaseManager:
    database_url = None

    def __init__(self, app):
        self.app = app

    @staticmethod
    def execute_in_db(func):
        """Декоратор для выполнения функций соединения с базой данных."""
        def inner(*args, **kwargs):
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    result = func(cursor=cursor, *args, **kwargs)
                    conn.commit()
                    return result
        return inner

    @staticmethod
    def with_commit(func):
        def inner(self, *args, **kwargs):
            try:
                with psycopg2.connect(DATABASE_URL) as connection:
                    cursor = connection.cursor(cursor_factory=NamedTupleCursor)
                    result = func(self, cursor, *args, **kwargs)
                    connection.commit()
                    return result
            except psycopg2.Error as e:
                print(f'Ошибка при выполнении транзакции: {e}')
                raise e
        return inner

    @with_commit
    def insert_url(self, cursor, url):
        date = datetime.date.today()
        cursor.execute("""INSERT INTO urls (name, created_at) VALUES (%s, %s)
                       RETURNING *""", (url, date))
        url_data = cursor.fetchone()
        return url_data

    def add_url(self, url, conn=None):
        conn = self.execute_in_db(conn)
        result = self.find_url_by_name(url, conn)
        if result:
            return result, False

        current_date = datetime.datetime.now()
        query = """INSERT INTO urls (name, created_at)
            VALUES (%s, %s);"""
        item_tuple = (url, current_date)
        self.insert_url(query, item_tuple, conn)
        result = self.find_url_by_name(url, conn)
        return result, True

    @execute_in_db
    def find_url_by_id(self, id, cursor):
        cursor.execute("SELECT * from urls WHERE id=%s", (id,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def find_url_by_name(self, name, cursor):
        value = str(name)
        cursor.execute("SELECT * from urls WHERE name=%s", (value,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def get_all_urls(self, cursor):
        query = """SELECT ur.id, ur.name, ur.created_at,
            max(uc.created_at) as last_check, uc.status_code
            FROM urls AS ur
            LEFT JOIN url_checks AS uc on uc.url_id = ur.id
            GROUP BY ur.id, ur.name, ur.created_at, uc.status_code
            ORDER BY ur.id DESC;"""
        cursor.execute(query)
        url_id = cursor.fetchall()
        return url_id

    def add_check(self, url, result_check, conn=None):
        conn = self.execute_in_db(conn)
        current_date = datetime.datetime.now()
        url_item = self.find_url_by_name(url, conn)
        if url_item:
            url_id = url_item.id
        else:
            return False
        status_code = result_check['status_code']
        h1 = result_check['h1']
        title = result_check['title'][:110]
        description = result_check['description'], 160
        query = """INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s);"""
        item_tuple = (url_id, status_code,
                      h1, title, description, current_date)
        self.insert_url(query, item_tuple, conn)
        return True

    @execute_in_db
    def find_checks_by_id(self, id, cursor):
        value = str(id)
        cursor.execute("SELECT * from urls WHERE id=%s", (value,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None
