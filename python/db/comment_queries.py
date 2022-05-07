import os
import sys

import db_connector as dbConn


# Function for submit_comment
def submit_comment(data):
    conn = dbConn.db_connector()

    email = data['email']
    today_date = data['today_date']
    comment = data['comment']
    receipt_id = data['receipt_id']

    query = ''
    row_count = 0

    query = ''' INSERT INTO comments (receipt_id, date, email, comment) 
                                    VALUES (%s, %s, %s, %s) '''
    values = (int(receipt_id), str(today_date), str(email), str(comment))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


def get_comments_by_id(id):
    conn = dbConn.db_connector()

    query = ''' SELECT comments.id, receipt_id, date, comments.email, users.name, comment FROM comments
                INNER JOIN users ON users.email = comments.email WHERE receipt_id = %s ORDER BY date DESC '''
    values = (int(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()
