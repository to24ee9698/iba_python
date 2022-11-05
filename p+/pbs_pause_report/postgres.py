import psycopg2
import psycopg2.extras


class Postgres:

    def __init__(self, host, port, db_name, username, password) -> None:
        """
        """
        super().__init__()
        self._host = host
        self._port = port
        self._db_name = db_name
        self._user = username
        self._pwd = password
        self.conn = None

    def __enter__(self):
        try:
            self.conn = psycopg2.connect(
                host=self._host,
                port=self._port,
                database=self._db_name,
                user=self._user,
                password=self._pwd,
                cursor_factory=psycopg2.extras.DictCursor,
            )
            return self.conn
        except psycopg2.OperationalError:
            pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()




