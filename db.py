import mysql.connector as sql
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return sql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 3306)),
        charset="utf8mb4",
    )


def add_user(info):
    try:
        with get_connection() as mydb:
            with mydb.cursor() as mycursor:
                placeholders = ", ".join(["%s"] * len(info))
                sql_str = f"INSERT INTO users (username, password) VALUES ({placeholders})"
                mycursor.execute(sql_str, info)
                mydb.commit()
    except sql.Error as err:
        raise err


def check_user(info):
    try:
        with get_connection() as mydb:
            with mydb.cursor() as mycursor:
                sql_str = "SELECT * FROM users WHERE username = %s AND password = %s"
                mycursor.execute(sql_str, info)
                user = mycursor.fetchone()
                return user is not None
    except sql.Error as err:
        raise err




def sync_inventory_to_mysql(username, local_items):
    """
    سینک کردن دیتابیس محلی با MySQL به روش ساده و امن (Upsert)
    local_items شامل لیستی از توپل‌هاست: [(ing_id, quantity), ...]
    """
    if not local_items:
        return True
    try:
        with get_connection() as mydb:
            with mydb.cursor() as mycursor:
                # فرض بر این است که جدولی به نام central_inventory با ستون‌های (username, ing_id, quantity) داریم
                sql_str = """
                    INSERT INTO central_inventory (username, ing_id, quantity)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE quantity = VALUES(quantity)
                """
                # اضافه کردن username به هر رکورد برای تفکیک در سرور مرکزی
                data_to_insert = [(username, item[0], item[1]) for item in local_items]

                mycursor.executemany(sql_str, data_to_insert)
                mydb.commit()
                return True
    except sql.Error as err:
        print(f"erorr: {err}")
        return False


