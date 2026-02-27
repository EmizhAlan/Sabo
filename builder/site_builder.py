from models.project import Project
from core.component_loader import ComponentLoader
from pathlib import Path
import shutil

class SiteBuilder:
    """
    Builder проекта.
    Теперь выполняет полноценную сборку страниц:
    - объединяет HTML компонентов
    - собирает общий CSS bundle
    - собирает общий JS bundle
    """
    def __init__(self, project: Project):
        self.project = project
        self.loader = ComponentLoader("components")
        self.component_registry = self.loader.load_all()
        
        # Директория сборки
        self.dist_path = Path("dist")
        
    def build(self):
        print(f"Building project: {self.project.name}")
        print(f"Pages count: {len(self.project.pages)}")
        
        # --- очистка dist ---
        if self.dist_path.exists():
            shutil.rmtree(self.dist_path)
            
        self.dist_path.mkdir()
        
        # глобальные буферы для bundle.css и  bundle.js
        global_css_parts = []
        global_js_parts = []
        
        for page in self.project.pages:
            print(f" - Page: {page.name}")
            print(f"   Components: {len(page.components)}")
            
            html_parts = []
            
            # --- последовательная сборка компонентов ---
            for component_data in page.components:
                
                component_name = component_data["name"]
                props = component_data.get("props", {})
                
                if component_name not in self.component_registry:
                    raise ValueError(
                        f"Component '{component_name}' not found in registry."
                    )
                    
                component = self.component_registry[component_name]
                
                # добавляем HTML
                html_parts.append(component.template)
                
                # добавляем CSS в глобальный bundle
                if component.css:
                    global_css_parts.append(component.css)
                    
                # добавляем JS в глобальный bundle
                if component.js:
                    global_js_parts.append(component.js)
                    
            # --- генерация html страницы ---
            self._write_html(page.name, html_parts)
            
        # --- после сборки всех страниц ---
        self._write_css_bundle(global_css_parts)
        self._write_js_bundle(global_js_parts)
            
        print("Build complete.")
        
    """--- методы сборки ---"""
        
    # --- HTML ---
    def _write_html(self, page_name, html_parts):
        html_content = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{page_name}</title>
                <link rel="stylesheet" href="bundle.css">
            </head>
            <body>
            {''.join(html_parts)}
            <script src="bundle.js"></script>
            </body>
            </html>
            """
            
        html_path = self.dist_path / f"{page_name}.html"
        html_path.write_text(html_content, encoding="utf-8")
            
    # --- CSS ---
    def _write_css_bundle(self, css_parts):
        css_bundle = "\n\n".join(css_parts)
        css_path = self.dist_path / "bundle.css"
        css_path.write_text(css_bundle, encoding="utf-8")
        
    # --- JS ---
    def _write_js_bundle(self, js_parts):
        js_bundle = "\n\n".join(js_parts)
        js_path = self.dist_path / "bundle.js"
        js_path.write_text(js_bundle, encoding="utf-8")        