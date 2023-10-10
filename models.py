from pydantic import BaseModel


class User(BaseModel):
    name: str
    nickname: str
    password: str

class LoginUser(BaseModel):
    nickname: str
    password: str