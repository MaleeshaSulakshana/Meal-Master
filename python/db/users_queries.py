import os
from pyclbr import Function
import sys

import db_connector as dbConn


# Function for check exist email
def is_exist_email(email):
    conn = dbConn.db_connector()

    query = ''' SELECT count(email) FROM users WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()[0][0]


# Function for login
def login(email, psw):
    conn = dbConn.db_connector()

    query = ''' SELECT id, email, name, account_type FROM users WHERE email = %s AND psw = %s '''
    values = (str(email), str(psw))

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for registration
def registration(data):
    conn = dbConn.db_connector()

    name = data['name']
    email = data['email']
    psw = data['psw']
    account_type = data['account_type']

    query = ''
    row_count = 0

    query = ''' INSERT INTO users (name, email, psw, account_type) VALUES (%s, %s, %s, %s) '''
    values = (str(name), str(email), str(psw), int(account_type))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get users count
def get_users_count(type):
    conn = dbConn.db_connector()

    if type == "users":
        query = ''' SELECT COUNT(email) FROM users WHERE account_type = 3 '''

    else:
        query = ''' SELECT COUNT(email) FROM users WHERE account_type IN (1,2) '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get profile details
def get_account_details(email):
    conn = dbConn.db_connector()

    query = ''' SELECT name, email FROM users WHERE email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get couches
def get_couches(email):
    conn = dbConn.db_connector()

    query = ''' SELECT name, email FROM users WHERE account_type in (1,2) AND email != %s '''

    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for remove couch
def remove_couch(email):
    conn = dbConn.db_connector()

    query = ''' DELETE FROM users WHERE email = %s '''

    values = (str(email),)
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for update user details
def update_user_details(data):
    conn = dbConn.db_connector()

    email = data['email']
    name = data['name']

    query = ''
    row_count = 0

    query = ''' UPDATE users SET name = %s WHERE email = %s '''
    values = (str(name), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count


# Function for update user psw
def update_user_psw(email, psw):
    conn = dbConn.db_connector()

    query = ''
    row_count = 0

    query = ''' UPDATE users SET psw = %s WHERE email = %s '''
    values = (str(psw), str(email))
    cur = conn.cursor()
    cur.execute(query, values)

    conn.commit()
    row_count = cur.rowcount

    return row_count
