"""
N8N Workflow Builder - A tool for generating n8n workflows using natural language.
"""

from .n8n_builder import N8NBuilder
from .validators import BaseWorkflowValidator, ValidationResult
from .app import app

__version__ = "0.1.0"
__all__ = ["N8NBuilder", "BaseWorkflowValidator", "ValidationResult", "app"]

"""
N8N Builder package initialization.
""" 