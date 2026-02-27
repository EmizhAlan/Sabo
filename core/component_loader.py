"""
Модуль загрузчика компонентов.

Отвечает за:
- Cканирование директории components
- Чтение meta.json
- Чтение template.html
- Чтение необязательных css/ks файлов
- Создание объектов Component
"""

import os
import json
from pathlib import Path
from models.component import Component
from core.component_definition import ComponentDefinition

class ComponentLoader:
    """
    Загружает и управляет компонентами.
    """
    
    def __init__(self, components_path: str = "components"):
        """
        :para components_path: Путь к директории с компонентами
        """
        self.components_path = Path(components_path)
        self.components = {}
        
    def load_all(self):
        """
        Сканирует директорию компонентов и загружает все компоненты.
        """
        if not self.components_path.exists():
            raise FileNotFoundError(f"Directory {self.components_path} not found")
        
        for item in self.components_path.iterdir():
            if item.is_dir():
                component = self._load_component(item)
                self.components[component.name] = component
                
        return self.components
    
    def _load_component(self, component_dir: Path) -> Component:
        """
        Загружает один компонент из его директории.
        
        :param component_dir: Путь к папке компонента
        :return: Экземпляр Component
        """
        
        name = component_dir.name
        component_id=name
        
        # --- Чтение meta.json ---
        meta_path = component_dir / "meta.json"
        if not meta_path.exists():
            raise FileNotFoundError(
                f"meta.json не нфйден в компоненте '{name}'"
            )
            
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        props = meta.get("props", {})
        
        # --- Чтение template.html ---
        template_path = component_dir / "template.html"
        if not template_path.exists():
            raise FileNotFoundError(
                f"template.html не найден в компоненте '{name}'"
            )
            
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
            
        # --- Чтение необязательного CSS ---
        css_path = component_dir / "style.css"
        css = ""
        if css_path.exists():
            with open(css_path, "r", encoding="utf-8") as f:
                css = f.read()
                
        # --- Работа optin js
        js_path = component_dir / "script.js"
        js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
                
        return Component(
            id=component_id,
            name=name,
            template=template,
            css=css,
            js=js,
            props=props
        )
        
    def list_components(self):
        """
        Возвращает список загруженных компонентов.
        """
        return list(self.components.keys())