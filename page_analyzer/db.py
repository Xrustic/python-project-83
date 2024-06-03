import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime


class DatabaseManager:
    database_url = None

    def __init__(self, database_url):
        self.database_url = database_url

    # @staticmethod
    # def execute_in_db(func):
    #     """Декоратор для выполнения функций соединения с базой данных."""
    #     def inner(*args, **kwargs):
    #         with psycopg2.connect(args[0].app.config['DATABASE_URL']) as 
    # conn:
    #             with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
    #                 result = func(cursor=cursor, *args, **kwargs)
    #                 conn.commit()
    #                 return result
    #     return inner

    # @staticmethod
    # def with_commit(func):
    #     def inner(self, *args, **kwargs):
    #         database = self.app.config['DATABASE_URL']
    #         try:
    #             with psycopg2.connect(database) as connection:
    #                 cursor = connection.cursor(cursor_factory=
    # NamedTupleCursor)
    #                 result = func(self, cursor, *args, **kwargs)
    #                 connection.commit()
    #                 return result
    #         except psycopg2.Error as e:
    #             print(f'Ошибка при выполнении транзакции: {e}')
    #             raise e
    #     return inner

    # @with_commit
    # def insert_url(self, cursor, url):
    #     date = datetime.date.today()
    #     cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)"
    #                    "RETURNING *", (url, date))
    #     url_data = cursor.fetchone()
    #     return url_data
    def __connect(self, conn=None):
        if conn is None:
            conn = psycopg2.connect(self.database_url)
            return conn

    def __do_insert(self, query, values, *args, conn=None):
        with psycopg2.connect(args[0].app.config['DATABASE_URL']) as conn:
            conn = self.__connect(conn)
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(query, values)
        conn.commit()

    def __do_select(self, query, values=None, *args, conn=None):
        with psycopg2.connect(args[0].app.config['DATABASE_URL']) as conn:
            conn = self.__connect(conn)
            with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                cursor.execute(query, values)
                result = cursor.fetchall()
        return result

    def add_url(self, url, conn=None):
        conn = self.__connect(conn)
        result = self.find_urls_by_name(url, conn)
        if result:
            return result, False

        current_date = datetime.datetime.now()
        query = """INSERT INTO urls (name, created_at)
            VALUES (%s, %s);"""
        item_tuple = (url, current_date)
        self.__do_insert(query, item_tuple, conn)
        result = self.find_urls_by_name(url, conn)
        return result, True

    def find_urls_by_id(self, id, conn=None):
        conn = self.__connect(conn)
        query = "SELECT * from urls WHERE id=%s"
        result = self.__do_select(query, (id,), conn)
        if result:
            result = result[0]
        return result

    def find_urls_by_name(self, name, conn=None):
        conn = self.__connect(conn)
        result = None
        value = str(name)
        if value:
            query = "SELECT * from urls WHERE name=%s"
            result = self.__do_select(query, (value,), conn)
        if result:
            result = result[0]
        return result

    # def find_urls(self, id=None, name=None):
    #     result = None
    #     key, value = None, None
    #     if id:
    #         key, value = 'id', str(id)
    #     elif name:
    #         key, value = 'name', str(name)
    #     if key:
    #         conn = self.__connect()
    #         with conn.cursor(cursor_factory=NamedTupleCursor) as curs:
    #             curs.execute(f"SELECT * from urls WHERE {key}=%s", (value,))
    #             result = curs.fetchall()
    #     return result

    # def find_one_url_by_id(self, id, conn=None):
    #     result = self.find_urls_by_id(id, conn)
    #     if result:
    #         result = result[0]
    #     return result

    # def find_one_url_by_name(self, name, conn=None):
    #     result = self.find_urls_by_name(name, conn)
    #     if result:
    #         result = result[0]
    #     return result

    def get_all_url(self, conn=None):
        conn = self.__connect(conn)
        query = """SELECT ur.id, ur.name, ur.created_at,
            max(uc.created_at) as last_check, uc.status_code
            FROM urls AS ur
            LEFT JOIN url_checks AS uc on uc.url_id = ur.id
            GROUP BY ur.id, ur.name, ur.created_at, uc.status_code
            ORDER BY ur.id DESC;"""
        result = self.__do_select(query, conn=conn)
        return result

    def add_check(self, url, result_check, conn=None):
        conn = self.__connect(conn)
        current_date = datetime.datetime.now()
        url_item = self.find_urls_by_name(url, conn)
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
        self.__do_insert(query, item_tuple, conn)
        return True

    def find_checks_by_id(self, id, conn=None):
        conn = self.__connect(conn)
        result = None
        value = str(id)
        if value:
            query = "SELECT * from url_checks WHERE url_id=%s"
            result = self.__do_select(query, (value,), conn)
        return result
