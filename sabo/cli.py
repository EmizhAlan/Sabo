import sys
import json
from pathlib import Path

from models.project import Project
from models.page import Page
from builder.site_builder import SiteBuilder
from core.component_loader import ComponentLoader


# Главный файл CLI Sabo. Обрабатывает команды пользователя и запускает сборку проекта.
def load_project_from_json(path: str) -> Project:
    """
    Загружает проект из JSON файла.
    формат JSON: имя проекта, страницы, компоненты каждой страницы.
    """
    
    path_obj = Path(path)
    
    if not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    with open(path_obj, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    project = Project(name=data["name"])
    
    for page_data in data.get("pages", []):
        page = Page(id=page_data["id"], name=page_data["name"])
        
        for comp_data in page_data.get("components", []):
            page.add_component({
            "name": comp_data["name"],
            "props": comp_data.get("props", {})
        })

            
        project.add_page(page)
        
    return project

def list_components():
    loader = ComponentLoader("components")
    loader.load_all()
    
    print("Available components:")
    for name in loader.list_components():
        print(f"- {name}")

def main():
    """Точка входа CLI Sabo"""
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python sabo.py build peth_to_project.json")
        print("  python sabo.py list")
        return
    
    command = sys.argv[1]
    
    if command == "build":
        if len(sys.argv) < 3:
            print("Error: project path required.")
            return
        
        project_path = sys.argv[2]
        project = load_project_from_json(project_path)
        builder = SiteBuilder(project)
        builder.build()
        
        print("Build completed.")
        
    elif command == "list":
        list_components()
    else:
        print(f"Unknown command: {command}")
        
if __name__ == "__main__":
    main()
