from typing import Union
from functools import lru_cache
from pydantic import BaseModel, BaseSettings


class Query(BaseModel):
    phrase: Union[str, None]
    image: Union[str, None]
    page: Union[int, None] = 0
    rowsPerPage: Union[int, None] = 10


class Settings(BaseSettings):
    es_host: str
    es_port: int
    es_index: str = "flickr-images"
    model_path: str = "../model/mlflow_clip_model"
    img_url_prefix: str = "https://farm66.staticflickr.com/"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
