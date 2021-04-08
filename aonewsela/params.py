from typing import List
from dataclasses import dataclass, field


@dataclass
class NewselaParams:
    min_utterance_length: int = field(default=1)
    punctuation: bool = field(default=True)

