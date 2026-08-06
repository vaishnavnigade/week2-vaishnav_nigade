from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name:str
    email: EmailStr
    password: str
    mobile:str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    
    email: EmailStr
    message: str


# used when reading a user from DB (never expose the password)
class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True