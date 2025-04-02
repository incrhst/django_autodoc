import os
import sys
import unittest
from django_autodoc.core.analyzer import ProjectAnalyzer

class TestProjectAnalyzer(unittest.TestCase):
    def setUp(self):
        # Create a minimal Django project structure for testing
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.join(self.test_dir, 'test_project')
        os.makedirs(self.project_dir, exist_ok=True)
        
        # Create settings.py
        with open(os.path.join(self.project_dir, 'settings.py'), 'w') as f:
            f.write("""
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

SECRET_KEY = 'test-key'
            """)
    
    def test_project_analysis(self):
        analyzer = ProjectAnalyzer(
            project_path=self.project_dir,
            settings_module='settings'
        )
        result = analyzer.analyze()
        
        # Basic assertions
        self.assertIsInstance(result, dict)
        self.assertIn('apps', result)
        self.assertIn('models', result)
        self.assertIn('urls', result)
        
        # Check if default Django apps are found
        app_names = [app['name'] for app in result['apps']]
        self.assertIn('django.contrib.admin', app_names)
        self.assertIn('django.contrib.auth', app_names)
    
    def tearDown(self):
        # Clean up test project directory
        import shutil
        if os.path.exists(self.project_dir):
            shutil.rmtree(self.project_dir)

if __name__ == '__main__':
    unittest.main() 