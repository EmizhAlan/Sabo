from sabo.models.project import Project
from sabo.core.component_loader import ComponentLoader
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
        
        # Исправил названия переменных, которые хранят содержимое
        self.collected_css_content = set()
        self.collected_js_content = set()
        
        # Директория сборки
        self.dist_path = Path("dist")
        
    def build(self):
        
        dist_path = Path("dist")
        dist_assets = dist_path / "assets"
        dist_assets.mkdir(parents=True, exist_ok=True)
        
        print(f"Building project: {self.project.name}")
        print(f"Pages count: {len(self.project.pages)}")
        
        # --- очистка dist ---
        if self.dist_path.exists():
            shutil.rmtree(self.dist_path)
            
        self.dist_path.mkdir()
        
        # сборка ассетов будущего сайта
        self._collect_project_assets()
        
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
                    
                # собираем пути к файлам компонентов
                self._collect_component_assets(component)
                    
            # --- генерация html страницы ---
            self._write_html(page.name, html_parts)
            
        # --- после сборки всех страниц ---
        all_css = list(self.collected_css_content) + global_css_parts
        all_js = list(self.collected_js_content) + global_js_parts
        
        self._write_bundles(dist_assets, all_css, all_js)
        self._copy_additional_assets()
            
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
        
    # --- новый метод для записи bundle ---
    # В методе _write_bundles (примерно строка 123)
    def _write_bundles(self, dist_assets, all_css, all_js):
        # Создаем директорию assets, если её нет
        assets_dir = dist_assets
        assets_dir.mkdir(parents=True, exist_ok=True)
    
        # Запись CSS бандла
        if all_css:
            css_bundle = "\n".join(all_css)
            css_path = assets_dir / 'bundle.css'
            css_path.write_text(css_bundle, encoding="utf-8")
            print(f"✓ CSS bundle written: {css_path}")
    
        # Запись JS бандла (аналогично)
        if all_js:
            js_bundle = "\n".join(all_js)
            js_path = assets_dir / 'bundle.js'
            js_path.write_text(js_bundle, encoding="utf-8")
            print(f"✓ JS bundle written: {js_path}")     
            
    # метод для сбора ассетов компонентов
    def _collect_component_assets(self, component):
        """Собирает содержимое CSS/JS файлов компонента"""

        # CSS
        for css_file in component.get_css_paths():
            if css_file.exists():
                content = css_file.read_text(encoding="utf-8")
                self.collected_css_content.add(content)

        # JS
        for js_file in component.get_js_paths():
            if js_file.exists():
                content = js_file.read_text(encoding="utf-8")
                self.collected_js_content.add(content)
                
    # новый метод для сбора ассетов из project/assets
    def _collect_project_assets(self):
        """Собирает все CSS/JS файлы из папки project/assets"""
        project_assets = Path("project/assets")
        
        if project_assets.exists():
            print("Collecting assets from project/assets...")
            
            # Собираем все CSS файлы
            for css_file in project_assets.glob("*.css"):
                content = css_file.read_text(encoding="utf-8")
                self.collected_css_content.add(content)
                print(f"   Found CSS: {css_file.name}")
            
            # Собираем все JS файлы
            for js_file in project_assets.glob("*.js"):
                content = js_file.read_text(encoding="utf-8")
                self.collected_js_content.add(content)
                print(f"   Found JS: {js_file.name}")
    
    # переименован и исправлен метод копирования
    def _copy_additional_assets(self):
        """Копирует остальные ассеты (изображения, шрифты и т.д.)"""
        source = Path("project/assets")
        target = self.dist_path / "assets"
        
        if source.exists():
            # Копируем только не-CSS и не-JS файлы
            for item in source.iterdir():
                if item.suffix not in ['.css', '.js']:
                    if item.is_file():
                        shutil.copy2(item, target / item.name)
                    elif item.is_dir():
                        # ИСПРАВЛЕНО: copythree -> copytree
                        shutil.copytree(item, target / item.name, dirs_exist_ok=True)
                    
    # --- Возвращает загруженный компонент по имени.
    def get(self, name: str):
        return self.component_registry.get(name)
            
    # --- Инъекция в HTML ---
    def _inject_bundles(self, html: str) -> str:
        css_link = '<link rel="stylesheet" href="assets/bundle.css">'
        js_script = '<script src="assets/bundle.js"></script>'
        
        html = html.replace("</head>", f"    {css_link}\n</head>")
        html = html.replace("</body>", f"    {js_script}\n</body>")
        
        return html