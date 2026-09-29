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
    cur.execute("SELECT id, username, name, password_hash, isadmin, isreadonly, email FROM users WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def get_user_from_username(username):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, name, password_hash, isadmin, isreadonly, email FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user

def create_user(username, name, password_hash, email):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, name, password_hash, email) VALUES (%s, %s, %s, %s)", (username, name, password_hash, email))
    conn.commit()
    cur.close()
    conn.close()

def log_attendance(user_id, date, brought_baked_goods, baked_good):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO attendance (member_id, meeting_date, brought_baked_good, baked_good) VALUES (%s, %s, %s, %s)", (user_id, date, brought_baked_goods, baked_good))
    conn.commit()
    cur.close()
    conn.close()

def generate_all_user_status():
    conn = get_db_connection()
    cur = conn.cursor()
    # want to get name, meetings attended, and number of things they've brought
    # maybe we can do something where we can see the number of meetings since they've brought something, but on the user page view, it will be easy to see for ourselves
    # in order to get last thing, we must join with attendance and get a count of meetings where brought_baked_goods is true
    cur.execute(
        "SELECT users.id, "
        "users.name, "
        "COUNT(attendance.member_id) AS meetings_attended, "
        "SUM(CASE WHEN attendance.brought_baked_good = TRUE THEN 1 ELSE 0 END) AS things_brought "
        "FROM users "
        "LEFT JOIN attendance ON users.id = attendance.member_id "
        "GROUP BY users.id"
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_individual_data(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT users.id, "
        "users.name, "
        "users.username, users.email, "
        "COUNT(attendance.member_id) AS meetings_attended, "
        "SUM(CASE WHEN attendance.brought_baked_good = TRUE THEN 1 ELSE 0 END) AS things_brought "
        "FROM users "
        "LEFT JOIN attendance ON users.id = attendance.member_id "
        "WHERE users.id = %s "
        "GROUP BY users.id",
        (user_id,)
    )
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def get_individual_meetings(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT meeting_date, date_submitted, brought_baked_good, baked_good "
        "FROM attendance "
        "WHERE member_id = %s "
        "ORDER BY meeting_date DESC",
        (user_id,)
    )
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data