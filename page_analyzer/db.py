import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime
import os
# import requests
# from bs4 import BeautifulSoup


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
        return url_id

    @execute_in_db
    def find_url_by_name(self, name, cursor):
        value = str(name)
        cursor.execute("SELECT * from urls WHERE name=%s", (value,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def get_all_urls(self, cursor):
        query = '''
            SELECT u.id, u.name, MAX(c.created_at) AS last_checked,
            MAX(c.status_code) AS last_status_code
            FROM urls u
            LEFT JOIN url_checks c ON u.id = c.url_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        '''
        cursor.execute(query)
        urls_data = cursor.fetchall()
        return urls_data

    # def fetch_and_parse_url(url):
    #     try:
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             soup = BeautifulSoup(response.content, 'html.parser')
    #             return {
    #                 'title': soup.find('title').text if soup.find('title')
    #                 else None,
    #                 'h1': soup.find('h1').text if soup.find('h1') else None,
    #                 'description': soup.find('meta',
    #                                          attrs={'name': 'description'})
    #                 ['content'] if soup.find('meta',
    #                                          attrs={'name': 'description'})
    #                 else None,
    #                 'status_code': response.status_code
    #             }
    #         else:
    #             return {'error': 'Произошла ошибка при проверке'}
    #     except requests.RequestException:
    #         return {'error': 'Произошла ошибка при проверке'}

    # @execute_in_db
    # def add_check(self, url, result_check, cursor):
    #     status_code = result_check['status_code']
    #     h1 = result_check['h1']
    #     title = result_check['title'][:110]
    #     description = result_check['description'], 160
    #     cursor.execute(
    #         '''INSERT INTO url_checks (url_id, status_code, h1, title,
    #         description, created_at)
    #         VALUES (%s, %s, %s, %s, %s, %s)''',
    #         (url, status_code, h1, title, description, datetime.now())
    #     )
    #     return True
    @execute_in_db
    def add_check(self, url, result_check, cursor):
        print(cursor.execute(
            '''INSERT INTO url_checks (url_id, status_code, h1, title,
            description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)''',
            (url, result_check['status_code'], result_check['h1'],
             result_check['title'], result_check['description'],
             datetime.datetime.now())
        ))
        checks = cursor.fetchone()
        print(checks, 'check')
        return checks

    @execute_in_db
    def find_checks_by_id(self, id, cursor):
        value = str(id)
        cursor.execute("SELECT * from url_checks WHERE url_id=%s", (value,))
        checks = cursor.fetchall()
        print(checks, 'view')
        return checks
