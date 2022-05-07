import os
import sys

import db_connector as dbConn


# Function for add_new_recipes
def add_new_recipes(data):
    conn = dbConn.db_connector()

    title = data['title']
    serves = data['serves']
    cooking_time = data['cooking_time']
    prep_time = data['prep_time']
    category = data['category']
    ingredients = data['ingredients']
    description = data['description']
    method = data['method']
    calories = data['calories']
    protein = data['protein']
    carbohydrates = data['carbohydrates']
    total_fats = data['total_fats']
    dietary_fibre = data['dietary_fibre']
    cholesterol = data['cholesterol']
    sodium = data['sodium']
    total_sugars = data['total_sugars']
    thumbnail = data['thumbnail']
    ingredients_image = data['ingredients_image']
    receipt_id = data['key_no']
    date = data['date']
    user_email = data['user_email']

    query = ''
    row_count = 0

    query = ''' INSERT INTO recipes (receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                                            , %s, %s, %s, %s, %s, %s, %s) '''
    values = (int(receipt_id), str(user_email), str(title), str(serves), str(cooking_time), str(prep_time), str(ingredients), str(description),
              str(method), str(calories), str(protein), str(
                  carbohydrates), str(total_fats), str(dietary_fibre),
              str(cholesterol), str(sodium), str(total_sugars), str(thumbnail), str(ingredients_image), str(date), str(category))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for edit_exist_receipt
def edit_exist_receipt(data):
    conn = dbConn.db_connector()

    title = data['title']
    serves = data['serves']
    cooking_time = data['cooking_time']
    prep_time = data['prep_time']
    category = data['category']
    ingredients = data['ingredients']
    description = data['description']
    method = data['method']
    calories = data['calories']
    protein = data['protein']
    carbohydrates = data['carbohydrates']
    total_fats = data['total_fats']
    dietary_fibre = data['dietary_fibre']
    cholesterol = data['cholesterol']
    sodium = data['sodium']
    total_sugars = data['total_sugars']
    receipt_id = data['key_no']

    query = ''
    row_count = 0

    query = ''' UPDATE recipes SET title = %s, serves = %s, cooking_time = %s, prep_time = %s
                                    , ingredients = %s, description = %s, method = %s, calories = %s, 
                                    protein = %s, carbohydrates = %s, total_fats = %s, dietary_fibre = %s, cholesterol = %s,
                                    sodium = %s, total_sugars = %s, category = %s WHERE receipt_id = %s '''
    values = (str(title), str(serves), str(cooking_time), str(prep_time), str(ingredients), str(description),
              str(method), str(calories), str(protein), str(
                  carbohydrates), str(total_fats), str(dietary_fibre),
              str(cholesterol), str(sodium), str(total_sugars), str(category), int(receipt_id))
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()

    row_count = cur.rowcount
    return row_count


# Function for get all my recipes
def get_all_my_recipes(email):
    conn = dbConn.db_connector()

    query = ''' SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes WHERE user_email = %s '''
    values = (str(email),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# Function for get recipes count
def get_recipes_count():
    conn = dbConn.db_connector()
    
    query = ''' SELECT COUNT(receipt_id) FROM recipes '''

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get all recipes
def get_all_recipes(search=""):
    conn = dbConn.db_connector()
    query = ""

    if search == "":
        query = ''' SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes ORDER BY id DESC '''

    else:
        query = """ SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes WHERE 
                                    title LIKE '%""" + str(search) + """%' ORDER BY id DESC """

    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()


# Function for get category latest 10 recipes
def get_top_10_category_recipes():
    conn = dbConn.db_connector()

    breakfast = []
    lunch = []
    dinner = []

    query = """ SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes
                                    WHERE category = 'breakfast' ORDER BY id DESC """
    cur = conn.cursor()
    cur.execute(query)
    breakfast = cur.fetchall()

    query = """ SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes
                                    WHERE category = 'lunch' ORDER BY id DESC """
    cur = conn.cursor()
    cur.execute(query)
    lunch = cur.fetchall()

    query = """ SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category FROM recipes
                                    WHERE category = 'dinner' ORDER BY id DESC """
    cur = conn.cursor()
    cur.execute(query)
    dinner = cur.fetchall()

    return breakfast, lunch, dinner


# Function for get_receipt_details
def get_receipt_details(receipt_id):
    conn = dbConn.db_connector()

    query = ''' SELECT receipt_id, user_email, title, serves, cooking_time, prep_time, ingredients, description, method,
                                    calories, protein, carbohydrates, total_fats, dietary_fibre, cholesterol,
                                    sodium, total_sugars, thumbnail, ingredients_image, date, category, name FROM recipes
                                    INNER JOIN users ON users.email = recipes.user_email WHERE receipt_id = %s '''
    values = (int(receipt_id),)

    cur = conn.cursor()
    cur.execute(query, values)
    return cur.fetchall()


# # Function for update user details
# def update_user_details(data):
#     conn = dbConn.db_connector()

#     email = data['email']
#     name = data['name']

#     query = ''
#     row_count = 0

#     query = ''' UPDATE users SET name = %s WHERE email = %s '''
#     values = (str(name), str(email))
#     cur = conn.cursor()
#     cur.execute(query, values)

#     conn.commit()
#     row_count = cur.rowcount

#     return row_count
