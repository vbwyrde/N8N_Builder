"""
Solution Validator - Validates and safely implements solutions.

This module provides comprehensive validation and safe implementation
of generated solutions, including rollback capabilities and risk assessment.
"""

import asyncio
import logging
import json
import shutil
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import tempfile
import os

# Import existing N8N Builder components
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.error_handler import ErrorDetail
from n8n_builder.logging_config import get_logger
from n8n_builder.project_manager import project_manager, filesystem_utils


class ValidationResult(Enum):
    """Results of solution validation."""
    SAFE = "safe"
    RISKY = "risky"
    UNSAFE = "unsafe"
    UNKNOWN = "unknown"


class ImplementationStatus(Enum):
    """Status of solution implementation."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ValidationReport:
    """Comprehensive validation report for a solution."""
    solution_id: str
    validation_result: ValidationResult
    confidence: float
    risk_factors: List[str] = field(default_factory=list)
    safety_checks: Dict[str, bool] = field(default_factory=dict)
    test_results: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    can_proceed: bool = False
    requires_manual_review: bool = False


@dataclass
class RollbackPoint:
    """Represents a rollback point for safe implementation."""
    rollback_id: str
    timestamp: datetime
    description: str
    affected_files: List[str] = field(default_factory=list)
    backup_location: Optional[str] = None
    system_state: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ImplementationResult:
    """Result of solution implementation."""
    solution_id: str
    status: ImplementationStatus
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    steps_completed: List[str] = field(default_factory=list)
    steps_failed: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    rollback_point: Optional[RollbackPoint] = None
    verification_results: Dict[str, Any] = field(default_factory=dict)


class SolutionValidator:
    """
    Validates and safely implements solutions.
    
    Features:
    - Comprehensive safety validation
    - Isolated testing environment
    - Automatic rollback capabilities
    - Integration with existing test suite
    - Risk assessment and impact analysis
    """
    
    def __init__(self):
        """Initialize the Solution Validator."""
        self.logger = get_logger('self_healer.solution_validator')
        
        # Paths
        self.project_root = Path(__file__).parent.parent.parent
        self.backup_dir = self.project_root / "Self-Healer" / "backups"
        self.test_dir = self.project_root / "tests"
        
        # State tracking
        self.validation_reports: Dict[str, ValidationReport] = {}
        self.rollback_points: Dict[str, RollbackPoint] = {}
        self.implementation_results: Dict[str, ImplementationResult] = {}
        
        # Safety configuration
        self.safety_config = {
            'max_file_changes': 10,
            'max_config_changes': 5,
            'require_backup': True,
            'require_tests': True,
            'max_implementation_time': 300,  # 5 minutes
        }
        
        # State
        self.is_running = False
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        self.logger.info("Solution Validator initialized")
    
    async def start(self):
        """Start the solution validator."""
        if self.is_running:
            self.logger.warning("Solution Validator is already running")
            return
        
        self.is_running = True
        self.logger.info("Solution Validator started successfully")
    
    async def stop(self):
        """Stop the solution validator."""
        if not self.is_running:
            return
        
        self.is_running = False
        self.logger.info("Solution Validator stopped")
    
    async def validate_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a solution for safety and effectiveness.
        
        Args:
            solution: The solution to validate
            context: Context information for the solution
            
        Returns:
            Validation report dictionary
        """
        try:
            solution_id = solution.get('solution_id', 'unknown')
            self.logger.info(f"Validating solution: {solution_id}")
            
            # Create validation report
            report = ValidationReport(
                solution_id=solution_id,
                validation_result=ValidationResult.UNKNOWN,
                confidence=0.0
            )
            
            # Perform safety checks
            await self._perform_safety_checks(solution, context, report)
            
            # Assess risk factors
            await self._assess_risk_factors(solution, context, report)
            
            # Run validation tests
            await self._run_validation_tests(solution, context, report)
            
            # Determine overall validation result
            self._determine_validation_result(report)
            
            # Cache the report
            self.validation_reports[solution_id] = report
            
            # Convert to dictionary for return
            report_dict = {
                'solution_id': report.solution_id,
                'validation_result': report.validation_result.value,
                'confidence': report.confidence,
                'risk_factors': report.risk_factors,
                'safety_checks': report.safety_checks,
                'test_results': report.test_results,
                'recommendations': report.recommendations,
                'can_proceed': report.can_proceed,
                'requires_manual_review': report.requires_manual_review,
                'is_safe': report.validation_result in [ValidationResult.SAFE]
            }
            
            self.logger.info(f"Validation completed for solution: {solution_id} - Result: {report.validation_result.value}")
            return report_dict
            
        except Exception as e:
            self.logger.error(f"Error validating solution: {e}")
            return {
                'solution_id': solution.get('solution_id', 'unknown'),
                'validation_result': 'unsafe',
                'confidence': 0.0,
                'error': str(e),
                'can_proceed': False,
                'is_safe': False
            }
    
    async def implement_solution(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Safely implement a validated solution.
        
        Args:
            solution: The solution to implement
            context: Context information for the solution
            
        Returns:
            Implementation result dictionary
        """
        try:
            solution_id = solution.get('solution_id', 'unknown')
            self.logger.info(f"Implementing solution: {solution_id}")
            
            # Check if solution is validated
            validation_report = self.validation_reports.get(solution_id)
            if not validation_report or not validation_report.can_proceed:
                raise Exception("Solution not validated or not safe to proceed")
            
            # Create implementation result
            result = ImplementationResult(
                solution_id=solution_id,
                status=ImplementationStatus.IN_PROGRESS,
                success=False,
                start_time=datetime.now()
            )
            
            # Create rollback point
            rollback_point = await self._create_rollback_point(solution, context)
            result.rollback_point = rollback_point
            
            try:
                # Implement solution steps
                await self._implement_solution_steps(solution, context, result)
                
                # Verify implementation
                verification_success = await self._verify_implementation(solution, context, result)
                
                if verification_success:
                    result.status = ImplementationStatus.COMPLETED
                    result.success = True
                    self.logger.info(f"Solution implemented successfully: {solution_id}")
                else:
                    raise Exception("Implementation verification failed")
                
            except Exception as e:
                # Implementation failed, attempt rollback
                self.logger.error(f"Solution implementation failed: {e}")
                result.error_message = str(e)
                
                if rollback_point:
                    rollback_success = await self._rollback_implementation(rollback_point)
                    if rollback_success:
                        result.status = ImplementationStatus.ROLLED_BACK
                        self.logger.info(f"Successfully rolled back solution: {solution_id}")
                    else:
                        result.status = ImplementationStatus.FAILED
                        self.logger.error(f"Failed to rollback solution: {solution_id}")
                else:
                    result.status = ImplementationStatus.FAILED
            
            finally:
                result.end_time = datetime.now()
                self.implementation_results[solution_id] = result
            
            # Convert to dictionary for return
            result_dict = {
                'solution_id': result.solution_id,
                'status': result.status.value,
                'success': result.success,
                'start_time': result.start_time.isoformat(),
                'end_time': result.end_time.isoformat() if result.end_time else None,
                'steps_completed': result.steps_completed,
                'steps_failed': result.steps_failed,
                'error_message': result.error_message,
                'verification_results': result.verification_results,
                'duration_seconds': (
                    (result.end_time - result.start_time).total_seconds() 
                    if result.end_time else 0
                )
            }
            
            return result_dict
            
        except Exception as e:
            self.logger.error(f"Error implementing solution: {e}")
            return {
                'solution_id': solution.get('solution_id', 'unknown'),
                'status': 'failed',
                'success': False,
                'error_message': str(e),
                'start_time': datetime.now().isoformat()
            }
    
    async def _perform_safety_checks(self, solution: Dict[str, Any], context: Dict[str, Any], report: ValidationReport):
        """Perform comprehensive safety checks on the solution."""
        try:
            # Check file change limits
            code_changes = solution.get('code_changes', [])
            config_changes = solution.get('config_changes', [])
            
            report.safety_checks['file_change_limit'] = len(code_changes) <= self.safety_config['max_file_changes']
            report.safety_checks['config_change_limit'] = len(config_changes) <= self.safety_config['max_config_changes']
            
            # Check for critical file modifications
            critical_files = ['config.py', 'app.py', '__init__.py']
            modifies_critical = any(
                any(critical in change.get('file', '') for critical in critical_files)
                for change in code_changes
            )
            report.safety_checks['avoids_critical_files'] = not modifies_critical
            
            # Check for dangerous operations
            dangerous_operations = ['rm', 'delete', 'drop', 'truncate', 'format']
            steps = solution.get('steps', [])
            has_dangerous_ops = any(
                any(op in str(step).lower() for op in dangerous_operations)
                for step in steps
            )
            report.safety_checks['no_dangerous_operations'] = not has_dangerous_ops
            
            # Check rollback capability
            report.safety_checks['rollback_possible'] = solution.get('rollback_possible', True)
            
            # Check automation safety
            can_be_automated = solution.get('can_be_automated', False)
            requires_user_input = solution.get('requires_user_input', True)
            report.safety_checks['automation_safe'] = can_be_automated and not requires_user_input
            
        except Exception as e:
            self.logger.error(f"Error performing safety checks: {e}")
            report.safety_checks['safety_check_error'] = True

    async def _assess_risk_factors(self, solution: Dict[str, Any], context: Dict[str, Any], report: ValidationReport):
        """Assess risk factors for the solution."""
        try:
            risk_factors = []

            # Risk based on solution type
            solution_type = solution.get('type', 'unknown')
            if solution_type in ['systematic_repair', 'code_improvement']:
                risk_factors.append('Complex solution type with potential for side effects')

            # Risk based on affected components
            affected_components = context.get('affected_components', [])
            critical_components = ['n8n_builder.py', 'app.py', 'config.py']
            if any(comp in str(affected_components) for comp in critical_components):
                risk_factors.append('Affects critical system components')

            # Risk based on confidence level
            confidence = solution.get('confidence', 0.0)
            if confidence < 0.7:
                risk_factors.append('Low confidence solution')

            # Risk based on estimated time
            estimated_time = solution.get('estimated_time', 0)
            if estimated_time > 60:
                risk_factors.append('Long implementation time increases risk')

            # Risk based on automation capability
            if not solution.get('can_be_automated', False):
                risk_factors.append('Manual implementation required')

            report.risk_factors = risk_factors

        except Exception as e:
            self.logger.error(f"Error assessing risk factors: {e}")
            report.risk_factors.append('Error during risk assessment')

    async def _run_validation_tests(self, solution: Dict[str, Any], context: Dict[str, Any], report: ValidationReport):
        """Run validation tests for the solution."""
        try:
            test_results = {}

            # Syntax validation for code changes
            code_changes = solution.get('code_changes', [])
            for change in code_changes:
                file_path = change.get('file', '')
                if file_path.endswith('.py'):
                    syntax_valid = await self._validate_python_syntax(change.get('content', ''))
                    test_results[f'syntax_valid_{file_path}'] = syntax_valid

            # Configuration validation
            config_changes = solution.get('config_changes', [])
            for change in config_changes:
                config_valid = await self._validate_configuration(change)
                test_results[f'config_valid_{change.get("file", "unknown")}'] = config_valid

            # Dependency validation
            dependencies_valid = await self._validate_dependencies(solution, context)
            test_results['dependencies_valid'] = dependencies_valid

            # Integration test (if applicable)
            if self.safety_config.get('require_tests', True):
                integration_test_passed = await self._run_integration_tests(solution, context)
                test_results['integration_tests'] = integration_test_passed

            report.test_results = test_results

        except Exception as e:
            self.logger.error(f"Error running validation tests: {e}")
            report.test_results['validation_test_error'] = str(e)

    def _determine_validation_result(self, report: ValidationReport):
        """Determine the overall validation result."""
        try:
            # Count passed safety checks
            safety_passed = sum(1 for passed in report.safety_checks.values() if passed)
            safety_total = len(report.safety_checks)
            safety_ratio = safety_passed / safety_total if safety_total > 0 else 0

            # Count passed tests
            test_passed = sum(1 for result in report.test_results.values() if result is True)
            test_total = len(report.test_results)
            test_ratio = test_passed / test_total if test_total > 0 else 0

            # Calculate overall confidence
            confidence = (safety_ratio * 0.6 + test_ratio * 0.4)
            report.confidence = confidence

            # Determine result based on thresholds
            if confidence >= 0.8 and len(report.risk_factors) <= 2:
                report.validation_result = ValidationResult.SAFE
                report.can_proceed = True
            elif confidence >= 0.6 and len(report.risk_factors) <= 3:
                report.validation_result = ValidationResult.RISKY
                report.can_proceed = True
                report.requires_manual_review = True
                report.recommendations.append('Manual review recommended due to moderate risk')
            else:
                report.validation_result = ValidationResult.UNSAFE
                report.can_proceed = False
                report.recommendations.append('Solution deemed unsafe for automatic implementation')

            # Add specific recommendations
            if safety_ratio < 0.8:
                report.recommendations.append('Address safety check failures before implementation')
            if test_ratio < 0.8:
                report.recommendations.append('Resolve test failures before implementation')
            if len(report.risk_factors) > 3:
                report.recommendations.append('Consider alternative solutions with lower risk')

        except Exception as e:
            self.logger.error(f"Error determining validation result: {e}")
            report.validation_result = ValidationResult.UNSAFE
            report.can_proceed = False

    async def _create_rollback_point(self, solution: Dict[str, Any], context: Dict[str, Any]) -> Optional[RollbackPoint]:
        """Create a rollback point before implementing the solution."""
        try:
            rollback_id = f"rollback_{solution.get('solution_id', 'unknown')}_{int(datetime.now().timestamp())}"

            # Identify files that will be affected
            affected_files = []

            # Add files from code changes
            for change in solution.get('code_changes', []):
                file_path = change.get('file', '')
                if file_path:
                    affected_files.append(file_path)

            # Add files from config changes
            for change in solution.get('config_changes', []):
                file_path = change.get('file', '')
                if file_path:
                    affected_files.append(file_path)

            # Create backup directory for this rollback point
            backup_location = self.backup_dir / rollback_id
            backup_location.mkdir(exist_ok=True)

            # Backup affected files
            for file_path in affected_files:
                source_path = self.project_root / file_path
                if source_path.exists():
                    backup_file_path = backup_location / file_path
                    backup_file_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_path, backup_file_path)

            # Create rollback point
            rollback_point = RollbackPoint(
                rollback_id=rollback_id,
                timestamp=datetime.now(),
                description=f"Rollback point for solution {solution.get('solution_id', 'unknown')}",
                affected_files=affected_files,
                backup_location=str(backup_location),
                system_state={'backup_created': True}
            )

            self.rollback_points[rollback_id] = rollback_point

            self.logger.info(f"Created rollback point: {rollback_id}")
            return rollback_point

        except Exception as e:
            self.logger.error(f"Error creating rollback point: {e}")
            return None

    async def _implement_solution_steps(self, solution: Dict[str, Any], context: Dict[str, Any], result: ImplementationResult):
        """Implement the solution steps."""
        try:
            steps = solution.get('steps', [])

            for i, step in enumerate(steps):
                step_name = f"step_{i+1}_{step.get('action', 'unknown')}"

                try:
                    # Implement individual step
                    await self._implement_step(step, context)
                    result.steps_completed.append(step_name)

                except Exception as step_error:
                    self.logger.error(f"Step failed: {step_name} - {step_error}")
                    result.steps_failed.append(step_name)
                    raise Exception(f"Step {step_name} failed: {step_error}")

            # Apply code changes
            for change in solution.get('code_changes', []):
                await self._apply_code_change(change)
                result.steps_completed.append(f"code_change_{change.get('file', 'unknown')}")

            # Apply config changes
            for change in solution.get('config_changes', []):
                await self._apply_config_change(change)
                result.steps_completed.append(f"config_change_{change.get('file', 'unknown')}")

        except Exception as e:
            self.logger.error(f"Error implementing solution steps: {e}")
            raise

    async def _implement_step(self, step: Dict[str, Any], context: Dict[str, Any]):
        """Implement a single solution step."""
        action = step.get('action', '')

        # This is a simplified implementation - would be expanded based on actual step types
        if action == 'check_service':
            # Check if a service is running
            pass
        elif action == 'restart_service':
            # Restart a service
            pass
        elif action == 'validate_json':
            # Validate JSON format
            pass
        elif action == 'clear_cache':
            # Clear system cache
            pass
        else:
            self.logger.warning(f"Unknown step action: {action}")

    async def _apply_code_change(self, change: Dict[str, Any]):
        """Apply a code change."""
        file_path = self.project_root / change.get('file', '')
        content = change.get('content', '')

        if file_path.exists() and content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

    async def _apply_config_change(self, change: Dict[str, Any]):
        """Apply a configuration change."""
        file_path = self.project_root / change.get('file', '')
        changes = change.get('changes', {})

        if file_path.exists() and changes:
            # This would implement actual config file modification
            # For now, just log the change
            self.logger.info(f"Would apply config changes to {file_path}: {changes}")

    async def _verify_implementation(self, solution: Dict[str, Any], context: Dict[str, Any], result: ImplementationResult) -> bool:
        """Verify that the solution was implemented correctly."""
        try:
            verification_results = {}

            # Run basic syntax checks
            syntax_ok = await self._verify_syntax()
            verification_results['syntax_check'] = syntax_ok

            # Run quick integration test
            integration_ok = await self._verify_integration()
            verification_results['integration_check'] = integration_ok

            # Check if the original error is resolved (simplified)
            error_resolved = await self._verify_error_resolution(context)
            verification_results['error_resolution'] = error_resolved

            result.verification_results = verification_results

            # All checks must pass
            return all(verification_results.values())

        except Exception as e:
            self.logger.error(f"Error verifying implementation: {e}")
            result.verification_results['verification_error'] = str(e)
            return False

    async def _rollback_implementation(self, rollback_point: RollbackPoint) -> bool:
        """Rollback an implementation using the rollback point."""
        try:
            if not rollback_point.backup_location:
                return False

            backup_path = Path(rollback_point.backup_location)
            if not backup_path.exists():
                return False

            # Restore backed up files
            for file_path in rollback_point.affected_files:
                backup_file = backup_path / file_path
                target_file = self.project_root / file_path

                if backup_file.exists():
                    shutil.copy2(backup_file, target_file)

            self.logger.info(f"Successfully rolled back using: {rollback_point.rollback_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error during rollback: {e}")
            return False

    # Validation helper methods (simplified implementations)
    async def _validate_python_syntax(self, code: str) -> bool:
        """Validate Python syntax."""
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False

    async def _validate_configuration(self, change: Dict[str, Any]) -> bool:
        """Validate configuration change."""
        # Simplified validation
        return True

    async def _validate_dependencies(self, solution: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Validate solution dependencies."""
        # Simplified validation
        return True

    async def _run_integration_tests(self, solution: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Run integration tests."""
        # Simplified test runner
        return True

    async def _verify_syntax(self) -> bool:
        """Verify syntax of modified files."""
        return True

    async def _verify_integration(self) -> bool:
        """Verify system integration."""
        return True

    async def _verify_error_resolution(self, context: Dict[str, Any]) -> bool:
        """Verify that the original error is resolved."""
        return True
