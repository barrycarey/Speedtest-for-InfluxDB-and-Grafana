from pydantic import BaseModel


class StorageConfig(BaseModel):
    name: str
    url: str