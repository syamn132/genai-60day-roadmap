
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    SecretStr,
)


class UserRegister(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-z0-9_]+$",
    )

    password: SecretStr = Field(
        min_length=12,
        max_length=128,
    )


class UserPublic(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    username: str
    is_active: bool


class UserLogin(BaseModel):

    username: str
    password: SecretStr


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = "bearer"
