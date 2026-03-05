# Sabo — Static Site Composer

**Sabo** — это локальный Python-framework для декларативной сборки статических фронтенд-проектов на основе JSON-описания.

Фреймворк позволяет описывать структуру сайта как модель данных и автоматически генерировать готовую HTML-структуру через встроенный механизм сборки.

Проект ориентирован на:

- разработчиков, которым нужен лёгкий статический генератор
- прототипирование UI-структур
- автоматизированную сборку шаблонных проектов
- создание расширяемых архитектур на Python

---

# Architecture


Sabo/
├── sabo/ # основной пакет фреймворка
│ ├── core/ # ядро системы
│ ├── models/ # модели данных проекта
│ │ ├── component.py
│ │ ├── page.py
│ │ └── project.py
│ ├── builder/ # логика сборки сайта
│ │ └── site_builder.py
│ └── utils/ # вспомогательные утилиты
│
├── sabo.py # CLI-интерфейс
├── pyproject.toml # конфигурация пакета
└── templates/ # шаблоны


---

# Core Concepts

## Project

Корневой объект системы.  
Содержит список страниц и общую конфигурацию проекта.

## Page

Представляет страницу сайта.

Каждая страница содержит список компонентов, которые будут сгенерированы в HTML.

## Component

Переиспользуемый UI-элемент.

Компоненты позволяют строить декларативную структуру интерфейса.

---

# Build System

Основная логика генерации реализована в:


sabo/builder/site_builder.py


`SiteBuilder` отвечает за:

- обход структуры проекта
- генерацию HTML-страниц
- сборку CSS
- сборку JavaScript
- организацию выходной директории

Результатом сборки является папка:


dist/


Пример:


dist/
├── index.html
├── about.html
├── contact.html
└── assets/
├── bundle.css
└── bundle.js


---

# CLI

CLI является основной точкой входа в систему.

После установки создаётся команда:


sabo


Основная команда сборки:


sabo build project.json


CLI выполняет:

1. загрузку JSON конфигурации
2. создание модели проекта
3. инициализацию SiteBuilder
4. запуск сборки

---

# Installation

## Через pip (рекомендуется)


pip install sabo


После установки становится доступна глобальная команда:


sabo


---

## Локальный запуск


git clone <repository>
cd Sabo
python sabo.py build primer.json


или


.\sabo.bat build primer.json


---

# Example Project Configuration

Пример файла `project.json`:

```json
{
  "name": "My Project",
  "pages": [
    {
      "name": "index",
      "components": []
    }
  ]
}
Build Example
sabo build project.json

Пример вывода:

Building project: test
Pages count: 3
 - Page: index
 - Page: about
 - Page: contact

✓ CSS bundle written
✓ JS bundle written
Build complete.
Design Principles

Sabo построен на следующих принципах:

Declarative project description

Separation of concerns

Minimal dependencies

Extensible architecture

Simple CLI workflow

Roadmap

Планируемые направления развития:

template engine

component slots

asset pipeline

plugin system

visual page builder