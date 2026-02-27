from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass 
class Component:
    """
        Базовая единица интерфейса Sabo.
        Содержит шаблон, стили, скрипты и свойства.
        Работает в двух режимах:
        1. Path-based (через пути к файлам)
        2. Loaded-content (через уже загруженное содержимое)
    """
    
    # --- Идентификация ---
    id: str
    name: str
    
    # --- Path-based режим (старый) ---
    template_path: Optional[str] = None
    styles: List[str] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    
    
    # --- Loaded-content режим (новый loader) ---
    template: Optional[str] = None
    css: str = ""
    js: str = ""
    
    
    # --- Свойства ---
    props: Dict[str, str] = field(default_factory=dict)
    
    def __post_init__(self):
          
        if not self.id:
            raise ValueError("Component must have an id")
        
        if not self.name:
            raise ValueError("Component must have a name")
        
    @classmethod
    def load(cls, component_path: Path):
            
        html = (component_path / "template.html").read_text(encoding="utf-8")
            
        css_path = component_path / "style.css"
            
        css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""
            
        js_path = component_path / "script.js"
        js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""
            
        return cls(
            name=component_path.name,
            html=html,
            css=css,
            js=js
        )
        
    def __repr__(self):
        return f"<Component id={self.id}, name={self.name}>"