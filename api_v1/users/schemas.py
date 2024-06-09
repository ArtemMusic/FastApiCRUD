from pydantic import BaseModel, ConfigDict


class UserBaseIn(BaseModel):
    name: str
    password: str
    optional: str | None = None


class UserBaseOut(BaseModel):
    id: int
    name: str
    optional: str | None = None


class User(UserBaseIn):
    id: int
    model_config = ConfigDict(from_attributes=True)


class UserOut(UserBaseOut):
    pass


class UserCreateIn(UserBaseIn):
    pass


class UserCreateOut(UserBaseOut):
    pass


class UserUpdateIn(UserBaseIn):
    pass


class UserUpdateOut(UserBaseOut):
    pass


class UserDeleteOut(UserBaseOut):
    pass
