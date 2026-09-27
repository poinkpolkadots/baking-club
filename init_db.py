from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

from model import get_db_connection

app = Flask(__name__)
bcrypt = Bcrypt(app)

load_dotenv()

conn = get_db_connection()
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users CASCADE;")
cur.execute("CREATE TABLE users ("
            "id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "username VARCHAR(50) UNIQUE NOT NULL,"
            "password_hash VARCHAR(128) NOT NULL,"
            "isadmin BOOLEAN DEFAULT FALSE,"
            "isreadonly BOOLEAN DEFAULT TRUE,"
            "email TEXT,"
            "CONSTRAINT perm_ck "
            "   CHECK ((isadmin = TRUE AND isreadonly = TRUE ) = FALSE)"
            ");")

cur.execute("DROP TABLE IF EXISTS members CASCADE;")
cur.execute("CREATE TABLE members ("
            "id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,"
            "name TEXT NOT NULL,"
            "isingoodstanding BOOLEAN DEFAULT TRUE NOT NULL)")

cur.execute("DROP TABLE IF EXISTS attendance CASCADE;")
cur.execute("CREATE TABLE attendance ("
            "member_id INTEGER REFERENCES members(id) ON DELETE CASCADE,"
            "date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            "broughtbakedgood BOOLEAN DEFAULT FALSE NOT NULL)")

username = "admin"
password = "09jJ2f)H)UOX"
isadmin = "true"
isreadonly = "false"
email = ""

hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

cur.execute("DELETE FROM USERS WHERE username = %s;", (username,))
cur.execute("INSERT INTO users (username, password_hash, isadmin, isreadonly, email)"
            "VALUES (%s, %s, %s, %s, %s)",
            (username, hashed_password, isadmin, isreadonly, email,))

conn.commit()
conn.close()
cur.close()