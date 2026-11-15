import db
import kitchen_db
import os



# توابع ثبت نام و ورود

def sign_up(user, password):
    info = (user, password)
    db.add_user(info)


