import os
import sys

import db_connector as dbConn


# Function for subscription
def submit_subscription(data):
    conn = dbConn.db_connector()

    email = data['email']
    today_date = data['today_date']
    payment_id = data['payment_id']

    query = ''
    row_count = 0

    query = ''' INSERT INTO subscription (email, date, payment_id) 
                                    VALUES (%s, %s, %s) '''
    values = (str(email), str(today_date), str(payment_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


def get_last_subscription_date(email):
    conn = dbConn.db_connector()

    query = ''' SELECT date FROM subscription WHERE email = %s ORDER BY id DESC LIMIT 1 '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_month_subscription_count(lastMonth):
    conn = dbConn.db_connector()

    query = """ SELECT COUNT(date) FROM subscription WHERE date LIKE '%""" + \
        str(lastMonth) + """%' """

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()
