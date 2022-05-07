import re
import os
import random
from datetime import datetime


# For validate email
def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True

    else:
        return False


# Function for get current date
def date_picker():
    current_datetime = datetime.now()
    date = str(current_datetime.strftime("%Y-%m-%d"))
    return date


# Function for genarate random number
def random_number():
    rand_no = str(random.randint(100000, 999999))
    return rand_no


# Function for save deseases images
def file_save(image, save_folder):
    if image != None:
        image_name = image.filename
        image.save(save_folder + image_name)

    else:
        image_name = None

    return str(image_name)
