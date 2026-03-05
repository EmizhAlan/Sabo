from dataclasses import dataclass, field
from typing import Dict, List
from pathlib import Path


@dataclass
class Component:
    """
    Базовая единица интерфейса Sabo.
    """

    # --- идентификация ---
    id: str
    name: str

    # --- путь к компоненту ---
    path: Path

    # --- содержимое ---
    template: str = ""
    css: str = ""
    js: str = ""

    # --- props ---
    props: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):

        if not self.id:
            raise ValueError("Component must have an id")

        if not self.name:
            raise ValueError("Component must have a name")

    @classmethod
    def load(cls, component_path: Path):
        """
        Загружает компонент из директории
        """

        template_path = component_path / "template.html"
        html = template_path.read_text(encoding="utf-8") if template_path.exists() else ""

        css_path = component_path / "style.css"
        css = css_path.read_text(encoding="utf-8") if css_path.exists() else ""

        js_path = component_path / "script.js"
        js = js_path.read_text(encoding="utf-8") if js_path.exists() else ""

        return cls(
            id=component_path.name,
            name=component_path.name,
            path=component_path,
            template=html,
            css=css,
            js=js
        )

    def __repr__(self):
        return f"<Component id={self.id}, name={self.name}>"

    # --- для builder ---
    def get_css_paths(self):
        css_file = self.path / "style.css"
        return [css_file] if css_file.exists() else []

    def get_js_paths(self):
        js_file = self.path / "script.js"
        return [js_file] if js_file.exists() else []