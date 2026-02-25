from dataclasses import dataclass, field
from typing import Set, List

@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)
        
@dataclass
class User:
    username: str
    enabled: bool = True
    roles: List[str] = field(default_factory=list)

