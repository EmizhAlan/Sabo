from models.project import Project

class SiteBuilder:
    """
    Builder проекта.
    Пока выводит структуру проекта, без генерации HTML.
    """
    def __init__(self, project: Project):
        self.project = project
        
    def build(self):
        print(f"Building project: {self.project.name}")
        print(f"Pages count: {len(self.project.pages)}")
        
        for page in self.project.pages:
            print(f" - Page: {page.name}")
            print(f"   Components: {len(page.components)}")
            
        print("Build complete (no rendering yet).")