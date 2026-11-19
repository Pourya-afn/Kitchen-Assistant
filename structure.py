import db
import kitchen_db
import os
import socket

SESSION_FILE = "current_session_user.txt"

def sign_up(user, password):
    info = (user, password)
    db.add_user(info)


def login(user, password):

    # ۱. بررسی صحت نام کاربری و رمز عبور در دیتابیس مرکزی
    if not db.check_user((user, password)):
        return False,

    last_user = get_last_user()

    # ۲. اگر کاربر جدیدی است که با کاربر قبلی فرق دارد
    if last_user and last_user != user:
        # بررسی اتصال به اینترنت برای جلوگیری از دست رفتن داده‌های کاربر قبلی
        if not check_internet_connection():
            return False,

        # استخراج داده‌های کاربر قبلی از دیتابیس محلی‌اش
        old_user_items = kitchen_db.get_inventory(last_user)

        # سینک کردن داده‌های کاربر قبلی به سرور مرکزی (با متد ساده‌ی شما)
        sync_success = db.sync_inventory_to_mysql(last_user, old_user_items)

        if sync_success:
            # بعد از سینک موفق، فایل دیتابیس یوزر قبلی را پاک می‌کنیم
            kitchen_db.delete_local_db(last_user)
        else:
            return False

    # ۳. آماده‌سازی دیتابیس محلی برای کاربرِ جدید (اگر وجود نداشته باشد ساخته می‌شود)
    kitchen_db.init_db(user)

    # ۴. آپدیت کردن فایل نشستِ آخرین کاربر
    set_last_user(user)

    return True


def get_last_user():
    """خواندن نام آخرین کاربری که روی این سیستم بوده از یک فایل متنی سبک"""
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            return f.read().strip()
    return None


def set_last_user(username):
    with open(SESSION_FILE, "w") as f:
        f.write(username)


def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False