from models.project import Project
from core.component_loader import ComponentLoader

class SiteBuilder:
    """
    Builder проекта.
    Пока выводит структуру проекта, без генерации HTML.
    """
    def __init__(self, project: Project):
        self.project = project
        self.loader = ComponentLoader("components")
        self.component_registry = self.loader.load_all()
        
    def build(self):
        print(f"Building project: {self.project.name}")
        print(f"Pages count: {len(self.project.pages)}")
        
        for page in self.project.pages:
            print(f" - Page: {page.name}")
            print(f"   Components: {len(page.components)}")
            
        print(f"Available components: {len(self.component_registry)}")
        for name in self.component_registry:
            print(f" - {name}")
            
        print("Build complete (no rendering yet).")