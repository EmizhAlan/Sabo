import re
from pathlib import Path

class TemplateRenderer:
    """
    Минимальный шаблонизатор Sabo.
    
    Поддерживает:
    - {{ variable}}
    - {% include component_name %}
    """
    
    VARIABLE_PATTERN = re.compile(r"\{\{\s*(\w+)\s*\}\}")
    INCLUDE_PATTERN = re.compile(r"\{\%\s*include\s+(\w+)\s*\%\}")
    
    def __init__(self, templates_dir: Path):
        """
        Инициализация шаблонизатора.
        
        :param templates_dir: Путь к директории с шаблонами.
        """
        self.templates_dir = templates_dir
        
    def render(self, template_name: str, context: dict) -> str:
        """
        Главный метод рендера.
        
        :param template_name: Имя шаблона.
        :param context: словарь переменных
        :return: готовый html
        """
        
        template_path = self.templates_dir / f"{template__name}.html"
        
        if not template_path.exists():
            raise FileNotFoundError(f"Template '{template_name}' not found")
        
        content = template_path.read_text(encoding="utf-8")
        
        # 1 Сначала раскрваем include
        content = self._process_includes(content, context)
        
        # 2 Затем подставляем переменные
        content = self._process_variables(content, context)
        
        return content
    
    # ---------------------------------------------------------------------
    # INTERNALS
    # ---------------------------------------------------------------------
    
    def _process_includes(self, content: str, context: dict) -> str:
        """
        Обрабатывает все include директивы рекурсивно
        """
        
        def replace_include(match):
            include_template = match.group(1)
            return self.render(included_template, context)
        
        # Пока есть include - раскрываем
        while self.INCLUDE_PATTERN.search(content):
            content = self.INCLUDE_PATTERN.sub(replace_include, content)
        
        return content
    
    def _process_variables(self, content: str, context: dict) -> str:
        """
        Обрабатывает все переменные рекурсивно
        """
        
        def replace_variable(match):
            variable_name = match.group(1)
            return str(context.get(var_name, ""))
        
        return self.VARIABLE_PATTERN.sub(replace_variable, content)