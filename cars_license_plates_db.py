import sqlite3
from sqlite3 import Error
from datetime import datetime

SQL_DB_FILE = r"C:\sqlite\sqlite.db"
TEST_SQL_DB_FILE = r"C:\sqlite\test_sqlite.db"

SQL_CREATE_TABLE = """ CREATE TABLE IF NOT EXISTS {table} (
                                    id integer PRIMARY KEY,
                                    plate_number CHARACTER(30) NULL,
                                    car_type CHARACTER(30) NULL,
                                    prohibited tinyint NULL,
                                    timestamp DATETIME NOT NULL
                                ); """

INSERT_ROW = "INSERT INTO {table} (plate_number, car_type , prohibited, timestamp)" \
             " VALUES ('{plate_number}', '{car_type}', {prohibited}, '{timestamp}')"

SELECT_ALL_QUERY = "SELECT * FROM {table}"


class DB:
    def __init__(self, test=False):
        self.table_name = 'cars_license_plates'
        self.sql_db_file = TEST_SQL_DB_FILE if test else SQL_DB_FILE
        self.create_table()

    def create_connection(self):
        """ create a database connection to a SQLite database """
        conn = None
        try:
            conn = sqlite3.connect(self.sql_db_file)
        except Error as e:
            print(e)
        return conn

    def drop_table(self):
        sql_con = self.create_connection()
        c = sql_con.cursor()
        c.execute("DROP TABLE {table}".format(table=self.table_name))
        sql_con.commit()

    def create_table(self):
        """ create a table from the create_table_sql statement """
        try:
            sql_con = self.create_connection()
            c = sql_con.cursor()
            c.execute(SQL_CREATE_TABLE.format(table=self.table_name))
        except Error as e:
            print(e)

    def add_row(self, plate_number, car_type, prohibited):
        sql_con = self.create_connection()
        c = sql_con.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_cmd = INSERT_ROW.format(table=self.table_name,
                                       plate_number=plate_number,
                                       car_type=car_type,
                                       prohibited=prohibited,
                                       timestamp=timestamp
                                       )
        c.execute(insert_cmd)
        sql_con.commit()

    def show_rows(self):
        sql_con = self.create_connection()
        c = sql_con.cursor()
        c.execute(SELECT_ALL_QUERY.format(table=self.table_name))
        for i in c.fetchall():
            print(i)
        c.close()
