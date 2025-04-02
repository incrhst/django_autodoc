from setuptools import setup, find_packages

setup(
    name="django-autodoc",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "Django>=3.2",
        "selenium>=4.0.0",
        "webdriver-manager>=3.8.0",
        "Markdown>=3.3.0",
        "Jinja2>=3.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "django-autodoc=django_autodoc.cli.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="Automatic documentation generator for Django projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/django-autodoc",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
) 