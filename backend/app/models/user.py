from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: int | None = None  # 可选字段

class UserResponse(UserCreate):
    id: int  # 响应时包含ID
    class Config:
        from_attributes = True  # Pydantic 2.0+ 需显式声明