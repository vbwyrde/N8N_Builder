"""
Self-Healer System for N8N Builder

A comprehensive self-healing and self-improving system that automatically detects,
analyzes, and resolves issues in the n8n workflow builder system.

Architecture Components:
- Error Detection: Monitors logs and system state for issues
- Context Analysis: Gathers relevant documentation and code context
- Solution Generation: Uses local LLM to create targeted fixes
- Validation & Safety: Tests solutions before applying them
- Learning & Improvement: Learns from successful and failed fixes

Integration Points:
- Extends existing logging and error handling systems
- Uses documentation structure for context retrieval
- Integrates with performance monitoring and retry logic
- Coordinates with project management for safe operations
"""

from .core.healer_manager import SelfHealerManager
from .core.error_monitor import ErrorMonitor
from .core.context_analyzer import ContextAnalyzer
from .core.solution_generator import SolutionGenerator
from .core.solution_validator import SolutionValidator
from .core.learning_engine import LearningEngine

__version__ = "1.0.0"
__all__ = [
    "SelfHealerManager",
    "ErrorMonitor", 
    "ContextAnalyzer",
    "SolutionGenerator",
    "SolutionValidator",
    "LearningEngine"
]
