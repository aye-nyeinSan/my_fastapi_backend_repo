
from pydantic_settings import BaseSettings


class AWS_Settings(BaseSettings):
    AWS_REGION: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_BUCKET_NAME: str

    class Config:
        env_file = ".env"


settings = AWS_Settings()
