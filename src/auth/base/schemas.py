from pydantic import BaseModel, Field, SecretStr, field_validator, EmailStr

class LoginSchema(BaseModel):
    identifier: str = Field(..., min_length=3, max_length=50)
    password: SecretStr

    class Config:
        str_strip_whitespace = True

class RegisterSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50)
    last_name: str = Field(..., min_length=3, max_length=50)
    email: EmailStr = Field(..., min_length=3, max_length=50)
    password: SecretStr
    password_repeat: SecretStr

    class Config:
        str_strip_whitespace = True

    @field_validator("password_repeat", mode="before")
    def password_match(cls, v, values, **kwargs):
        print(v)
        print(values.data)
        if "password" in values.data and v != values.data["password"].get_secret_value():
            raise ValueError("passwords don't match")
        return v
