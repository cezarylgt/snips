from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List


@dataclass
class Snippet:
    id: str
    snippet: str
    desc: str
    tags: List[str] = None
    alias: str = None
    created_at: datetime = None
    updated_at: datetime = None

    def dict(self):
        return asdict(self)
