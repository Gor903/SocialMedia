from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    password: str
    email: EmailStr


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
