from pydantic_settings import BaseSettings
from pydantic import Field


class Config(BaseSettings):
    sql_uri: str = Field(default="postgresql+asyncpg://postgres:cyc@192.168.1.40:5432/boilerplate", alias="DEF_SQL_URI")
    
    JWT_SECRET_KEY: str = Field(default="TvXrIhF1Abs5g7xTvXrIhF1Abs5g7xPzVsq46hpsPQuiX7PzVsq46hpsPQuiX7", alias="DEF_JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    GOOGLE_CLIENT_ID: str = Field(default="GOOGLE_CLIENT_ID", alias="DEF_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(default="GOOGLE_CLIENT_SECRET", alias="DEF_GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI: str = Field(default="GOOGLE_REDIRECT_URI", alias="DEF_GOOGLE_REDIRECT_URI")



config: Config = Config()
