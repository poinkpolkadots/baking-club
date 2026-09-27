from dotenv import load_dotenv
import os
import psycopg2
from flask_bcrypt import Bcrypt
from flask import Flask

load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
    )

def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT (id, username, name, password_hash, isadmin, isreadonly, email) FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def create_user(username, name, password_hash, email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, name, password_hash, email) VALUES (%s, %s, %s, %s)", (username, name, password_hash, email))
    conn.commit()
    cur.close()
    conn.close()

def get_user_from_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT (id, username, name, password_hash, isadmin, isreadonly, email) FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def log_attendance(user_id, date, brought_baked_goods, baked_good):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (member_id, meeting_date, brought_baked_good, baked_good) VALUES (%s, %s, %s, %s)", (user_id, date, brought_baked_goods, baked_good))
    conn.commit()
    cur.close()
    conn.close()