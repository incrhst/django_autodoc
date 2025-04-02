# Django Autodoc

A powerful documentation generator for Django projects that automatically creates comprehensive user manuals with screenshots.

## Features

- Analyzes Django project structure and components
- Extracts information from models, views, URLs, forms, and templates
- Captures screenshots of running views
- Generates user-friendly documentation with navigation
- Supports both Markdown and HTML output formats

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone https://github.com/incrhst/django_autodoc.git
cd django_autodoc
```

2. Install in development mode:
```bash
pip install -e .
```

This will install the package in "editable" mode, meaning changes to the source code will be reflected immediately without needing to reinstall.

### Requirements

- Python 3.8+
- Django 3.2+
- A running Django application (for screenshot capture)
- Chrome/Chromium browser (for screenshot capture)

## Usage

Basic usage without screenshots:

```bash
django-autodoc --project /path/to/myproject --settings myproject.settings --output ./documentation
```

Generate documentation with screenshots:

```bash
django-autodoc --project /path/to/myproject --url http://localhost:8000 --username admin --password securepass
```

## Documentation Structure

The generated documentation includes:

1. README / Index with overview and navigation
2. Models Reference with data structures
3. Views Reference with technical details
4. User Guide with task-oriented instructions
5. Admin Guide for administrative functions

## Development

To contribute to the project:

1. Fork the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Run tests:
```bash
python -m unittest discover tests
```

## License

MIT License - see LICENSE file for details. 