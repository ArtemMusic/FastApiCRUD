from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBaseIn(BaseModel):
    name: str
    emails: List[EmailStr]
    password: str
    optional: str | None = None


class UserBaseOut(BaseModel):
    id: int
    name: str
    emails: List[EmailStr]
    optional: str | None = None


class User(UserBaseIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBaseOut):
    pass


class UserIn(UserBaseIn):
    pass
