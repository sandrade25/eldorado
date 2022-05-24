from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str
    schema_: str = Field(alias="schema")


class LoginSuccess(BaseModel):
    token: str
