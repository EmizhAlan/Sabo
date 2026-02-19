from dataclasses import dataclass, field
from typing import List
from .component import Component

@dataclass 
class Page:
    id: str
    name: str
    components: List[Component] = field(default_factory=list)
    
    def add_component(self, component: Component):
        self.components.append(component)