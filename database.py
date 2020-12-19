import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'admin',
    'host': 'localhost'
}

db = mysql.connector.connect(**config)
cursor = db.cursor()

DB_NAME = 'todoListApp'

TABLES = {}

TABLES['users'] = (
    "CREATE TABLE `users` ("
    " `id` int(10) NOT NULL AUTO_INCREMENT,"
    " `name` varchar(250) NOT NULL,"
    " `username` varchar(250) NOT NULL,"
    " `password` varchar(250) NOT NULL,"
    " PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB"
)

TABLES['tasks'] = (
    "CREATE TABLE `tasks` ("
    " `id` varchar(250) NOT NULL,"
    " `task` varchar(250) NOT NULL"
    ") ENGINE=InnoDB"
)

def create_database():
    cursor.execute(
        "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    print("Database {} created successfully.".format(DB_NAME))


def create_tables():
    cursor.execute("USE {}".format(DB_NAME))

    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            cursor.execute(table_description)
            print("Table ({}) created successfully".format(table_name), end="")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("Table Exists")
            else:
                print(err.msg)


create_database()
create_tables()