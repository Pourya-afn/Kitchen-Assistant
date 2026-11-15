import sqlite3
import os

def get_db_path(username):
    """ساخت مسیر فایل دیتابیس اختصاصی برای هر کاربر"""
    return f"inventory_{username}.db"

def init_db(username):
    """ساخت جدول یخچال برای کاربر خاص در صورت عدم وجود"""
    db_path = get_db_path(username)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inventory (
                    ing_id INTEGER PRIMARY KEY,
                    quantity REAL NOT NULL
                )
            """)
            conn.commit()
    except sqlite3.Error as e:
        print(f"خطا در ایجاد پایگاه داده محلی برای {username}: {e}")

def add_item(username, ing_id, quantity):
    """اضافه کردن یا افزایش مقدار ماده اولیه در یخچال کاربر"""
    db_path = get_db_path(username)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO inventory (ing_id, quantity) 
                VALUES (?, ?)
                ON CONFLICT(ing_id) DO UPDATE SET quantity = quantity + ?
            """, (ing_id, quantity, quantity))
            conn.commit()
    except sqlite3.Error as e:
        print(f"خطا در ثبت اطلاعات در دیتابیس محلی: {e}")

def get_inventory(username):
    """گرفتن لیست تمام مواد داخل یخچال کاربر"""
    db_path = get_db_path(username)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ing_id, quantity FROM inventory")
            rows = cursor.fetchall()
            return rows
    except sqlite3.Error as e:
        print(f"خطا در خواندن اطلاعات از دیتابیس محلی: {e}")
        return []

def delete_local_db(username):
    """حذف فایل دیتابیس محلی کاربر (بعد از سینک موفق)"""
    db_path = get_db_path(username)
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
        except OSError as e:
            print(f"خطا در حذف دیتابیس محلی {username}: {e}")