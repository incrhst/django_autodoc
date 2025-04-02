import os
import click
from typing import Optional

from ..core.analyzer import ProjectAnalyzer
from ..core.capturer import ScreenshotCapturer
from ..core.generator import DocumentationGenerator

@click.command()
@click.option(
    '--project',
    required=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help='Path to Django project'
)
@click.option(
    '--settings',
    required=False,
    help='Django settings module name'
)
@click.option(
    '--url',
    required=False,
    help='Base URL of running application for screenshots'
)
@click.option(
    '--output',
    default='docs',
    type=click.Path(file_okay=False, dir_okay=True),
    help='Output directory for documentation'
)
@click.option(
    '--format',
    type=click.Choice(['md', 'html'], case_sensitive=False),
    default='md',
    help='Output format'
)
@click.option(
    '--username',
    required=False,
    help='Admin username for authenticated views'
)
@click.option(
    '--password',
    required=False,
    help='Admin password for authenticated views'
)
def main(
    project: str,
    settings: Optional[str],
    url: Optional[str],
    output: str,
    format: str,
    username: Optional[str],
    password: Optional[str]
) -> None:
    """Generate user documentation for Django projects."""
    
    click.echo("Analyzing Django project...")
    analyzer = ProjectAnalyzer(project, settings)
    project_info = analyzer.analyze()
    
    screenshots = {}
    if url:
        click.echo("Capturing screenshots...")
        capturer = ScreenshotCapturer(
            base_url=url,
            output_dir=os.path.join(output, 'screenshots'),
            username=username,
            password=password
        )
        screenshots = capturer.capture_screenshots(project_info['urls'])
    
    click.echo("Generating documentation...")
    generator = DocumentationGenerator(
        output_dir=output,
        project_info=project_info,
        screenshots=screenshots,
        format=format
    )
    generator.generate()
    
    click.echo(f"Documentation generated in {output} directory")

if __name__ == '__main__':
    main() 