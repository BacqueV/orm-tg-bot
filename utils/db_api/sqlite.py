import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            db_id INTEGER NOT NULL,
            name varchar(255) NOT NULL,
            username varchar(60),
            user_id INTEGER UNIQUE NOT NULL,
            PRIMARY KEY (db_id)
            );
            """
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, name: str, username: str, user_id: int):
        # SQL_EXAMPLE = "INSERT INTO Users(name, username, user_id) VALUES('John', 'JohnDoe', 123456789)"

        sql = """
        INSERT INTO Users(name, username, user_id) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(name, username, user_id), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where user_id=1 AND Name='John'"
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_users(self):
        self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def show_tables(self):
        return self.execute("SELECT name FROM sqlite_master WHERE type='table'", fetchall=True)

    def create_custom_table(self, **kwargs):
        sql = (
            """
            CREATE TABLE table_name=? (
            column_name=? column_type=?
            )
            """)
        return self.execute(sql, parameters=(kwargs,), commit=True)


def logger(statement):
    print(f"""
_____________________________________________________
Executing:
{statement}
_____________________________________________________
""")
