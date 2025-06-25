"""
Generic Types - Common data structures for the Self-Healer system.

This module provides generic data structures that work across different projects
without dependencies on specific project implementations.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class ErrorCategory(Enum):
    """Generic error categories."""
    GENERAL = "general"
    SYSTEM = "system"
    NETWORK = "network"
    FILE_SYSTEM = "file_system"
    CONFIGURATION = "configuration"
    DEPENDENCY = "dependency"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATA = "data"
    INTEGRATION = "integration"


class ErrorSeverity(Enum):
    """Error severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class GenericErrorDetail:
    """Generic error detail structure that works with any project."""
    # Core error information
    error_id: str
    title: str
    message: str
    category: ErrorCategory = ErrorCategory.GENERAL
    severity: ErrorSeverity = ErrorSeverity.ERROR
    
    # Additional information
    technical_details: Optional[str] = None
    user_guidance: Optional[str] = None
    fix_suggestions: List[str] = field(default_factory=list)
    documentation_links: List[str] = field(default_factory=list)
    
    # Context and metadata
    context: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    source_file: Optional[str] = None
    line_number: Optional[int] = None
    
    # Project-specific fields
    original_error: Optional[Any] = None  # Store original project error object
    project_category: Optional[str] = None  # Project-specific category
    project_severity: Optional[str] = None  # Project-specific severity


@dataclass
class GenericLogEntry:
    """Generic log entry structure."""
    timestamp: datetime
    level: str
    message: str
    logger_name: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    function_name: Optional[str] = None
    thread_id: Optional[str] = None
    process_id: Optional[str] = None
    extra_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenericFileInfo:
    """Generic file information structure."""
    path: str
    file_type: str
    size_bytes: int
    last_modified: datetime
    is_critical: bool = False
    is_config: bool = False
    is_executable: bool = False
    permissions: Optional[str] = None
    encoding: Optional[str] = None


@dataclass
class GenericProjectInfo:
    """Generic project information structure."""
    name: str
    version: str
    description: str
    root_path: str
    language: Optional[str] = None
    framework: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    config_files: List[str] = field(default_factory=list)
    entry_points: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class SolutionType(Enum):
    """Types of solutions that can be generated."""
    IMMEDIATE_FIX = "immediate_fix"
    SYSTEMATIC_REPAIR = "systematic_repair"
    PREVENTIVE_MEASURE = "preventive_measure"
    CONFIGURATION_CHANGE = "configuration_change"
    CODE_IMPROVEMENT = "code_improvement"
    DEPENDENCY_UPDATE = "dependency_update"
    ENVIRONMENT_FIX = "environment_fix"


class SolutionPriority(Enum):
    """Priority levels for solutions."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class GenericSolution:
    """Generic solution structure."""
    solution_id: str
    title: str
    description: str
    solution_type: SolutionType
    priority: SolutionPriority
    
    # Implementation details
    steps: List[Dict[str, Any]] = field(default_factory=list)
    code_changes: List[Dict[str, Any]] = field(default_factory=list)
    config_changes: List[Dict[str, Any]] = field(default_factory=list)
    file_operations: List[Dict[str, Any]] = field(default_factory=list)
    commands: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    confidence: float = 0.0
    estimated_time_minutes: int = 0
    risk_level: str = "medium"
    prerequisites: List[str] = field(default_factory=list)
    
    # Validation info
    can_be_automated: bool = False
    requires_user_input: bool = False
    rollback_possible: bool = True
    
    # Context
    applicable_errors: List[str] = field(default_factory=list)
    related_components: List[str] = field(default_factory=list)
    
    # Internal
    ranking_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class GenericValidationResult:
    """Generic validation result structure."""
    solution_id: str
    is_valid: bool
    is_safe: bool
    confidence: float
    
    # Validation details
    safety_checks: Dict[str, bool] = field(default_factory=dict)
    test_results: Dict[str, Any] = field(default_factory=dict)
    risk_factors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    # Recommendations
    can_proceed: bool = False
    requires_manual_review: bool = False
    recommendations: List[str] = field(default_factory=list)
    
    # Metadata
    validation_time: datetime = field(default_factory=datetime.now)
    validator_version: Optional[str] = None


@dataclass
class GenericImplementationResult:
    """Generic implementation result structure."""
    solution_id: str
    success: bool
    start_time: datetime
    end_time: Optional[datetime] = None
    
    # Implementation details
    steps_completed: List[str] = field(default_factory=list)
    steps_failed: List[str] = field(default_factory=list)
    files_modified: List[str] = field(default_factory=list)
    commands_executed: List[str] = field(default_factory=list)
    
    # Results
    error_message: Optional[str] = None
    rollback_performed: bool = False
    rollback_successful: bool = False
    verification_results: Dict[str, Any] = field(default_factory=dict)
    
    # Metadata
    implementation_log: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class GenericLearningRecord:
    """Generic learning record structure."""
    record_id: str
    timestamp: datetime
    
    # Error information
    error_category: str
    error_severity: str
    error_keywords: List[str] = field(default_factory=list)
    
    # Solution information
    solution_type: str
    solution_confidence: float
    solution_steps: List[str] = field(default_factory=list)
    
    # Context information
    affected_components: List[str] = field(default_factory=list)
    system_state: Dict[str, Any] = field(default_factory=dict)
    
    # Outcome information
    success: bool = False
    implementation_time: float = 0.0
    verification_results: Dict[str, Any] = field(default_factory=dict)
    
    # Learning metadata
    pattern_matches: List[str] = field(default_factory=list)
    effectiveness_score: float = 0.0
    feedback: Optional[str] = None


@dataclass
class GenericPattern:
    """Generic pattern structure for learning."""
    pattern_id: str
    pattern_type: str
    
    # Pattern definition
    conditions: Dict[str, Any] = field(default_factory=dict)
    triggers: List[str] = field(default_factory=list)
    
    # Pattern statistics
    occurrence_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    average_effectiveness: float = 0.0
    
    # Pattern metadata
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    confidence: float = 0.0
    tags: List[str] = field(default_factory=list)


@dataclass
class GenericInsight:
    """Generic insight structure."""
    insight_id: str
    insight_type: str
    title: str
    description: str
    
    # Supporting data
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0
    impact_level: str = 'medium'
    
    # Actionable recommendations
    recommendations: List[str] = field(default_factory=list)
    priority: int = 5
    
    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    category: Optional[str] = None
    tags: List[str] = field(default_factory=list)


def convert_project_error_to_generic(project_error: Any, project_adapter: Any) -> GenericErrorDetail:
    """Convert a project-specific error to generic error detail."""
    try:
        # Try to extract information from project error
        if hasattr(project_error, 'title'):
            title = project_error.title
        elif hasattr(project_error, 'message'):
            title = project_error.message[:100]  # First 100 chars as title
        else:
            title = str(project_error)[:100]
        
        if hasattr(project_error, 'message'):
            message = project_error.message
        else:
            message = str(project_error)
        
        # Map project categories to generic categories
        category = ErrorCategory.GENERAL
        if hasattr(project_error, 'category'):
            category_mapping = {
                'llm_communication': ErrorCategory.NETWORK,
                'json_parsing': ErrorCategory.DATA,
                'workflow_structure': ErrorCategory.CONFIGURATION,
                'performance': ErrorCategory.PERFORMANCE,
                'system': ErrorCategory.SYSTEM,
                'file_operations': ErrorCategory.FILE_SYSTEM,
                'network': ErrorCategory.NETWORK,
                'security': ErrorCategory.SECURITY
            }
            project_category = str(project_error.category).lower()
            category = category_mapping.get(project_category, ErrorCategory.GENERAL)
        
        # Map project severity to generic severity
        severity = ErrorSeverity.ERROR
        if hasattr(project_error, 'severity'):
            severity_mapping = {
                'info': ErrorSeverity.INFO,
                'warning': ErrorSeverity.WARNING,
                'error': ErrorSeverity.ERROR,
                'critical': ErrorSeverity.CRITICAL
            }
            project_severity = str(project_error.severity).lower()
            severity = severity_mapping.get(project_severity, ErrorSeverity.ERROR)
        
        # Extract additional information
        technical_details = getattr(project_error, 'technical_details', None)
        user_guidance = getattr(project_error, 'user_guidance', None)
        fix_suggestions = getattr(project_error, 'fix_suggestions', [])
        context = getattr(project_error, 'context', {})
        
        # Generate error ID
        import hashlib
        error_content = f"{title}:{message}"
        error_id = hashlib.md5(error_content.encode()).hexdigest()[:16]
        
        return GenericErrorDetail(
            error_id=error_id,
            title=title,
            message=message,
            category=category,
            severity=severity,
            technical_details=technical_details,
            user_guidance=user_guidance,
            fix_suggestions=fix_suggestions or [],
            context=context or {},
            original_error=project_error,
            project_category=getattr(project_error, 'category', None),
            project_severity=getattr(project_error, 'severity', None)
        )
        
    except Exception as e:
        # Fallback for any conversion errors
        return GenericErrorDetail(
            error_id="conversion_error",
            title="Error Conversion Failed",
            message=f"Failed to convert project error: {str(e)}",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.ERROR,
            original_error=project_error
        )
