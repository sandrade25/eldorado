from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str
    db_schema: str


class LoginSuccess(BaseModel):
    token: str
