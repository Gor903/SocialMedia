from typing import Self

from pydantic import BaseModel, EmailStr, model_validator


class CreateUserRequest(BaseModel):
    password: str
    password_repeat: str
    email: EmailStr

    @model_validator(mode="before")
    def check_passwords_match(self) -> Self:
        if self["password"] != self["password_repeat"]:
            raise ValueError("Passwords do not match!!")
        return self


class PasswordResetForm(BaseModel):
    otp: int
    new_password: str


class ChangePassword(BaseModel):
    current_password: str
    new_password: str


class Token(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str
