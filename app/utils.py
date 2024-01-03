import hashlib
from  models import LopHoc,HocSinh, Khoi
from datetime import datetime, timedelta
from flask_admin import BaseView, expose
from app import db

from app.models import  User

def  get_user_by_id(user_id):
    return  User.query.get(user_id)
def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        hashlib.md5('123'.encode('utf-8')).hexdigest()

        return  User.query.filter(User.username.__eq__(username.strip()),
                          User.password.__eq__(password)).first()
    return None





