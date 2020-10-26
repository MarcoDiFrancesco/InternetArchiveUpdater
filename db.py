import psycopg2
import os


class PG:
    def __init__(self, conn_string: str = os.environ["PG_CONNSTRING"]):
        self.conn = psycopg2.connect(conn_string, sslmode="require")

    def query(self, query: str, params: list = None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, params)

    def fetchall(self, query: str, params: list = None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchall()
        return result

    def fetchone(self, query: str, params: list = None):
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(query, params)
                result = cur.fetchone()[0]
        return result

    def insert_urls(self, my_list):
        """
        Query to insert all values of list into table.
        If value gives conflict do nothing.
        """
        # Return if empty
        if not my_list:
            return
        query_string = "INSERT INTO url (value) VALUES "
        for item in my_list:
            query_string += f"('{item}'), "
        query_string = query_string[:-2]
        query_string += " ON CONFLICT (value) DO NOTHING;"
        self.query(query_string)

    def get_urls(self):
        """
        Query to get 10 urls and set their state to 1
        """
        query_select = (
            "SELECT value FROM url WHERE status = 0 ORDER BY random() LIMIT 10;"
        )
        urls = self.fetchall(query_select)
        # From list of tuples => list
        urls = [url[0] for url in urls]
        if urls:
            query_update = "UPDATE url SET status = 1 WHERE value in ("
            for url in urls:
                query_update += f"'{url}', "
            query_update = query_update[:-2]
            query_update += ");"
            self.query(query_update)
        return urls

    def get_status(self):
        """
        Get query progress e.g. 13/88
        """
        query = "SELECT COUNT(*) FROM url WHERE status = 1;"
        completed = self.fetchone(query)
        query = "SELECT COUNT(*) FROM url"
        total = self.fetchone(query)
        return f"{completed}/{total}"
