import sys
import json
from models.project import Project
from models.page import Page
from models.component import Component
from builder.site_builder import SiteBuilder


def load_project_from_json(path: str) -> Project:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    project = Project(name=data["name"])
    
    for page_data in data.get("pages", []):
        page = Page(id=page_data["id"], name=page_data["name"])
        
        for comp_data in page_data.get("components", []):
            component = Component(
                id=comp_data["id"],
                name=comp_data["name"],
                template_path=comp_data["template_path"]
            )
            page.add_component(component)
            
        project.add_page(page)
        
    return project

def main():
    if len(sys.argv) < 3:
        print("Usege: python sabo.py build peth_to_project.json")
        return
    
    command = sys.argv[1]
    
    if command == "build":
        project_path = sys.argv[2]
        Project = load_project_from_json(project_path)
        builder = SiteBuilder(Project)
        builder.build()
    else:
        print("Unknown command")
        
if __name__ == "__main__":
    main()
