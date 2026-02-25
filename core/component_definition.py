"""
ComponentDefinitio представляет собой 
загруженный компонент из каталога компонентов
"""

class ComponentDefinition:
    
    def __init__(self, name, template, css="", js="", props=None):
        self.name = name
        self.template = template
        self.css = css
        self.js = js
        self.props = props or {}
        
    def __repr__(self):
        return f"<ComponentDefinition {self.name}>"