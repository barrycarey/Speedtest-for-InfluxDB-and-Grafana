from dataclasses import dataclass


@dataclass
class GraphiteConfig:
    name: str
    url: str
    prefix: str
    port: int