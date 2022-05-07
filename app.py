from fileinput import filename
import os
import sys
import paypalrestsdk

from googleapiclient import discovery
from googleapiclient.discovery import build
from google.oauth2 import service_account

import hashlib
import time
from datetime import datetime, date, time, timedelta
from flask import Flask, render_template, redirect, jsonify, url_for, request, session

sys.path.append(os.path.abspath('./python/'))
sys.path.append(os.path.abspath('python/db'))

import users_queries as uq
import recipes_queries as rq
import diet_plannings_queries as dpq
import comment_queries as cq
import subscription_queries as sq

import email_sender as sender
import utils

app = Flask(__name__)

app.secret_key = "food_recipes"
# app.static_folder = "templates/"
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(APP_ROOT)


# Paypal
paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "ASKzM_YMG3PZHVkE68UXS5xlYJSEni2lEK9qfpjLfZAgapi0t_RCLSqhqICXXkabVJL-Z4RdusZqWU4x",
    "client_secret": "ECNMjNUmDlN7b9F0IsOB--X7kmzaeLZR71NmJma5r5KPRNBWgZhAT5nJvGmVwT-kDRlInqWjB594bye9"})


# Google spreadsheet
credentials = None
SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'python/services_account.json'
API_SERVER_NAME = "sheets"
API_VERSION = "v4"
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = discovery.build('sheets', 'v4', credentials=credentials)
SPREADSHEET_ID = '1WmqJNmDjGUKXGYoc92K-mKtTZJkji7lvyCZTBUwQYFc'


@app.route('/')
@app.route('/index')
def index():

    breakfast, lunch, dinner = rq.get_top_10_category_recipes()

    usersCount = 0
    couchesCount = 0
    recipesCount = 0
    planningsCount = 0
    lastMonthSubsCount = 0
    thisMonthSubsCount = 0

    if 'couchId' in session:
        usersCount = uq.get_users_count("users")[0][0]
        couchesCount = uq.get_users_count("couch")[0][0]
        recipesCount = rq.get_recipes_count()[0][0]
        planningsCount = dpq.get_diet_plannings_count()[0][0]

        now = datetime.now()
        last_month = now.month - 1 if now.month > 1 else 12
        this_year = now.year

        this_month = datetime.today().strftime('%Y-%m')

        last_month_year = this_year

        if last_month == 1:
            last_month_year = this_year - 1

        if len(str(last_month)) < 2:
            last_month = "0" + str(last_month)

        lastMonth = str(last_month_year) + "-" + str(last_month)

        lastMonthSubsCount = sq.get_month_subscription_count(lastMonth)[
            0][0]

        thisMonthSubsCount = sq.get_month_subscription_count(this_month)[
            0][0]

    return render_template('index.html', breakfast=breakfast, lunch=lunch, dinner=dinner,
                           usersCount=usersCount, couchesCount=couchesCount, recipesCount=recipesCount,
                           planningsCount=planningsCount, lastMonthSubsCount=lastMonthSubsCount,
                           thisMonthSubsCount=thisMonthSubsCount)


@app.route('/authentication')
def authentication():
    if 'userId' in session:
        return redirect('/index')
    else:
        return render_template('authentication.html')


@app.route('/account')
def account():
    if 'userId' in session or 'couchId' in session:
        return render_template('account.html')
    else:
        return redirect('/index')


@app.route('/my-recipes')
def my_recipes():
    if 'userId' not in session:
        return redirect('/index')

    else:

        email = session['userId']
        recipes = rq.get_all_my_recipes(email)
        return render_template('my_recipes.html', recipes=recipes)


@app.route('/all-recipes')
def all_recipes():
    if 'userId' in session or 'couchId' in session:
        search = request.args.get('search', "")

        recipes = rq.get_all_recipes(search)
        return render_template('all_recipes.html', recipes=recipes)
    else:
        return redirect('/index')


@app.route('/add-recipes')
def add_recipes():
    if 'userId' not in session:
        return redirect('/index')
    else:
        return render_template('add_recipes.html')


@app.route('/edit-receipt')
def edit_receipt():
    if 'userId' not in session:
        return redirect('/index')
    else:

        id = request.args['id']
        details = rq.get_receipt_details(id)
        return render_template('edit_receipt.html', details=details[0])


@app.route('/my_recipes_details')
def my_recipes_details():

    id = request.args['id']
    details = rq.get_receipt_details(id)
    comments = cq.get_comments_by_id(id)

    if len(details) == 0:
        return redirect('/index')

    else:
        return render_template('my_recipes_details.html', details=details[0], comments=comments)


@app.route('/view_recipes_details')
def view_recipes_details():

    id = request.args['id']
    details = rq.get_receipt_details(id)
    comments = cq.get_comments_by_id(id)

    if len(details) == 0:
        return redirect('/index')

    else:
        return render_template('view_recipes_details.html', details=details[0], comments=comments)


@app.route('/my-plannings')
def my_plannings():

    email = session['userId']
    details = dpq.get_diet_plannings_by_user(email)

    last_sub_date = sq.get_last_subscription_date(email)
    if len(last_sub_date) > 0:
        last_sub_date = last_sub_date[0][0]
        today = datetime.today().strftime('%Y-%m-%d')

        date_format = "%Y-%m-%d"
        a = datetime.strptime(last_sub_date, date_format)
        b = datetime.strptime(today, date_format)
        day_count = b - a

        days = day_count.days

    else:
        days = 32

    if 'userId' not in session:
        return redirect('/index')
    else:

        is_show = "yes"
        if days > 30:
            is_show = "no"

        return render_template('my_plannings.html', details=details, days=days, is_show=is_show)


@app.route('/view-my-plannings')
def view_my_plannings():

    id = request.args['id']
    details = dpq.get_diet_plannings_by_id(id)

    if 'userId' not in session:
        return redirect('/index')
    else:
        return render_template('view_my_planning.html', details=details)


@app.route('/couches')
def couches():

    couch_email = session['couchId']
    details = uq.get_couches(couch_email)

    if 'couchId' not in session:
        return redirect('/index')
    else:
        return render_template('couches.html', details=details)


@app.route('/requested-plannings')
def requested_plannings():

    details = dpq.get_diet_plannings()

    if 'couchId' not in session:
        return redirect('/index')
    else:
        return render_template('requested_plannings.html', details=details)


@app.route('/view-requested-plannings')
def view_requested_plannings():

    id = request.args['id']
    details = dpq.get_diet_plannings_by_id(id)

    if 'couchId' not in session:
        return redirect('/index')
    else:
        return render_template('view_requested_planning.html', details=details)


@app.route('/diet-journal')
def diet_journal():

    email = session['userId']

    # Check check exist
    is_exist_request = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID)
    is_exist_response = is_exist_request.execute()
    is_exist_sheets = is_exist_response.get('sheets', [])

    is_exist = "no"
    for i in is_exist_sheets:
        if i['properties']['title'] == email:
            is_exist = "yes"
            break

    values = []
    if is_exist == "yes":
        # Get all
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                     range=email).execute()
        values = result.get('values', [])

    if 'userId' not in session:
        return redirect('/index')
    else:
        return render_template('diet_journal.html', details=enumerate(values))


@app.route('/view_diet_journal')
def view_diet_journal():

    id = request.args['id']
    email = session['userId']

    # Get all
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                 range=email).execute()
    values = result.get('values', [])

    if 'userId' not in session:
        return redirect('/index')
    else:
        return render_template('view_diet_journal.html', details=values[int(id)])


# Route for user_sign_up
@app.route('/user_sign_up', methods=['GET', 'POST'])
def user_sign_up():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            name = request.form.get('name')
            email = request.form.get('email')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(name) == 0 or len(email) == 0 or len(psw) == 0 or
                    len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            elif utils.validate_email(email) == False:
                return jsonify({'error': "Email not valid. Please check your email!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()
                data = {
                    'name': name,
                    'email': email,
                    'psw': psw,
                    'account_type': 3
                }

                # Check email already exist
                is_exist = uq.is_exist_email(email)
                if is_exist > 0:
                    return jsonify({'error': "Email already exist!"})

                else:
                    is_created = uq.registration(data)
                    if is_created > 0:
                        return jsonify({'success': "Account has been created. Please sign in!"})

                    else:
                        return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'redirect': url_for('authentication')})


# Route for user_sign_in
@app.route('/user_sign_in', methods=['GET', 'POST'])
def user_sign_in():

    if request.method == "POST":

        if 'userId' in session:
            return jsonify({'redirect': url_for('index')})

        else:
            email = request.form.get('email')
            psw = request.form.get('psw')

            if (len(email) == 0 or len(psw) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                psw = hashlib.md5(psw.encode()).hexdigest()

                # Check email already exist
                details = uq.login(email, psw)
                if len(details) > 0:
                    account_type = int(details[0][3])

                    if account_type in [1, 2]:
                        session['couchId'] = str(details[0][1])

                        if account_type == 1:
                            session['couchType'] = "super"
                        else:
                            session['couchType'] = "normal"

                    else:
                        session['userId'] = str(details[0][1])

                    return jsonify({'redirect': url_for('index')})

                else:
                    return jsonify({'error': "Sign in failed. Please try again!"})

    return jsonify({'redirect': url_for('authentication')})


# Route for add_couch
@app.route('/add_couch', methods=['GET', 'POST'])
def add_couch():

    if request.method == "POST":

        name = request.form.get('name')
        email = request.form.get('email')
        psw = request.form.get('psw')
        account_type = request.form.get('type')

        if (len(name) == 0 or len(email) == 0 or len(psw) == 0):

            return jsonify({'error': "Fields are empty!"})

        elif utils.validate_email(email) == False:
            return jsonify({'error': "Email not valid. Please check your email!"})

        else:

            psw = hashlib.md5(psw.encode()).hexdigest()
            data = {
                'name': name,
                'email': email,
                'psw': psw,
                'account_type': int(account_type)
            }

            # Check email already exist
            is_exist = uq.is_exist_email(email)
            if is_exist > 0:
                return jsonify({'error': "Email already exist!"})

            else:
                is_created = uq.registration(data)
                if is_created > 0:
                    return jsonify({'success': "Account has been created.!"})

                else:
                    return jsonify({'error': "Account not created. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for remove_couch
@app.route('/remove_couch', methods=['GET', 'POST'])
def remove_couch():

    if request.method == "POST":

        email = request.form.get('email')
        is_removed = uq.remove_couch(email)
        if is_removed > 0:
            return jsonify({'success': "Account has been removed.!"})

        else:
            return jsonify({'error': "Account not removed. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for sign out
@app.route('/sign_out')
def sign_out():
    if 'userId' in session:
        session.pop('userId', None)

    elif 'couchId' in session:
        session.pop('couchId', None)
        session.pop('couchType', None)

    return redirect(url_for('index'))


# Route for get account details
@app.route('/account_details', methods=['GET', 'POST'])
def account_details():

    if 'userId' in session or 'couchId' in session:
        email = ""
        if 'userId' in session:
            email = session['userId']
        else:
            email = session['couchId']

        details = uq.get_account_details(email)
        data = {}

        if (len(details) > 0):
            data = {
                'name': details[0][0],
                'email': details[0][1]
            }

        return jsonify({'data': data})

    else:
        return jsonify({'redirect': url_for('index')})


# Route for update user details
@app.route('/update_user_details', methods=['GET', 'POST'])
def update_user_details():

    if request.method == "POST":
        if 'userId' in session or 'couchId' in session:
            name = request.form.get('name')
            email = request.form.get('email')

            if (len(name) == 0 or len(email) == 0):
                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    'name': name,
                    'email': email
                }

                # Update
                is_updated = uq.update_user_details(data)
                if is_updated > 0:
                    return jsonify({'success': "Account details has been updated!"})

                else:
                    return jsonify({'error': "Account details not updated. Please try again!"})
        else:
            return jsonify({'redirect': url_for('index')})

    return jsonify({'redirect': url_for('account')})


# Route for update user psw
@app.route('/update_user_psw', methods=['GET', 'POST'])
def update_user_psw():

    if request.method == "POST":

        if 'userId' in session or 'couchId' in session:
            email = request.form.get('email')
            psw = request.form.get('psw')
            cpsw = request.form.get('cpsw')

            if (len(email) == 0 or len(psw) == 0 or len(cpsw) == 0):

                return jsonify({'error': "Fields are empty!"})

            elif psw != cpsw:
                return jsonify({'error': "Password and confirm password not matched!"})

            else:

                # Update
                psw = hashlib.md5(psw.encode()).hexdigest()
                is_updated = uq.update_user_psw(email, psw)
                if is_updated > 0:
                    return jsonify({'success': "Account password has been updated!"})

                else:
                    return jsonify({'error': "Account password not updated. Please try again!"})

        else:
            return jsonify({'redirect': url_for('index')})

    return jsonify({'redirect': url_for('account')})


# Route for add new receipt
@app.route('/add_new_receipt', methods=['GET', 'POST'])
def add_new_receipt():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            title = request.form.get('title')
            serves = request.form.get('serves')
            cooking_time = request.form.get('cooking-time')
            prep_time = request.form.get('prep-time')
            category = request.form.get('category')
            ingredients = request.form.get('ingredients')
            description = request.form.get('description')
            method = request.form.get('method')
            calories = request.form.get('calories')
            protein = request.form.get('protein')
            carbohydrates = request.form.get('carbohydrates')
            total_fats = request.form.get('total-fats')
            dietary_fibre = request.form.get('dietary-fibre')
            cholesterol = request.form.get('cholesterol')
            sodium = request.form.get('sodium')
            total_sugars = request.form.get('total-sugars')

            thumbnail = request.files.get('thumbnail')
            ingredients_image = request.files.get('ingredients-image')

            if (len(title) == 0 or len(serves) == 0 or len(cooking_time) == 0 or len(prep_time) == 0
                or len(category) == 0 or len(ingredients) == 0 or
                len(description) == 0 or len(method) == 0 or len(calories) == 0 or len(protein) == 0 or
                len(carbohydrates) == 0 or len(total_fats) == 0 or len(dietary_fibre) == 0 or len(cholesterol) == 0 or
                    len(sodium) == 0 or len(total_sugars) == 0 or thumbnail == None or ingredients_image == None):

                return jsonify({'error': "Fields are empty!"})

            else:

                key_no = utils.random_number()
                date = utils.date_picker()
                user_email = session['userId']

                save_folder = os.path.join(
                    APP_ROOT, 'static/images/recipes/' + key_no + "/")

                if not os.path.exists(save_folder):
                    os.makedirs(save_folder)

                thumbnail_name = utils.file_save(thumbnail, save_folder)
                ingredients_image_name = utils.file_save(
                    ingredients_image, save_folder)

                data = {
                    "title": title,
                    "serves": serves,
                    "cooking_time": cooking_time,
                    "prep_time": prep_time,
                    "category": category,
                    "ingredients": ingredients,
                    "description": description,
                    "method": method,
                    "calories": calories,
                    "protein": protein,
                    "carbohydrates": carbohydrates,
                    "total_fats": total_fats,
                    "dietary_fibre": dietary_fibre,
                    "cholesterol": cholesterol,
                    "sodium": sodium,
                    "total_sugars": total_sugars,
                    "thumbnail": thumbnail_name,
                    "ingredients_image": ingredients_image_name,
                    "key_no": key_no,
                    "date": date,
                    "user_email": user_email
                }

                # Check email already exist
                is_added = rq.add_new_recipes(data)
                if is_added > 0:
                    return jsonify({'success': "Your receipt added successfully"})

                else:
                    return jsonify({'error': "Your receipt added not successfully. Please try again!"})

    return jsonify({'redirect': url_for('add_recipes')})


# Route for edit exist receipt
@app.route('/edit_exist_receipt', methods=['GET', 'POST'])
def edit_exist_receipt():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            id = request.form.get('id')
            title = request.form.get('title')
            serves = request.form.get('serves')
            cooking_time = request.form.get('cooking-time')
            prep_time = request.form.get('prep-time')
            category = request.form.get('category')
            ingredients = request.form.get('ingredients')
            description = request.form.get('description')
            method = request.form.get('method')
            calories = request.form.get('calories')
            protein = request.form.get('protein')
            carbohydrates = request.form.get('carbohydrates')
            total_fats = request.form.get('total-fats')
            dietary_fibre = request.form.get('dietary-fibre')
            cholesterol = request.form.get('cholesterol')
            sodium = request.form.get('sodium')
            total_sugars = request.form.get('total-sugars')

            if (len(title) == 0 or len(serves) == 0 or len(cooking_time) == 0 or len(prep_time) == 0
                or len(category) == 0 or len(ingredients) == 0 or
                len(description) == 0 or len(method) == 0 or len(calories) == 0 or len(protein) == 0 or
                len(carbohydrates) == 0 or len(total_fats) == 0 or len(dietary_fibre) == 0 or len(cholesterol) == 0 or
                    len(sodium) == 0 or len(total_sugars) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                data = {
                    "title": title,
                    "serves": serves,
                    "cooking_time": cooking_time,
                    "prep_time": prep_time,
                    "category": category,
                    "ingredients": ingredients,
                    "description": description,
                    "method": method,
                    "calories": calories,
                    "protein": protein,
                    "carbohydrates": carbohydrates,
                    "total_fats": total_fats,
                    "dietary_fibre": dietary_fibre,
                    "cholesterol": cholesterol,
                    "sodium": sodium,
                    "total_sugars": total_sugars,
                    "key_no": id
                }

                # Check email already exist
                is_added = rq.edit_exist_receipt(data)
                if is_added > 0:
                    return jsonify({'success': "Your receipt update successfully"})

                else:
                    return jsonify({'error': "Your receipt update not successfully. Please try again!"})

    return jsonify({'redirect': url_for('add_recipes')})


# Route for request my planning
@app.route('/request_my_planning', methods=['GET', 'POST'])
def request_my_planning():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            category = request.form.get('category')
            age = request.form.get('age')
            gender = request.form.get('gender')
            height = request.form.get('height')
            weight = request.form.get('weight')
            desired_weight = request.form.get('desired_weight')
            veg_or_not = request.form.get('veg_or_not')
            preferred_foods = request.form.get('preferred_foods')
            allergies = request.form.get('allergies')
            hours = request.form.get('hours')

            if (len(category) == 0 or len(age) == 0 or len(gender) == 0 or len(height) == 0 or
                    len(weight) == 0 or len(desired_weight) == 0 or len(veg_or_not) == 0 or len(preferred_foods) == 0 or len(hours) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                email = session['userId']
                today_date = datetime.today().strftime('%Y-%m-%d')
                data = {
                    'email': email,
                    'today_date': today_date,
                    'category': category,
                    'age': age,
                    'gender': gender,
                    'height': height,
                    'weight': weight,
                    'desired_weight': desired_weight,
                    'veg_or_not': veg_or_not,
                    'preferred_foods': preferred_foods,
                    'allergies': allergies,
                    'hours': hours,
                    'status': "requested"
                }

                is_requested = dpq.add_request_planning(data)
                if is_requested > 0:
                    return jsonify({'success': "Planning requested.!"})

                else:
                    return jsonify({'error': "Planning not requested. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for add_requested_plan
@app.route('/add_requested_plan', methods=['GET', 'POST'])
def add_requested_plan():

    if request.method == "POST":

        if 'couchId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            id = request.form.get('id')
            plan = request.form.get('plan')

            if (len(plan) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                couchId = session['couchId']
                data = {
                    'id': id,
                    'plan': plan,
                    'couch': couchId,
                    'status': "received"
                }

                is_updated = dpq.update_requested_plan(data)
                if is_updated > 0:
                    return jsonify({'success': "Plan Updated.!"})

                else:
                    return jsonify({'error': "Plan not updated. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Route for submit_comment
@app.route('/submit_comment', methods=['GET', 'POST'])
def submit_comment():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            comment = request.form.get('comment')
            receipt_id = request.form.get('receipt_id')

            if (len(comment) == 0 or len(receipt_id) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                email = session['userId']
                today_date = datetime.today().strftime('%Y-%m-%d')
                data = {
                    'email': email,
                    'today_date': today_date,
                    'comment': comment,
                    'receipt_id': receipt_id
                }

                is_submitted = cq.submit_comment(data)
                if is_submitted > 0:
                    return jsonify({'success': "Comment Submitted.!"})

                else:
                    return jsonify({'error': "Comment not submit. Please try again!"})

    return jsonify({'redirect': url_for('index')})


# Payment gateway
@app.route('/payment', methods=['POST'])
def payment():

    if 'userId' not in session:
        return jsonify({'redirect': url_for('authentication')})

    else:
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": "http://localhost:3000/payment/execute",
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "amount": {
                    "total": "20.00",
                    "currency": "USD"},
                "description": "Meal master 30 days subscription payment."}]})

        if payment.create():
            print('Payment success!')
        else:
            print(payment.error)

        return jsonify({'paymentID': payment.id})


@app.route('/execute', methods=['POST'])
def execute():

    if 'userId' not in session:
        return jsonify({'redirect': url_for('authentication')})

    else:
        success = False
        payment = paypalrestsdk.Payment.find(request.form['paymentID'])

        if payment.execute({'payer_id': request.form['payerID']}):

            print('Execute success!')
            success = True

            payment_id = request.form['payerID']
            email = session["userId"]
            today_date = datetime.today().strftime('%Y-%m-%d')
            enddate = datetime.today() + timedelta(days=30)
            end_date = enddate.strftime('%Y-%m-%d')

            sender.send_payment_receipt(
                email, payment_id, today_date, end_date)

            data = {
                'email': email,
                'today_date': today_date,
                'payment_id': payment_id
            }

            is_submitted = sq.submit_subscription(data)
            if is_submitted > 0:
                return jsonify({'success': "Payment Successfull.!"})

            else:
                return jsonify({'error': "Payment not successfull. Please try again!"})

        else:
            print(payment.error)
            return jsonify({'error': "Payment not successfull. Please try again!"})

        # return jsonify({'success': success})


# Route for add_diet_journal
@app.route('/add_diet_journal', methods=['GET', 'POST'])
def add_diet_journal():

    if request.method == "POST":

        if 'userId' not in session:
            return jsonify({'redirect': url_for('authentication')})

        else:
            date = request.form.get('date')
            meal_items = request.form.get('meal_items')
            carbs = request.form.get('carbs')
            fat = request.form.get('fat')
            protein = request.form.get('protein')
            calories = request.form.get('calories')
            water = request.form.get('water')
            exercise = request.form.get('exercise')
            review = request.form.get('review')
            type = request.form.get('type')

            if (len(date) == 0 or len(meal_items) == 0 or len(carbs) == 0 or len(fat) == 0
                or len(protein) == 0 or len(calories) == 0 or
                    len(water) == 0 or len(exercise) == 0 or len(calories) == 0 or len(protein) == 0 or len(type) == 0):

                return jsonify({'error': "Fields are empty!"})

            else:

                email = session['userId']

                # Check check exist
                is_exist_request = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID)
                is_exist_response = is_exist_request.execute()
                is_exist_sheets = is_exist_response.get('sheets', [])

                is_exist = "no"
                for i in is_exist_sheets:
                    if i['properties']['title'] == email:
                        is_exist = "yes"
                        break

                # Create new sheet
                if is_exist == "no":
                    request_body = {
                        'requests': [{
                            "addSheet": {
                                "properties": {
                                    "title": email
                                }
                            }
                        }],
                    }

                    create_request = service.spreadsheets().batchUpdate(
                        spreadsheetId=SPREADSHEET_ID, body=request_body)
                    create_response = create_request.execute()

                # Add new recode
                raw_data = [[date, meal_items, carbs, fat, protein,
                             calories, water, exercise, review, type]]
                add_response = service.spreadsheets().values().append(
                    spreadsheetId=SPREADSHEET_ID, range=email + "!A1:J1",
                    valueInputOption="USER_ENTERED", body={"values": raw_data}).execute()

                return jsonify({'success': "Diet Journal added successfully"})

    return jsonify({'redirect': url_for('index')})


# Main
if __name__ == '__main__':

    port = 5000
    url = "http://127.0.0.1:{0}".format(port)
    app.run(port=port, debug=True)
