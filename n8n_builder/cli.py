import click
import uvicorn
from pathlib import Path
import json
from .n8n_builder import N8NBuilder
from .validators import BaseWorkflowValidator

@click.group()
def cli():
    """N8N Workflow Builder CLI"""
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='Host to bind the server to')
@click.option('--port', default=8000, help='Port to bind the server to')
@click.option('--reload', is_flag=True, help='Enable auto-reload')
def serve(host: str, port: int, reload: bool):
    """Start the FastAPI server."""
    uvicorn.run("n8n_builder.app:app", host=host, port=port, reload=reload)

@cli.command()
@click.argument('description')
@click.option('--output', '-o', type=click.Path(), help='Output file for the workflow JSON')
def generate(description: str, output: str):
    """Generate a workflow from a description."""
    builder = N8NBuilder()
    validator = BaseWorkflowValidator()
    
    try:
        # Generate workflow
        workflow_json = builder.generate_workflow(description)
        
        # Validate workflow
        validation_result = validator.validate_workflow(workflow_json)
        
        # Print validation results
        click.echo("\nValidation Results:")
        if validation_result.is_valid:
            click.secho("✓ Workflow is valid", fg='green')
        else:
            click.secho("✗ Workflow has errors:", fg='red')
            for error in validation_result.errors:
                click.echo(f"  - {error}")
        
        if validation_result.warnings:
            click.secho("\nWarnings:", fg='yellow')
            for warning in validation_result.warnings:
                click.echo(f"  - {warning}")
        
        if validation_result.suggestions:
            click.secho("\nSuggestions:", fg='blue')
            for suggestion in validation_result.suggestions:
                click.echo(f"  - {suggestion}")
        
        # Save or print workflow
        if output:
            output_path = Path(output)
            output_path.write_text(workflow_json)
            click.echo(f"\nWorkflow saved to: {output_path}")
        else:
            click.echo("\nGenerated Workflow:")
            click.echo(json.dumps(json.loads(workflow_json), indent=2))
            
    except Exception as e:
        click.secho(f"Error: {str(e)}", fg='red')
        raise click.Abort()

if __name__ == '__main__':
    cli() 