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
            "name TEXT,"
            "password_hash VARCHAR(128) NOT NULL,"
            "isadmin BOOLEAN DEFAULT FALSE,"
            "isreadonly BOOLEAN DEFAULT TRUE,"
            "email TEXT,"
            "isingoodstanding BOOLEAN DEFAULT TRUE NOT NULL,"
            # add constraint for name so that if user is admin it has to be blank but not otherwise
            "CONSTRAINT name_ck "
            "   CHECK ((isadmin = TRUE AND (name IS NULL OR name = '')) OR (isadmin = FALSE AND (name IS NOT NULL AND name <> ''))),"
            "CONSTRAINT perm_ck "
            "   CHECK ((isadmin = TRUE AND isreadonly = TRUE ) = FALSE)"
            ");")

cur.execute("DROP TABLE IF EXISTS attendance CASCADE;")
cur.execute("CREATE TABLE attendance ("
            "member_id INTEGER REFERENCES users(id) ON DELETE CASCADE,"
            "meeting_date DATE NOT NULL,"
            "date_submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,"
            "brought_baked_good BOOLEAN DEFAULT FALSE NOT NULL,"
            "baked_good TEXT"
            ")")

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