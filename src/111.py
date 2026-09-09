@staticmethod
def conn_decorator(db_name: str, params: dict):
    """Дополняет работу функции подключением к базе данных"""

    def wrapper(func):
        def fun_in(*args, **kwargs):
            conn = psycopg2.connect(dbname=db_name, **params)
            cur = conn.cursor()

            result = func(cur, *args, **kwargs)

            cur.close()
            conn.close()
            return result

        return fun_in

    return wrapper