# Django Autodoc

A powerful documentation generator for Django projects that automatically creates comprehensive user manuals with screenshots.

## Features

- Analyzes Django project structure and components
- Extracts information from models, views, URLs, forms, and templates
- Captures screenshots of running views
- Generates user-friendly documentation with navigation
- Supports both Markdown and HTML output formats

## Installation

```bash
pip install django-autodoc
```

## Usage

Basic usage without screenshots:

```bash
django-autodoc --project /path/to/myproject --settings myproject.settings --output ./documentation
```

Generate documentation with screenshots:

```bash
django-autodoc --project /path/to/myproject --url http://localhost:8000 --username admin --password securepass
```

## Requirements

- Python 3.8+
- Django 3.2+
- A running Django application (for screenshot capture)
- Chrome/Chromium browser (for screenshot capture)

## Documentation Structure

The generated documentation includes:

1. README / Index with overview and navigation
2. Models Reference with data structures
3. Views Reference with technical details
4. User Guide with task-oriented instructions
5. Admin Guide for administrative functions

## License

MIT License - see LICENSE file for details. 