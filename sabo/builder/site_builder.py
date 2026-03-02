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
        
        self.collected_css = set()
        self.collected_js = set()
        
        # Директория сборки
        self.dist_path = Path("dist")
        
    def build(self):
        
        dist_path = Path("dist")
        dist_assets = dist_path / "assets"
        dist_assets.mkdir(parents=True, exist_ok=True)
        
        self.component_loader = ComponentLoader("components")
        self.component_loader.load_all()
        
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
            self._collect_assets(page)
            self._write_html(page.name, html_parts)
            
        # --- после сборки всех страниц ---
        self._build_bundles(dist_assets)
        self._copy_project_assets()
        self._write_css_bundle(global_css_parts)
        self._write_js_bundle(global_js_parts)
            
        print("Build complete.")
        
    """--- методы сборки ---"""
        
    # --- Данная функция формирует HTML страницы и сохраняет их в dist ---
    def _write_html(self, page_name, html_parts):
        # Собираем базовый каркас страницы
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
            
        html = self._inject_bundles(html_content)
        html_path = self.dist_path / f"{page_name}.html"
        html_path.write_text(html, encoding="utf-8")
            
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
        
    # --- Метод сбора страниц ---
    def _collect_assets(self, page):
        for comp_data in page.components:
            component = self.component_loader.get(comp_data["name"])
            
            for css_path in component.get_css_paths():
                self.collected_css.add(css_path)
                
            for js_path in component.get_js_paths():
                self. collected_js.add(js_path)
                
    # --- Возвращает загруженный компонент по имени.
    def get(self, name: str):
        return self.components.get(name)
                
    # --- Генерация bundle файлов ---
    def _build_bundles(self, dist_assets: Path):
        """
        Собирает boundle.css и boundle.js в папке dist/assets
        """
        # Гарантируем, что папка существует
        dist_assets.mkdir(parents=True, exist_ok=True)

        bundle_css = dist_assets / "bundle.css"
        bundle_js = dist_assets / "bundle.js"

        # Сборка CSS
        with bundle_css.open("w", encoding="utf-8") as css_out:
            for css_content in self.collected_css:
                css_out.write(css_content)
                css_out.write("\n")

        # Сборка JS
        with bundle_js.open("w", encoding="utf-8") as js_out:
            for js_content in self.collected_js:
                js_out.write(js_content)
                js_out.write("\n")
                    
    # --- Особая технология копирования ---
    def _copy_project_assets(self):
        source = Path("project/assets")
        target = Path("dist/assets")
        
        if source.exists():
            shutil.copythree(source, target, dirs_exist_ok=True)
            
    # --- Инъекция в HTML ---
    def _inject_bundles(self, html: str) -> str:
        css_link = '<link rel="stylesheet" href="assets/bundle.css">'
        js_script = '<script src="assets/bundle.js"></script>'
        
        html = html.replace("</head>", f"    {css_link}\n</head>")
        html = html.replace("</body>", f"    {js_script}\n</body>")
        
        return html