import os
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape
import markdown

class DocumentationGenerator:
    """Generates documentation from project analysis and screenshots."""
    
    def __init__(
        self,
        output_dir: str,
        project_info: Dict[str, Any],
        screenshots: Optional[Dict[str, str]] = None,
        format: str = 'md'
    ):
        """
        Initialize the documentation generator.
        
        Args:
            output_dir: Directory to save documentation
            project_info: Project information from ProjectAnalyzer
            screenshots: Screenshot paths from ScreenshotCapturer (optional)
            format: Output format ('md' or 'html')
        """
        self.output_dir = output_dir
        self.project_info = project_info
        self.screenshots = screenshots or {}
        self.format = format.lower()
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        
    def generate(self) -> None:
        """Generate complete documentation."""
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Generate main sections
        self._generate_index()
        self._generate_models_reference()
        self._generate_views_reference()
        self._generate_user_guide()
        self._generate_admin_guide()
        
        # Convert to HTML if needed
        if self.format == 'html':
            self._convert_markdown_to_html()
    
    def _generate_index(self) -> None:
        """Generate main index/overview page."""
        template = self.env.get_template('index.md.j2')
        content = template.render(
            apps=self.project_info['apps'],
            models_count=len(self.project_info['models']),
            urls_count=len(self.project_info['urls']),
        )
        
        with open(os.path.join(self.output_dir, 'index.md'), 'w') as f:
            f.write(content)
    
    def _generate_models_reference(self) -> None:
        """Generate models reference documentation."""
        template = self.env.get_template('models.md.j2')
        content = template.render(models=self.project_info['models'])
        
        with open(os.path.join(self.output_dir, 'models.md'), 'w') as f:
            f.write(content)
    
    def _generate_views_reference(self) -> None:
        """Generate views reference documentation."""
        template = self.env.get_template('views.md.j2')
        content = template.render(
            urls=self.project_info['urls'],
            views=self.project_info['views'],
            screenshots=self.screenshots
        )
        
        with open(os.path.join(self.output_dir, 'views.md'), 'w') as f:
            f.write(content)
    
    def _generate_user_guide(self) -> None:
        """Generate user-focused documentation."""
        template = self.env.get_template('user_guide.md.j2')
        content = template.render(
            urls=self.project_info['urls'],
            screenshots=self.screenshots
        )
        
        with open(os.path.join(self.output_dir, 'user_guide.md'), 'w') as f:
            f.write(content)
    
    def _generate_admin_guide(self) -> None:
        """Generate admin documentation."""
        template = self.env.get_template('admin_guide.md.j2')
        content = template.render(
            models=self.project_info['models'],
            screenshots=self.screenshots
        )
        
        with open(os.path.join(self.output_dir, 'admin_guide.md'), 'w') as f:
            f.write(content)
    
    def _convert_markdown_to_html(self) -> None:
        """Convert all Markdown files to HTML if format is html."""
        if self.format != 'html':
            return
            
        for filename in os.listdir(self.output_dir):
            if filename.endswith('.md'):
                md_path = os.path.join(self.output_dir, filename)
                html_path = os.path.join(self.output_dir, filename[:-3] + '.html')
                
                with open(md_path, 'r') as md_file:
                    md_content = md_file.read()
                    html_content = markdown.markdown(
                        md_content,
                        extensions=['tables', 'fenced_code', 'toc']
                    )
                    
                    # Add basic styling
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>{filename[:-3].title()}</title>
                        <style>
                            body {{ font-family: system-ui, -apple-system, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 2rem; }}
                            img {{ max-width: 100%; height: auto; }}
                            code {{ background: #f4f4f4; padding: 0.2em 0.4em; border-radius: 3px; }}
                            pre {{ background: #f4f4f4; padding: 1em; overflow-x: auto; }}
                            table {{ border-collapse: collapse; width: 100%; }}
                            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                            th {{ background-color: #f4f4f4; }}
                        </style>
                    </head>
                    <body>
                        {html_content}
                    </body>
                    </html>
                    """
                    
                    with open(html_path, 'w') as html_file:
                        html_file.write(html_content)
                        
                # Remove markdown file
                os.remove(md_path) 