from dotenv import load_dotenv
import os
import psycopg2
from flask_bcrypt import Bcrypt
from flask import Flask, session

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
    cur.execute("SELECT id, username, password_hash, isadmin, isreadonly, email FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def get_user_from_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password_hash, isadmin, isreadonly, email FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user
