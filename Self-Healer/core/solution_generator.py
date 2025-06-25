"""
Solution Generator - Creates targeted solutions for detected errors.

This module uses local LLM and pattern-based approaches to generate
comprehensive solutions for detected errors based on gathered context.
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import re

# Import existing N8N Builder components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.error_handler import ErrorDetail
from n8n_builder.logging_config import get_logger
from n8n_builder.config import config


class SolutionType(Enum):
    """Types of solutions that can be generated."""
    IMMEDIATE_FIX = "immediate_fix"
    SYSTEMATIC_REPAIR = "systematic_repair"
    PREVENTIVE_MEASURE = "preventive_measure"
    CONFIGURATION_CHANGE = "configuration_change"
    CODE_IMPROVEMENT = "code_improvement"


class SolutionPriority(Enum):
    """Priority levels for solutions."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Solution:
    """Represents a generated solution."""
    solution_id: str
    solution_type: SolutionType
    priority: SolutionPriority
    title: str
    description: str
    
    # Implementation details
    steps: List[Dict[str, Any]] = field(default_factory=list)
    code_changes: List[Dict[str, Any]] = field(default_factory=list)
    config_changes: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    confidence: float = 0.0
    estimated_time: int = 0  # minutes
    risk_level: str = "medium"
    prerequisites: List[str] = field(default_factory=list)
    
    # Validation info
    can_be_automated: bool = False
    requires_user_input: bool = False
    rollback_possible: bool = True
    
    # Context
    applicable_errors: List[str] = field(default_factory=list)
    related_components: List[str] = field(default_factory=list)

    # Internal ranking
    ranking_score: float = 0.0


class SolutionGenerator:
    """
    Generates targeted solutions for detected errors.
    
    Features:
    - Local LLM integration for intelligent solution generation
    - Pattern-based solutions for common error types
    - Multi-strategy approach with different solution types
    - Risk assessment and confidence scoring
    - Automated vs manual solution classification
    """
    
    def __init__(self):
        """Initialize the Solution Generator."""
        self.logger = get_logger('self_healer.solution_generator')
        
        # LLM configuration
        self.llm_config = config.mimo_llm
        
        # Solution templates and patterns
        self.solution_templates = self._load_solution_templates()
        self.pattern_solutions = self._load_pattern_solutions()
        
        # State
        self.is_running = False
        self.generated_solutions: Dict[str, List[Solution]] = {}
        
        self.logger.info("Solution Generator initialized")
    
    def _load_solution_templates(self) -> Dict[str, Dict[str, Any]]:
        """Load solution templates for different error categories."""
        return {
            'llm_communication': {
                'connection_failed': {
                    'title': 'Fix LLM Connection',
                    'steps': [
                        {'action': 'check_service', 'target': 'LM Studio'},
                        {'action': 'verify_endpoint', 'target': 'localhost:1234'},
                        {'action': 'test_connection', 'timeout': 30},
                        {'action': 'restart_service', 'if_needed': True}
                    ],
                    'confidence': 0.8,
                    'risk_level': 'low'
                },
                'model_not_loaded': {
                    'title': 'Load Required Model',
                    'steps': [
                        {'action': 'check_model_availability', 'model': 'mimo-vl-7b-rl'},
                        {'action': 'load_model', 'model': 'mimo-vl-7b-rl'},
                        {'action': 'verify_model_loaded'},
                        {'action': 'test_inference'}
                    ],
                    'confidence': 0.9,
                    'risk_level': 'low'
                }
            },
            'json_parsing': {
                'invalid_format': {
                    'title': 'Fix JSON Format Issues',
                    'steps': [
                        {'action': 'validate_json', 'fix_common_issues': True},
                        {'action': 'check_encoding', 'ensure_utf8': True},
                        {'action': 'verify_structure', 'against_schema': True}
                    ],
                    'confidence': 0.7,
                    'risk_level': 'low'
                }
            },
            'workflow_structure': {
                'missing_fields': {
                    'title': 'Add Missing Required Fields',
                    'steps': [
                        {'action': 'identify_missing_fields'},
                        {'action': 'add_default_values'},
                        {'action': 'validate_structure'}
                    ],
                    'confidence': 0.8,
                    'risk_level': 'medium'
                }
            },
            'performance': {
                'memory_issue': {
                    'title': 'Optimize Memory Usage',
                    'steps': [
                        {'action': 'clear_cache'},
                        {'action': 'optimize_data_structures'},
                        {'action': 'implement_streaming', 'if_large_data': True}
                    ],
                    'confidence': 0.6,
                    'risk_level': 'medium'
                },
                'timeout': {
                    'title': 'Resolve Timeout Issues',
                    'steps': [
                        {'action': 'increase_timeout_limits'},
                        {'action': 'implement_retry_logic'},
                        {'action': 'optimize_processing'}
                    ],
                    'confidence': 0.7,
                    'risk_level': 'low'
                }
            }
        }
    
    def _load_pattern_solutions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Load pattern-based solutions for common error patterns."""
        return {
            'file_not_found': [
                {
                    'type': 'create_missing_file',
                    'confidence': 0.8,
                    'steps': ['check_path', 'create_directory', 'create_file']
                },
                {
                    'type': 'fix_path_reference',
                    'confidence': 0.7,
                    'steps': ['analyze_path', 'correct_path', 'update_references']
                }
            ],
            'permission_denied': [
                {
                    'type': 'fix_permissions',
                    'confidence': 0.9,
                    'steps': ['check_permissions', 'update_permissions', 'verify_access']
                }
            ],
            'connection_refused': [
                {
                    'type': 'restart_service',
                    'confidence': 0.8,
                    'steps': ['check_service_status', 'restart_service', 'verify_connection']
                },
                {
                    'type': 'check_configuration',
                    'confidence': 0.7,
                    'steps': ['validate_config', 'fix_config', 'reload_config']
                }
            ]
        }
    
    async def start(self):
        """Start the solution generator."""
        if self.is_running:
            self.logger.warning("Solution Generator is already running")
            return
        
        self.is_running = True
        self.logger.info("Solution Generator started successfully")
    
    async def stop(self):
        """Stop the solution generator."""
        if not self.is_running:
            return
        
        self.is_running = False
        self.logger.info("Solution Generator stopped")
    
    async def generate_solutions(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate comprehensive solutions for an error.
        
        Args:
            error_detail: The error to solve
            context: Comprehensive context information
            
        Returns:
            List of generated solutions
        """
        try:
            error_id = context.get('error_id', 'unknown')
            self.logger.info(f"Generating solutions for error: {error_id}")
            
            solutions = []
            
            # Generate different types of solutions
            immediate_solutions = await self._generate_immediate_solutions(error_detail, context)
            systematic_solutions = await self._generate_systematic_solutions(error_detail, context)
            preventive_solutions = await self._generate_preventive_solutions(error_detail, context)
            
            solutions.extend(immediate_solutions)
            solutions.extend(systematic_solutions)
            solutions.extend(preventive_solutions)
            
            # Use LLM for additional intelligent solutions
            llm_solutions = await self._generate_llm_solutions(error_detail, context)
            solutions.extend(llm_solutions)
            
            # Rank and filter solutions
            ranked_solutions = self._rank_solutions(solutions, error_detail, context)
            
            # Convert to dictionaries for return
            solution_dicts = []
            for solution in ranked_solutions:
                solution_dict = {
                    'solution_id': solution.solution_id,
                    'type': solution.solution_type.value,
                    'priority': solution.priority.value,
                    'title': solution.title,
                    'description': solution.description,
                    'steps': solution.steps,
                    'code_changes': solution.code_changes,
                    'config_changes': solution.config_changes,
                    'confidence': solution.confidence,
                    'estimated_time': solution.estimated_time,
                    'risk_level': solution.risk_level,
                    'can_be_automated': solution.can_be_automated,
                    'requires_user_input': solution.requires_user_input,
                    'rollback_possible': solution.rollback_possible,
                    'prerequisites': solution.prerequisites
                }
                solution_dicts.append(solution_dict)
            
            # Cache solutions
            self.generated_solutions[error_id] = ranked_solutions
            
            self.logger.info(f"Generated {len(solution_dicts)} solutions for error: {error_id}")
            return solution_dicts
            
        except Exception as e:
            self.logger.error(f"Error generating solutions: {e}")
            return []
    
    async def _generate_immediate_solutions(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Solution]:
        """Generate immediate fix solutions."""
        solutions = []
        
        try:
            error_category = context.get('error_category', 'unknown')
            
            # Check for template-based solutions
            category_templates = self.solution_templates.get(error_category, {})
            
            for template_name, template in category_templates.items():
                if self._template_matches_error(template_name, error_detail):
                    solution = Solution(
                        solution_id=f"immediate_{template_name}_{int(datetime.now().timestamp())}",
                        solution_type=SolutionType.IMMEDIATE_FIX,
                        priority=SolutionPriority.HIGH,
                        title=template['title'],
                        description=f"Immediate fix for {error_category} error",
                        steps=template['steps'],
                        confidence=template.get('confidence', 0.5),
                        risk_level=template.get('risk_level', 'medium'),
                        can_be_automated=True,
                        estimated_time=5
                    )
                    solutions.append(solution)
            
            # Check for pattern-based solutions
            error_message = error_detail.message.lower()
            for pattern, pattern_solutions in self.pattern_solutions.items():
                if pattern in error_message:
                    for pattern_solution in pattern_solutions:
                        solution = Solution(
                            solution_id=f"pattern_{pattern}_{int(datetime.now().timestamp())}",
                            solution_type=SolutionType.IMMEDIATE_FIX,
                            priority=SolutionPriority.MEDIUM,
                            title=f"Fix {pattern.replace('_', ' ').title()}",
                            description=f"Pattern-based solution for {pattern}",
                            steps=[{'action': step} for step in pattern_solution['steps']],
                            confidence=pattern_solution.get('confidence', 0.6),
                            can_be_automated=True,
                            estimated_time=10
                        )
                        solutions.append(solution)
        
        except Exception as e:
            self.logger.error(f"Error generating immediate solutions: {e}")
        
        return solutions

    async def _generate_systematic_solutions(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Solution]:
        """Generate systematic repair solutions."""
        solutions = []

        try:
            error_category = context.get('error_category', 'unknown')
            affected_components = context.get('affected_components', [])

            # Generate component-specific solutions
            for component in affected_components:
                solution = Solution(
                    solution_id=f"systematic_{component}_{int(datetime.now().timestamp())}",
                    solution_type=SolutionType.SYSTEMATIC_REPAIR,
                    priority=SolutionPriority.MEDIUM,
                    title=f"Systematic Repair of {component}",
                    description=f"Comprehensive repair of {component} to address root cause",
                    steps=[
                        {'action': 'analyze_component', 'target': component},
                        {'action': 'identify_issues', 'target': component},
                        {'action': 'apply_fixes', 'target': component},
                        {'action': 'test_component', 'target': component}
                    ],
                    confidence=0.6,
                    estimated_time=30,
                    risk_level='medium',
                    can_be_automated=False,
                    requires_user_input=True
                )
                solutions.append(solution)

        except Exception as e:
            self.logger.error(f"Error generating systematic solutions: {e}")

        return solutions

    async def _generate_preventive_solutions(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Solution]:
        """Generate preventive measure solutions."""
        solutions = []

        try:
            error_category = context.get('error_category', 'unknown')

            # Generate category-specific preventive measures
            preventive_measures = {
                'llm_communication': [
                    {
                        'title': 'Implement Connection Health Monitoring',
                        'description': 'Add monitoring to detect LLM connection issues early',
                        'steps': [
                            {'action': 'add_health_check', 'interval': 60},
                            {'action': 'implement_alerts'},
                            {'action': 'add_fallback_logic'}
                        ]
                    }
                ],
                'json_parsing': [
                    {
                        'title': 'Add JSON Validation Layer',
                        'description': 'Implement comprehensive JSON validation before processing',
                        'steps': [
                            {'action': 'add_schema_validation'},
                            {'action': 'implement_sanitization'},
                            {'action': 'add_error_recovery'}
                        ]
                    }
                ],
                'performance': [
                    {
                        'title': 'Implement Performance Monitoring',
                        'description': 'Add monitoring to detect performance issues early',
                        'steps': [
                            {'action': 'add_performance_metrics'},
                            {'action': 'implement_thresholds'},
                            {'action': 'add_auto_optimization'}
                        ]
                    }
                ]
            }

            measures = preventive_measures.get(error_category, [])
            for measure in measures:
                solution = Solution(
                    solution_id=f"preventive_{error_category}_{int(datetime.now().timestamp())}",
                    solution_type=SolutionType.PREVENTIVE_MEASURE,
                    priority=SolutionPriority.LOW,
                    title=measure['title'],
                    description=measure['description'],
                    steps=measure['steps'],
                    confidence=0.7,
                    estimated_time=60,
                    risk_level='low',
                    can_be_automated=False,
                    requires_user_input=True
                )
                solutions.append(solution)

        except Exception as e:
            self.logger.error(f"Error generating preventive solutions: {e}")

        return solutions

    async def _generate_llm_solutions(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Solution]:
        """Generate solutions using local LLM."""
        solutions = []

        try:
            # Prepare prompt for LLM
            prompt = self._build_solution_prompt(error_detail, context)

            # Call LLM (simplified - would use actual LLM integration)
            llm_response = await self._call_llm_for_solution(prompt)

            if llm_response:
                # Parse LLM response and create solutions
                parsed_solutions = self._parse_llm_response(llm_response)
                solutions.extend(parsed_solutions)

        except Exception as e:
            self.logger.error(f"Error generating LLM solutions: {e}")

        return solutions

    def _build_solution_prompt(self, error_detail: ErrorDetail, context: Dict[str, Any]) -> str:
        """Build a prompt for the LLM to generate solutions."""
        prompt = f"""
You are an expert system administrator and developer. Analyze the following error and provide specific, actionable solutions.

ERROR DETAILS:
- Category: {context.get('error_category', 'unknown')}
- Severity: {context.get('error_severity', 'unknown')}
- Title: {error_detail.title}
- Message: {error_detail.message}
- Technical Details: {error_detail.technical_details or 'None'}

CONTEXT:
- Affected Components: {', '.join(context.get('affected_components', []))}
- Related Files: {len(context.get('related_files', []))} files identified
- System: N8N Builder workflow automation system

REQUIREMENTS:
1. Provide 1-3 specific, actionable solutions
2. For each solution, include:
   - Clear title
   - Step-by-step instructions
   - Risk level (low/medium/high)
   - Estimated time to implement
   - Whether it can be automated

Focus on practical solutions that address the root cause while maintaining system stability.
"""
        return prompt

    async def _call_llm_for_solution(self, prompt: str) -> Optional[str]:
        """Call the local LLM to generate solutions."""
        try:
            # This would integrate with the actual LLM service
            # For now, return None to indicate LLM is not available
            self.logger.debug("LLM solution generation not implemented yet")
            return None

        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            return None

    def _parse_llm_response(self, response: str) -> List[Solution]:
        """Parse LLM response into Solution objects."""
        solutions = []

        try:
            # This would parse the LLM response and create Solution objects
            # Implementation depends on LLM response format
            pass

        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {e}")

        return solutions

    def _template_matches_error(self, template_name: str, error_detail: ErrorDetail) -> bool:
        """Check if a template matches the current error."""
        error_message = error_detail.message.lower()
        technical_details = (error_detail.technical_details or "").lower()

        # Simple keyword matching - could be enhanced
        template_keywords = {
            'connection_failed': ['connection', 'failed', 'refused', 'timeout'],
            'model_not_loaded': ['model', 'not loaded', 'unavailable'],
            'invalid_format': ['format', 'invalid', 'syntax', 'parse'],
            'missing_fields': ['missing', 'required', 'field'],
            'memory_issue': ['memory', 'out of memory', 'allocation'],
            'timeout': ['timeout', 'timed out', 'slow']
        }

        keywords = template_keywords.get(template_name, [])
        for keyword in keywords:
            if keyword in error_message or keyword in technical_details:
                return True

        return False

    def _rank_solutions(self, solutions: List[Solution], error_detail: ErrorDetail, context: Dict[str, Any]) -> List[Solution]:
        """Rank solutions by priority, confidence, and relevance."""
        try:
            # Calculate ranking score for each solution
            for solution in solutions:
                score = 0.0

                # Priority weight
                priority_weights = {
                    SolutionPriority.CRITICAL: 1.0,
                    SolutionPriority.HIGH: 0.8,
                    SolutionPriority.MEDIUM: 0.6,
                    SolutionPriority.LOW: 0.4
                }
                score += priority_weights.get(solution.priority, 0.5) * 0.3

                # Confidence weight
                score += solution.confidence * 0.4

                # Automation preference (automated solutions ranked higher)
                if solution.can_be_automated:
                    score += 0.2

                # Risk penalty (lower risk preferred)
                risk_penalties = {'low': 0.0, 'medium': -0.1, 'high': -0.2}
                score += risk_penalties.get(solution.risk_level, -0.1)

                # Time preference (faster solutions preferred)
                if solution.estimated_time <= 10:
                    score += 0.1
                elif solution.estimated_time >= 60:
                    score -= 0.1

                solution.ranking_score = score

            # Sort by ranking score
            solutions.sort(key=lambda s: getattr(s, 'ranking_score', 0), reverse=True)

            # Limit to top 10 solutions
            return solutions[:10]

        except Exception as e:
            self.logger.error(f"Error ranking solutions: {e}")
            return solutions

    def get_solution_by_id(self, solution_id: str) -> Optional[Solution]:
        """Get a specific solution by ID."""
        for error_solutions in self.generated_solutions.values():
            for solution in error_solutions:
                if solution.solution_id == solution_id:
                    return solution
        return None

    def get_solutions_for_error(self, error_id: str) -> List[Solution]:
        """Get all solutions for a specific error."""
        return self.generated_solutions.get(error_id, [])
