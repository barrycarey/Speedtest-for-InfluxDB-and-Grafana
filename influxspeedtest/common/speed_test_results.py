from dataclasses import dataclass
from typing import Text


@dataclass
class SpeedTestResult:
    latency: float
    jitter: int
    download: int
    upload: int
    server_id: int
    server_name: Text
    server_country: Text
    server_location: Text
    packetloss: int = None

    def to_dict(self):
        return {
            'jitter': self.jitter,
            'latency': self.latency,
            'download': self.download,
            'upload': self.upload,
            'server_id': self.server_id,
        }