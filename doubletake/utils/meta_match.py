from dataclasses import dataclass, field
from typing import Set


@dataclass
class MetaMatch:
    pattern: str = ""
    replacement: str = ""
    breadcrumbs: Set[str] = field(default_factory=set)
    value: str = ""
