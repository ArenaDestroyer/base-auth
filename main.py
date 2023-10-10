from fastapi import FastAPI, HTTPException, Depends, Cookie, Response
from models import User, LoginUser
import hashlib
import uuid

app = FastAPI()

fake_database = {}


def get_user(username):
    if username in fake_database:
        return fake_database[username]
    return None


def verify_session_token(session_token: str = Cookie(None), user=Depends(get_user)):
    if not session_token or session_token != user["session_token"]:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def get_hashed_value(password):
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(user, password):
    return user["password"] == get_hashed_value(password)


@app.post("/register/")
async def register_user(user: User):
    if get_user(user.nickname):
        raise HTTPException(status_code=400, detail="Username already exist in database")
    hashed_password = get_hashed_value(user.password)
    fake_database[user.nickname] = {"name": user.name, "username": user.nickname, "password": hashed_password}
    return "Registration was successful, all 200 :D"


@app.post("/login")
async def login_user(user: LoginUser, response: Response):
    client = get_user(user.nickname)
    if not client or not check_password(client, user.password):
        raise HTTPException(status_code=400, detail="Invalid data")

    session_token = str(uuid.uuid4())
    fake_database[user.nickname]["session_token"] = session_token

    response.set_cookie(key="session_token", value=session_token, secure=True)

    return {"message": "Successfully logged"}


@app.post("/show_user")
async def get_user_data(user: User):
    return user


@app.get("/get_user/{username}")
async def get_user_data(username, user=Depends(verify_session_token)):
    return user