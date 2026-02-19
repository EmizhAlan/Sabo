# Sabo — Static Site Composer

Sabo — локальный framework для сборки фронтенд-проектов.

##Структура проекта

Sabo/
├── sabo.py                 # главный CLI
├── sabo.bat                # batch-обёртка для Windows
├── sabo/                   # пакет фреймворка
│   ├── __init__.py
│   ├── core/
│   │    └── __init__.py
│   ├── models/
│   │    ├── __init__.py
│   │    ├── component.py
│   │    ├── page.py
│   │    └── project.py
│   ├── builder/
│   │    ├── __init__.py
│   │    └── site_builder.py
│   └── utils/
│        └── __init__.py
└── primer.json             # пример проекта

sabo/ - пакет фреймворка
sabo.py - главный скрипт фреймворка, отвечает за обработку команды build, загружает проект json и вызывает builder.
sabo.bat - batch-обертка для Windows, позволляет запускать Sabo из Windows PowerShell или командной строки .\sabo.bat build name_your_project.json
models/ - пакет моделей данных фреймворка
builder/ - пакет билдера сайта
utils/ - пакет утилит фреймворка
core/ - пакет ядра фреймворка

## Установка

1. Скачайте репозиторий
2. Для Windows используйте PowerShell:

```powershell
.\sabo.bat build primer.json