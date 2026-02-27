from dataclasses import dataclass, field
from typing import List
from .component import Component

from pathlib import Path
import json

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
        
    """Метод позволяющий назевисимо загружать странцу"""       
    @classmethod
    def from_json(cls, path: Path) -> "Page":
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # Получаем id, name и компоненты
        page_id = data.get("id", data.get("name", "page"))
        page_name = data.get("name", "Page")
        components_data = data.get("components", [])
        
        # Преобразуем каждый компонент в объект Component, если нужно
        # Пока можно оставить пустым или загружать через ComponentLoader
        components_list = [] # заполнение позже через loader
        
                
        return cls(
            id=page_id,
            name=page_name,
            components=components_list
        )