from pydantic import BaseModel, Field


class LoginCredentials(BaseModel):
    email: str
    password: str
    db_schema_: str = Field(alias="db_schema")


class LoginSuccess(BaseModel):
    token: str
