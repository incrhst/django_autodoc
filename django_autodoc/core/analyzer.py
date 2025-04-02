import os
import sys
import importlib
from typing import Dict, List, Any, Optional
from django.apps import apps
from django.urls import URLPattern, URLResolver
from django.core.management import execute_from_command_line
from django.conf import settings

class ProjectAnalyzer:
    """Analyzes Django project structure and extracts relevant information."""
    
    def __init__(self, project_path: str, settings_module: Optional[str] = None):
        """
        Initialize the project analyzer.
        
        Args:
            project_path: Path to the Django project
            settings_module: Django settings module name (optional)
        """
        self.project_path = os.path.abspath(project_path)
        self.settings_module = settings_module
        self._setup_django_environment()
        
    def _setup_django_environment(self) -> None:
        """Set up Django environment for analysis."""
        sys.path.insert(0, self.project_path)
        
        if self.settings_module:
            os.environ['DJANGO_SETTINGS_MODULE'] = self.settings_module
        else:
            # Try to detect settings module
            for root, dirs, files in os.walk(self.project_path):
                if 'settings.py' in files:
                    relative_path = os.path.relpath(root, self.project_path)
                    module_path = relative_path.replace(os.sep, '.') + '.settings'
                    os.environ['DJANGO_SETTINGS_MODULE'] = module_path
                    break
        
        # Initialize Django
        import django
        django.setup()
    
    def analyze(self) -> Dict[str, Any]:
        """
        Analyze the Django project and return structured information.
        
        Returns:
            Dict containing project structure information
        """
        return {
            'apps': self._analyze_apps(),
            'urls': self._analyze_urls(),
            'models': self._analyze_models(),
            'views': self._analyze_views(),
            'forms': self._analyze_forms(),
            'templates': self._analyze_templates(),
        }
    
    def _analyze_apps(self) -> List[Dict[str, Any]]:
        """Analyze installed Django apps."""
        app_configs = []
        for app_config in apps.get_app_configs():
            app_configs.append({
                'name': app_config.name,
                'label': app_config.label,
                'path': app_config.path,
                'models': [model._meta.model_name for model in app_config.get_models()],
            })
        return app_configs
    
    def _analyze_models(self) -> Dict[str, Any]:
        """Analyze Django models."""
        models_info = {}
        for model in apps.get_models():
            model_info = {
                'fields': [],
                'methods': [],
                'meta': {},
            }
            
            # Analyze fields
            for field in model._meta.get_fields():
                field_info = {
                    'name': field.name,
                    'type': field.__class__.__name__,
                    'required': not field.null if hasattr(field, 'null') else True,
                }
                model_info['fields'].append(field_info)
            
            # Analyze methods
            for attr in dir(model):
                if not attr.startswith('_') and callable(getattr(model, attr)):
                    model_info['methods'].append(attr)
            
            # Get meta options
            if model._meta:
                model_info['meta'] = {
                    'verbose_name': model._meta.verbose_name,
                    'verbose_name_plural': model._meta.verbose_name_plural,
                    'ordering': model._meta.ordering,
                }
            
            models_info[f"{model._meta.app_label}.{model._meta.model_name}"] = model_info
        
        return models_info
    
    def _analyze_urls(self) -> List[Dict[str, Any]]:
        """Analyze URL patterns."""
        from django.urls import get_resolver
        
        def _process_url_pattern(pattern: URLPattern) -> Dict[str, Any]:
            return {
                'pattern': str(pattern.pattern),
                'name': pattern.name,
                'view_name': pattern.callback.__name__ if pattern.callback else None,
                'view_class': pattern.callback.__class__.__name__ if pattern.callback and hasattr(pattern.callback, '__class__') else None,
            }
        
        def _process_url_patterns(patterns) -> List[Dict[str, Any]]:
            urls = []
            for pattern in patterns:
                if isinstance(pattern, URLResolver):
                    urls.extend(_process_url_patterns(pattern.url_patterns))
                else:
                    urls.append(_process_url_pattern(pattern))
            return urls
        
        resolver = get_resolver()
        return _process_url_patterns(resolver.url_patterns)
    
    def _analyze_views(self) -> Dict[str, Any]:
        """Analyze views."""
        # This will be implemented to extract view information
        return {}
    
    def _analyze_forms(self) -> Dict[str, Any]:
        """Analyze forms."""
        # This will be implemented to extract form information
        return {}
    
    def _analyze_templates(self) -> Dict[str, Any]:
        """Analyze templates."""
        # This will be implemented to extract template information
        return {} 