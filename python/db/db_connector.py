import mysql.connector


def db_connector():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="meal_master"
    )

    return conn
