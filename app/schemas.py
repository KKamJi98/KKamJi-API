from pydantic import BaseModel

# TODO 스키마 user, post 파일 나눠야 함


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserUpdatePassword(BaseModel):
    password: str


class PostBase(BaseModel):
    title: str
    content: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
