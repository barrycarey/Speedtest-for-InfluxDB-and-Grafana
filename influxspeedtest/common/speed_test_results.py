from dataclasses import dataclass
from typing import Text


@dataclass
class SpeedTestResult:
    jitter: float
    latency: float
    jitter: int
    download: int
    upload: int
    server_id: int
    server_name: Text
    server_country: Text
    server_location: Text
    packetloss: int = None