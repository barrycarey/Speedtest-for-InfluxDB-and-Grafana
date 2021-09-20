from dataclasses import dataclass


@dataclass
class InfluxV2Config:
    name: str
    url: str
    token: str
    org: str
    bucket: str
    ssl: bool