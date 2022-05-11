import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import constants


class PSQLConnection:

    def __enter__(self):
        self.conn = psycopg2.connect(
            dbname=constants.DBNAME,
            user=constants.USER,
            password=constants.PASSWORD,
            host=constants.HOST,
            port=constants.PORT
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise
