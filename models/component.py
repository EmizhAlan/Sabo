from dataclasses import dataclass, field
from typing import Dict, List

@dataclass 
class Component:
    """
        Базовая единица интерфейса.
        Содержит шаблон, стили, скрипты и свойства.
    """
    id: str
    name: str
    template_path: str
    styles: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    props: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            raise ValueError("Component must have an id")