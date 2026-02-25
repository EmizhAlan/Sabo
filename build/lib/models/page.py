from dataclasses import dataclass, field
from typing import List
from .component import Component

@dataclass 
class Page:
    """Страница проекта, состоит из компонентов которые
    пользователь сможет создавать, удалять, копировать, перемещать"""
    id: str
    name: str
    components: List[Component] = field(default_factory=list)
    
    def add_component(self, component: Component):
        """Добавление компонента на страницу"""
        self.components.append(component)