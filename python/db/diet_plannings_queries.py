import os
import sys

import db_connector as dbConn


# Function for add_request_planning
def add_request_planning(data):
    conn = dbConn.db_connector()

    email = data['email']
    today_date = data['today_date']
    category = data['category']
    age = data['age']
    gender = data['gender']
    height = data['height']
    weight = data['weight']
    desired_weight = data['desired_weight']
    veg_or_not = data['veg_or_not']
    preferred_foods = data['preferred_foods']
    allergies = data['allergies']
    hours = data['hours']
    status = data['status']

    query = ''
    row_count = 0

    query = """ INSERT INTO diet_plannings (email, date, category, age, gender, height, weight, desired_weight,
                                    veg_or_not, preferred_foods, allergies, hours, status, plan, couch_id) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '', '') """
    values = (str(email), str(today_date), str(category), str(age), str(gender), str(height), str(
        weight), str(desired_weight), str(veg_or_not), str(preferred_foods), str(allergies), str(hours), str(status))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


def get_diet_plannings_by_user(email):
    conn = dbConn.db_connector()

    query = ''' SELECT id, email, date, category, status FROM diet_plannings WHERE email = %s ORDER BY date DESC '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


def get_diet_plannings_by_id(id):
    conn = dbConn.db_connector()

    query = ''' SELECT id, email, date, category, age, gender, height, weight, desired_weight,
                        veg_or_not, preferred_foods, allergies, hours, status, plan, couch_id FROM diet_plannings WHERE id = %s '''
    values = (str(id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()



def get_diet_plannings_count():
    conn = dbConn.db_connector()

    query = """ SELECT COUNT(diet_plannings.id) FROM diet_plannings
                INNER JOIN users ON users.email = diet_plannings.email WHERE status = 'requested' """

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


def get_diet_plannings():
    conn = dbConn.db_connector()

    query = """ SELECT diet_plannings.id, name, diet_plannings.email, date, category, status FROM diet_plannings
                INNER JOIN users ON users.email = diet_plannings.email WHERE status = 'requested' ORDER BY date DESC """

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for update_requested_plan
def update_requested_plan(data):
    conn = dbConn.db_connector()

    id = data['id']
    plan = data['plan']
    couch = data['couch']
    status = data['status']

    query = ''
    row_count = 0

    query = ''' UPDATE diet_plannings SET plan = %s, couch_id = %s, status = %s WHERE id = %s '''
    values = (str(plan), str(couch), str(status), int(id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count
