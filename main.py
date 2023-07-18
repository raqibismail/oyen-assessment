from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
import sqlite3
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8081", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = "sadfsadfsdafsdafasfsadf"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBasic()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        login_date TEXT,
        access_token TEXT
    )
''')
conn.commit()


@app.on_event("shutdown")
def shutdown_event():
    conn.close()


@app.post("/login/token")
async def login_for_access_token(user: dict):
    username = user.get('username')
    password = user.get('password')

    retrieved_user_from_users_table = find_user_by_username(username, password)

    if retrieved_user_from_users_table is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    else:
        token_data = {
            "sub": retrieved_user_from_users_table,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        response = {"access_token": access_token, "token_type": "bearer"}

        login_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO login_history (username, login_date, access_token) VALUES (?, ?, ?)",
                    (username, login_date, access_token))
        conn.commit()

        return response


def find_user_by_username(username, password):
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    print(user)

    if user and user[2] == password:
        return user

    return None
