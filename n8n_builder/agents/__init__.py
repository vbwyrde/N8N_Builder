"""
Agent system for N8N Workflow Builder.

This module provides the agent architecture for the N8N Workflow Builder,
including AG-UI compatible agents and integration components.
"""

from .base_agent import (
    AgentConfig,
    AgentResult,
    BaseAgent,
    OrchestratorAgent,
    WorkflowGeneratorAgent,
    ValidationAgent,
    WorkflowExecutorAgent,
    ErrorRecoveryAgent,
    WorkflowOptimizerAgent,
    WorkflowDocumentationAgent,
    WorkflowTestingAgent
)

__all__ = [
    'AgentConfig',
    'AgentResult',
    'BaseAgent',
    'OrchestratorAgent',
    'WorkflowGeneratorAgent',
    'ValidationAgent',
    'WorkflowExecutorAgent',
    'ErrorRecoveryAgent',
    'WorkflowOptimizerAgent',
    'WorkflowDocumentationAgent',
    'WorkflowTestingAgent'
]
