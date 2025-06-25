"""
Self-Healer Manager - Main orchestrator for the self-healing system.

This module coordinates all self-healing activities including error detection,
analysis, solution generation, validation, and implementation.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
import json

# Import self-healer components
from .project_adapter import ProjectAdapter
from .error_monitor import ErrorMonitor
from .context_analyzer import ContextAnalyzer
from .solution_generator import SolutionGenerator
from .solution_validator import SolutionValidator
from .learning_engine import LearningEngine


class HealingStatus(Enum):
    """Status of healing operations."""
    IDLE = "idle"
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    GENERATING_SOLUTION = "generating_solution"
    VALIDATING = "validating"
    IMPLEMENTING = "implementing"
    LEARNING = "learning"
    ERROR = "error"


@dataclass
class HealingSession:
    """Represents a complete healing session for an error."""
    session_id: str
    error_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    status: HealingStatus = HealingStatus.MONITORING
    error_detail: Optional[ErrorDetail] = None
    context: Optional[Dict[str, Any]] = None
    solutions: List[Dict[str, Any]] = field(default_factory=list)
    selected_solution: Optional[Dict[str, Any]] = None
    validation_results: Optional[Dict[str, Any]] = None
    implementation_results: Optional[Dict[str, Any]] = None
    success: bool = False
    error_message: Optional[str] = None
    learning_feedback: Optional[Dict[str, Any]] = None


class SelfHealerManager:
    """
    Main orchestrator for the self-healing system.
    
    Coordinates error detection, analysis, solution generation, validation,
    and implementation while maintaining safety and learning capabilities.
    """
    
    def __init__(self, config_path: Optional[Path] = None, project_config_path: Optional[Path] = None):
        """Initialize the Self-Healer Manager."""
        # Initialize project adapter first
        self.project_adapter = ProjectAdapter(project_config_path)
        self.logger = self.project_adapter.get_logger('self_healer.manager')

        self.config_path = config_path or Path(__file__).parent.parent / "config" / "healer_config.yaml"

        # Initialize components with project adapter
        self.error_monitor = ErrorMonitor(self.project_adapter)
        self.context_analyzer = ContextAnalyzer(self.project_adapter)
        self.solution_generator = SolutionGenerator(self.project_adapter)
        self.solution_validator = SolutionValidator(self.project_adapter)
        self.learning_engine = LearningEngine(self.project_adapter)
        
        # State management
        self.status = HealingStatus.IDLE
        self.active_sessions: Dict[str, HealingSession] = {}
        self.session_history: List[HealingSession] = []
        self.is_running = False
        self.tasks: List[asyncio.Task] = []
        
        # Configuration
        self.config = self._load_config()
        
        # Metrics
        self.metrics = {
            'total_errors_detected': 0,
            'total_healing_attempts': 0,
            'successful_healings': 0,
            'failed_healings': 0,
            'average_healing_time': 0.0,
            'uptime_start': datetime.now()
        }
        
        self.logger.info("Self-Healer Manager initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        default_config = {
            'monitoring': {
                'check_interval': 5.0,  # seconds
                'max_concurrent_sessions': 3,
                'error_cooldown': 300,  # seconds before re-processing same error
            },
            'safety': {
                'max_healing_attempts_per_hour': 10,
                'require_validation': True,
                'auto_rollback_on_failure': True,
                'emergency_stop_threshold': 5  # consecutive failures
            },
            'learning': {
                'enable_learning': True,
                'feedback_collection': True,
                'pattern_analysis': True
            }
        }
        
        if self.config_path.exists():
            try:
                import yaml
                with open(self.config_path, 'r') as f:
                    file_config = yaml.safe_load(f)
                    default_config.update(file_config)
            except Exception as e:
                self.logger.warning(f"Could not load config file: {e}, using defaults")
        
        return default_config
    
    async def start(self):
        """Start the self-healing system."""
        if self.is_running:
            self.logger.warning("Self-Healer is already running")
            return
        
        self.is_running = True
        self.status = HealingStatus.MONITORING
        
        # Start component services
        await self.error_monitor.start()
        await self.context_analyzer.start()
        await self.solution_generator.start()
        await self.solution_validator.start()
        await self.learning_engine.start()
        
        # Start main monitoring loop
        self.tasks = [
            asyncio.create_task(self._monitoring_loop()),
            asyncio.create_task(self._metrics_collection_loop()),
            asyncio.create_task(self._cleanup_loop())
        ]
        
        self.logger.info("Self-Healer Manager started successfully")
    
    async def stop(self):
        """Stop the self-healing system."""
        if not self.is_running:
            return
        
        self.is_running = False
        self.status = HealingStatus.IDLE
        
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        # Stop component services
        await self.error_monitor.stop()
        await self.context_analyzer.stop()
        await self.solution_generator.stop()
        await self.solution_validator.stop()
        await self.learning_engine.stop()
        
        # Complete any active sessions
        for session in self.active_sessions.values():
            session.status = HealingStatus.ERROR
            session.error_message = "System shutdown"
            session.end_time = datetime.now()
            self.session_history.append(session)
        
        self.active_sessions.clear()
        self.logger.info("Self-Healer Manager stopped")
    
    async def _monitoring_loop(self):
        """Main monitoring loop that processes detected errors."""
        while self.is_running:
            try:
                # Check for new errors
                new_errors = await self.error_monitor.get_new_errors()
                
                for error in new_errors:
                    if self._should_process_error(error):
                        await self._initiate_healing_session(error)
                
                # Process active sessions
                await self._process_active_sessions()
                
                # Wait before next check
                await asyncio.sleep(self.config['monitoring']['check_interval'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(1)  # Brief pause on error
    
    def _should_process_error(self, error: ErrorDetail) -> bool:
        """Determine if an error should be processed for healing."""
        # Check if we're already processing this error
        for session in self.active_sessions.values():
            if session.error_id == error.error_id:
                return False
        
        # Check cooldown period
        cooldown = self.config['monitoring']['error_cooldown']
        cutoff_time = datetime.now() - timedelta(seconds=cooldown)
        
        for session in self.session_history:
            if (session.error_id == error.error_id and 
                session.end_time and session.end_time > cutoff_time):
                return False
        
        # Check concurrent session limit
        max_concurrent = self.config['monitoring']['max_concurrent_sessions']
        if len(self.active_sessions) >= max_concurrent:
            return False
        
        return True
    
    async def _initiate_healing_session(self, error: ErrorDetail):
        """Start a new healing session for an error."""
        session_id = f"heal_{int(time.time() * 1000)}"
        session = HealingSession(
            session_id=session_id,
            error_id=error.error_id,
            start_time=datetime.now(),
            error_detail=error
        )
        
        self.active_sessions[session_id] = session
        self.metrics['total_errors_detected'] += 1
        self.metrics['total_healing_attempts'] += 1
        
        self.logger.info(f"Initiated healing session {session_id} for error {error.error_id}")
        
        # Start processing in background
        asyncio.create_task(self._process_healing_session(session))
    
    async def get_status(self) -> Dict[str, Any]:
        """Get current system status and metrics."""
        uptime = datetime.now() - self.metrics['uptime_start']

        return {
            'status': self.status.value,
            'is_running': self.is_running,
            'active_sessions': len(self.active_sessions),
            'metrics': {
                **self.metrics,
                'uptime_seconds': uptime.total_seconds(),
                'success_rate': (
                    self.metrics['successful_healings'] /
                    max(1, self.metrics['total_healing_attempts'])
                ) * 100
            },
            'recent_sessions': [
                {
                    'session_id': s.session_id,
                    'error_id': s.error_id,
                    'status': s.status.value,
                    'success': s.success,
                    'duration': (
                        (s.end_time or datetime.now()) - s.start_time
                    ).total_seconds()
                }
                for s in self.session_history[-10:]  # Last 10 sessions
            ]
        }

    async def _process_healing_session(self, session: HealingSession):
        """Process a complete healing session from analysis to implementation."""
        try:
            # Phase 1: Context Analysis
            session.status = HealingStatus.ANALYZING
            self.logger.info(f"Analyzing context for session {session.session_id}")

            session.context = await self.context_analyzer.analyze_error(session.error_detail)

            # Phase 2: Solution Generation
            session.status = HealingStatus.GENERATING_SOLUTION
            self.logger.info(f"Generating solutions for session {session.session_id}")

            session.solutions = await self.solution_generator.generate_solutions(
                session.error_detail, session.context
            )

            if not session.solutions:
                raise Exception("No solutions generated")

            # Phase 3: Solution Validation
            session.status = HealingStatus.VALIDATING
            self.logger.info(f"Validating solutions for session {session.session_id}")

            best_solution = None
            for solution in session.solutions:
                validation_result = await self.solution_validator.validate_solution(
                    solution, session.context
                )
                solution['validation'] = validation_result

                if validation_result.get('is_safe', False) and validation_result.get('confidence', 0) > 0.7:
                    best_solution = solution
                    break

            if not best_solution:
                raise Exception("No safe solutions found")

            session.selected_solution = best_solution
            session.validation_results = best_solution['validation']

            # Phase 4: Implementation
            session.status = HealingStatus.IMPLEMENTING
            self.logger.info(f"Implementing solution for session {session.session_id}")

            session.implementation_results = await self.solution_validator.implement_solution(
                best_solution, session.context
            )

            # Phase 5: Learning
            session.status = HealingStatus.LEARNING
            session.success = session.implementation_results.get('success', False)

            session.learning_feedback = await self.learning_engine.record_healing_result(
                session.error_detail, session.context, best_solution,
                session.implementation_results
            )

            if session.success:
                self.metrics['successful_healings'] += 1
                self.logger.info(f"Healing session {session.session_id} completed successfully")
            else:
                self.metrics['failed_healings'] += 1
                self.logger.warning(f"Healing session {session.session_id} failed")

        except Exception as e:
            session.status = HealingStatus.ERROR
            session.error_message = str(e)
            session.success = False
            self.metrics['failed_healings'] += 1
            self.logger.error(f"Healing session {session.session_id} failed: {e}")

        finally:
            # Complete session
            session.end_time = datetime.now()
            duration = (session.end_time - session.start_time).total_seconds()

            # Update average healing time
            total_sessions = len(self.session_history) + 1
            current_avg = self.metrics['average_healing_time']
            self.metrics['average_healing_time'] = (
                (current_avg * (total_sessions - 1) + duration) / total_sessions
            )

            # Move to history
            self.session_history.append(session)
            if session.session_id in self.active_sessions:
                del self.active_sessions[session.session_id]

    async def _process_active_sessions(self):
        """Check and manage active healing sessions."""
        current_time = datetime.now()
        timeout_threshold = timedelta(minutes=30)  # 30 minute timeout

        timed_out_sessions = []
        for session_id, session in self.active_sessions.items():
            if current_time - session.start_time > timeout_threshold:
                timed_out_sessions.append(session_id)

        # Handle timed out sessions
        for session_id in timed_out_sessions:
            session = self.active_sessions[session_id]
            session.status = HealingStatus.ERROR
            session.error_message = "Session timeout"
            session.end_time = current_time
            session.success = False

            self.session_history.append(session)
            del self.active_sessions[session_id]

            self.logger.warning(f"Healing session {session_id} timed out")

    async def _metrics_collection_loop(self):
        """Collect and update system metrics."""
        while self.is_running:
            try:
                # Update component metrics
                await self._update_component_metrics()
                await asyncio.sleep(60)  # Update every minute

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in metrics collection: {e}")
                await asyncio.sleep(5)

    async def _cleanup_loop(self):
        """Periodic cleanup of old data."""
        while self.is_running:
            try:
                # Clean up old session history (keep last 1000)
                if len(self.session_history) > 1000:
                    self.session_history = self.session_history[-1000:]

                await asyncio.sleep(3600)  # Cleanup every hour

            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup loop: {e}")
                await asyncio.sleep(60)

    async def _update_component_metrics(self):
        """Update metrics from all components."""
        try:
            # This would collect metrics from each component
            # Implementation depends on what metrics each component provides
            pass
        except Exception as e:
            self.logger.error(f"Error updating component metrics: {e}")

    async def emergency_stop(self):
        """Emergency stop for critical situations."""
        self.logger.critical("Emergency stop activated")
        await self.stop()

    def get_session_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific session."""
        # Check active sessions first
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
        else:
            # Check history
            session = next((s for s in self.session_history if s.session_id == session_id), None)

        if not session:
            return None

        return {
            'session_id': session.session_id,
            'error_id': session.error_id,
            'start_time': session.start_time.isoformat(),
            'end_time': session.end_time.isoformat() if session.end_time else None,
            'status': session.status.value,
            'success': session.success,
            'error_detail': session.error_detail.__dict__ if session.error_detail else None,
            'context': session.context,
            'solutions': session.solutions,
            'selected_solution': session.selected_solution,
            'validation_results': session.validation_results,
            'implementation_results': session.implementation_results,
            'error_message': session.error_message,
            'learning_feedback': session.learning_feedback
        }
