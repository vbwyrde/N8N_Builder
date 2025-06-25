"""
Error Monitor - Detects and classifies errors from log files and system state.

This module continuously monitors error logs and system state to detect issues
that require healing intervention.
"""

import asyncio
import logging
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Any
from pathlib import Path
from dataclasses import dataclass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re

# Import existing N8N Builder components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.error_handler import EnhancedErrorHandler, ErrorDetail
from n8n_builder.logging_config import get_logger


@dataclass
class DetectedError:
    """Represents a detected error with metadata."""
    error_id: str
    timestamp: datetime
    log_file: str
    line_number: int
    raw_message: str
    error_detail: ErrorDetail
    severity: str
    category: str
    frequency: int = 1
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None


class LogFileHandler(FileSystemEventHandler):
    """Handles file system events for log files."""
    
    def __init__(self, error_monitor):
        self.error_monitor = error_monitor
        self.logger = get_logger('self_healer.log_handler')
    
    def on_modified(self, event):
        """Handle file modification events."""
        if not event.is_directory and event.src_path.endswith('.log'):
            asyncio.create_task(self.error_monitor._process_log_file_change(event.src_path))


class ErrorMonitor:
    """
    Monitors error logs and system state for issues requiring healing.
    
    Features:
    - Real-time log file monitoring
    - Error classification and deduplication
    - Pattern recognition for recurring issues
    - Integration with existing error handling
    """
    
    def __init__(self, log_directory: Optional[Path] = None):
        """Initialize the Error Monitor."""
        self.logger = get_logger('self_healer.error_monitor')
        
        # Configuration
        self.log_directory = log_directory or Path(__file__).parent.parent.parent / "logs"
        self.error_log_path = self.log_directory / "errors.log"
        self.main_log_path = self.log_directory / "n8n_builder.log"
        
        # Error handling
        self.error_handler = EnhancedErrorHandler()
        
        # State tracking
        self.detected_errors: Dict[str, DetectedError] = {}
        self.processed_lines: Dict[str, int] = {}  # Track last processed line per file
        self.error_patterns: Dict[str, re.Pattern] = {}
        self.is_running = False
        
        # File system monitoring
        self.observer = Observer()
        self.file_handler = LogFileHandler(self)
        
        # Error processing queue
        self.error_queue: asyncio.Queue = asyncio.Queue()
        self.processing_task: Optional[asyncio.Task] = None
        
        # Load error patterns
        self._load_error_patterns()
        
        self.logger.info("Error Monitor initialized")
    
    def _load_error_patterns(self):
        """Load error detection patterns."""
        # Common error patterns for log parsing
        self.error_patterns = {
            'python_exception': re.compile(r'ERROR.*?(?:Exception|Error):\s*(.+)', re.IGNORECASE),
            'llm_failure': re.compile(r'ERROR.*?LLM.*?(?:failed|error|crashed):\s*(.+)', re.IGNORECASE),
            'connection_error': re.compile(r'ERROR.*?(?:connection|network).*?(?:failed|refused|timeout):\s*(.+)', re.IGNORECASE),
            'validation_error': re.compile(r'ERROR.*?validation.*?failed:\s*(.+)', re.IGNORECASE),
            'file_error': re.compile(r'ERROR.*?(?:file|path).*?(?:not found|permission|access):\s*(.+)', re.IGNORECASE),
            'memory_error': re.compile(r'ERROR.*?(?:memory|out of memory|allocation):\s*(.+)', re.IGNORECASE),
            'timeout_error': re.compile(r'ERROR.*?timeout:\s*(.+)', re.IGNORECASE),
            'critical_error': re.compile(r'CRITICAL.*?:\s*(.+)', re.IGNORECASE)
        }
        
        self.logger.debug(f"Loaded {len(self.error_patterns)} error patterns")
    
    async def start(self):
        """Start the error monitoring system."""
        if self.is_running:
            self.logger.warning("Error Monitor is already running")
            return
        
        self.is_running = True
        
        # Ensure log directory exists
        self.log_directory.mkdir(exist_ok=True)
        
        # Initialize file tracking
        await self._initialize_file_tracking()
        
        # Start file system monitoring
        self.observer.schedule(self.file_handler, str(self.log_directory), recursive=False)
        self.observer.start()
        
        # Start error processing task
        self.processing_task = asyncio.create_task(self._process_error_queue())
        
        # Initial scan of existing log files
        await self._scan_existing_logs()
        
        self.logger.info("Error Monitor started successfully")
    
    async def stop(self):
        """Stop the error monitoring system."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stop file system monitoring
        self.observer.stop()
        self.observer.join()
        
        # Stop processing task
        if self.processing_task:
            self.processing_task.cancel()
            try:
                await self.processing_task
            except asyncio.CancelledError:
                pass
        
        self.logger.info("Error Monitor stopped")
    
    async def _initialize_file_tracking(self):
        """Initialize tracking of log files."""
        for log_file in [self.error_log_path, self.main_log_path]:
            if log_file.exists():
                # Start tracking from end of file to avoid processing old errors
                with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    self.processed_lines[str(log_file)] = len(lines)
            else:
                self.processed_lines[str(log_file)] = 0
    
    async def _scan_existing_logs(self):
        """Scan existing log files for recent errors."""
        # Only scan recent entries (last hour) to avoid overwhelming the system
        cutoff_time = datetime.now() - timedelta(hours=1)
        
        for log_file in [self.error_log_path, self.main_log_path]:
            if log_file.exists():
                await self._process_log_file(str(log_file), recent_only=True, cutoff_time=cutoff_time)
    
    async def _process_log_file_change(self, file_path: str):
        """Process changes to a log file."""
        await self._process_log_file(file_path)
    
    async def _process_log_file(self, file_path: str, recent_only: bool = False, cutoff_time: Optional[datetime] = None):
        """Process a log file for new errors."""
        try:
            if not Path(file_path).exists():
                return
            
            last_processed = self.processed_lines.get(file_path, 0)
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
                # Process only new lines
                new_lines = lines[last_processed:]
                
                for i, line in enumerate(new_lines):
                    line_number = last_processed + i + 1
                    
                    # Extract timestamp if available
                    timestamp = self._extract_timestamp(line)
                    
                    # Skip old entries if recent_only is True
                    if recent_only and cutoff_time and timestamp and timestamp < cutoff_time:
                        continue
                    
                    # Check if line contains an error
                    error_info = self._parse_error_line(line, file_path, line_number, timestamp)
                    if error_info:
                        await self.error_queue.put(error_info)
                
                # Update processed line count
                self.processed_lines[file_path] = len(lines)
                
        except Exception as e:
            self.logger.error(f"Error processing log file {file_path}: {e}")
    
    def _extract_timestamp(self, line: str) -> Optional[datetime]:
        """Extract timestamp from log line."""
        # Common timestamp patterns
        timestamp_patterns = [
            r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',  # YYYY-MM-DD HH:MM:SS
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',  # ISO format
        ]
        
        for pattern in timestamp_patterns:
            match = re.search(pattern, line)
            if match:
                try:
                    timestamp_str = match.group(1)
                    # Try different formats
                    for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
                        try:
                            return datetime.strptime(timestamp_str, fmt)
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        return datetime.now()  # Fallback to current time
    
    def _parse_error_line(self, line: str, file_path: str, line_number: int, timestamp: datetime) -> Optional[Dict[str, Any]]:
        """Parse a log line to detect errors."""
        line = line.strip()
        if not line:
            return None
        
        # Check each error pattern
        for pattern_name, pattern in self.error_patterns.items():
            match = pattern.search(line)
            if match:
                error_message = match.group(1) if match.groups() else line
                
                # Create error ID based on content
                error_content = f"{pattern_name}:{error_message}"
                error_id = hashlib.md5(error_content.encode()).hexdigest()[:16]
                
                return {
                    'error_id': error_id,
                    'timestamp': timestamp,
                    'log_file': file_path,
                    'line_number': line_number,
                    'raw_message': line,
                    'error_message': error_message,
                    'pattern_name': pattern_name,
                    'severity': self._determine_severity(line, pattern_name)
                }
        
        return None
    
    def _determine_severity(self, line: str, pattern_name: str) -> str:
        """Determine error severity based on content."""
        line_lower = line.lower()

        if 'critical' in line_lower or pattern_name == 'critical_error':
            return 'CRITICAL'
        elif 'error' in line_lower:
            return 'ERROR'
        elif 'warning' in line_lower:
            return 'WARNING'
        else:
            return 'INFO'

    async def _process_error_queue(self):
        """Process detected errors from the queue."""
        while self.is_running:
            try:
                # Wait for new error with timeout
                error_info = await asyncio.wait_for(self.error_queue.get(), timeout=1.0)
                await self._process_detected_error(error_info)

            except asyncio.TimeoutError:
                continue  # Normal timeout, continue monitoring
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing error queue: {e}")
                await asyncio.sleep(1)

    async def _process_detected_error(self, error_info: Dict[str, Any]):
        """Process a detected error and create ErrorDetail."""
        try:
            error_id = error_info['error_id']

            # Check if we've seen this error before
            if error_id in self.detected_errors:
                # Update existing error
                existing_error = self.detected_errors[error_id]
                existing_error.frequency += 1
                existing_error.last_seen = error_info['timestamp']

                # Only re-process if it's been a while since last occurrence
                if existing_error.last_seen:
                    time_since_last = datetime.now() - existing_error.last_seen
                    if time_since_last.total_seconds() < 300:  # 5 minutes cooldown
                        return
            else:
                # Create new error entry
                # Create a mock exception for error handler
                mock_exception = Exception(error_info['error_message'])

                # Use existing error handler to categorize
                error_detail = self.error_handler.categorize_error(
                    mock_exception,
                    {
                        'log_file': error_info['log_file'],
                        'line_number': error_info['line_number'],
                        'pattern': error_info['pattern_name'],
                        'raw_message': error_info['raw_message'],
                        'error_id': error_id,  # Store error_id in context
                        'detected_severity': error_info['severity']
                    }
                )

                detected_error = DetectedError(
                    error_id=error_id,
                    timestamp=error_info['timestamp'],
                    log_file=error_info['log_file'],
                    line_number=error_info['line_number'],
                    raw_message=error_info['raw_message'],
                    error_detail=error_detail,
                    severity=error_info['severity'],
                    category=error_info['pattern_name'],
                    first_seen=error_info['timestamp'],
                    last_seen=error_info['timestamp']
                )

                self.detected_errors[error_id] = detected_error

                self.logger.info(f"New error detected: {error_id} - {error_detail.title}")

        except Exception as e:
            self.logger.error(f"Error processing detected error: {e}")

    async def get_new_errors(self) -> List[ErrorDetail]:
        """Get list of new errors that need healing attention."""
        new_errors = []
        current_time = datetime.now()

        for error_id, detected_error in self.detected_errors.items():
            # Consider error "new" if:
            # 1. It's recent (within last hour)
            # 2. It's recurring (frequency > 1 and recent)
            # 3. It's critical severity

            time_since_detection = current_time - detected_error.timestamp
            is_recent = time_since_detection.total_seconds() < 3600  # 1 hour
            is_recurring = detected_error.frequency > 1
            is_critical = detected_error.severity in ['CRITICAL', 'ERROR']

            if (is_recent and is_critical) or (is_recurring and is_recent):
                new_errors.append(detected_error.error_detail)

        return new_errors

    def get_error_statistics(self) -> Dict[str, Any]:
        """Get statistics about detected errors."""
        total_errors = len(self.detected_errors)
        if total_errors == 0:
            return {
                'total_errors': 0,
                'by_severity': {},
                'by_category': {},
                'recent_errors': 0,
                'recurring_errors': 0
            }

        # Count by severity
        severity_counts = {}
        category_counts = {}
        recent_count = 0
        recurring_count = 0

        current_time = datetime.now()

        for detected_error in self.detected_errors.values():
            # Severity counts
            severity = detected_error.severity
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

            # Category counts
            category = detected_error.category
            category_counts[category] = category_counts.get(category, 0) + 1

            # Recent errors (last hour)
            time_since = current_time - detected_error.timestamp
            if time_since.total_seconds() < 3600:
                recent_count += 1

            # Recurring errors
            if detected_error.frequency > 1:
                recurring_count += 1

        return {
            'total_errors': total_errors,
            'by_severity': severity_counts,
            'by_category': category_counts,
            'recent_errors': recent_count,
            'recurring_errors': recurring_count,
            'most_frequent': max(
                self.detected_errors.values(),
                key=lambda x: x.frequency
            ).error_id if self.detected_errors else None
        }

    def clear_old_errors(self, max_age_hours: int = 24):
        """Clear old errors from memory."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        old_error_ids = [
            error_id for error_id, detected_error in self.detected_errors.items()
            if detected_error.timestamp < cutoff_time
        ]

        for error_id in old_error_ids:
            del self.detected_errors[error_id]

        if old_error_ids:
            self.logger.info(f"Cleared {len(old_error_ids)} old errors")

    def get_error_details(self, error_id: str) -> Optional[DetectedError]:
        """Get detailed information about a specific error."""
        return self.detected_errors.get(error_id)
