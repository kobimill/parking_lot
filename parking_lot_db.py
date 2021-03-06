import os
import platform
import sqlite3
from sqlite3 import Error
from datetime import datetime

"""
Supporting both Windows & Linux OS
"""
if platform.system() == 'Windows':
    SQL_DB_ROOT_DIR = r"C:\parking_lot_db"
else:  # Linux
    SQL_DB_ROOT_DIR = os.path.join(os.getenv('HOME'), 'parking_lot_db')  # i.e: /home/user/parking_lot_db

if not os.path.isdir(SQL_DB_ROOT_DIR):
    os.mkdir(SQL_DB_ROOT_DIR)

SQL_DB_FILE_NAME = "parking_lot_sqlite.db"
TEST_SQL_DB_FILE_NAME = 'test_' + SQL_DB_FILE_NAME
SQL_DB_FILE = os.path.join(SQL_DB_ROOT_DIR, SQL_DB_FILE_NAME)
TEST_SQL_DB_FILE = os.path.join(SQL_DB_ROOT_DIR, TEST_SQL_DB_FILE_NAME)

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
        self.table_name = 'parking_lot'
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

    def get_records(self):
        sql_con = self.create_connection()
        c = sql_con.cursor()
        c.execute(SELECT_ALL_QUERY.format(table=self.table_name))
        column_names = ', '.join([i[0] for i in c.description])
        rows_info = [column_names]
        for i in c.fetchall():
            '''
            Converting row tuple to str-line:
            i.e:
            (12, '3204525', 'public_transportation', 1, '2020-08-01 12:36:03')
            -->
            '12, 3204525, public_transportation, 1, 2020-08-01 12:36:03'
            '''
            row_line = ', '.join(map(str, i))
            rows_info.append(row_line)

        c.close()
        return rows_info
