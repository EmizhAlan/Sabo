from dataclasses import dataclass, field
from typing import List, Dict
from .page import Page

@dataclass
class Project:
    """Здесь зранятся наборы страниц и глобальные переменные проекта."""
    name: str
    pages: List[Page] = field(default_factory=list)
    global_variables: Dict[str, str] = field(default_factory=dict)
    
    def add_page(self, page: Page):
        """Добавление страницы в проект"""
        self.pages.append(page)