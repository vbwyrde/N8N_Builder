"""
24-Hour Log Rotation Manager for N8N Builder and Enterprise Module
Implements time-based log rotation with datestamps to prevent large files
"""

import os
import logging
import shutil
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from logging.handlers import TimedRotatingFileHandler
import threading
import time
import schedule


class DatestampedTimedRotatingFileHandler(TimedRotatingFileHandler):
    """
    Enhanced TimedRotatingFileHandler that adds datestamps to rotated files
    and provides better compression and cleanup options.
    """
    
    def __init__(self, filename, when='midnight', interval=1, backupCount=7, 
                 encoding=None, delay=False, utc=False, atTime=None, 
                 compress=True, datestamp_format='%Y%m%d'):
        """
        Initialize the handler with compression and datestamp options.
        
        Args:
            filename: Log file path
            when: When to rotate ('midnight', 'H', 'D', etc.)
            interval: Rotation interval
            backupCount: Number of backup files to keep
            compress: Whether to compress rotated files
            datestamp_format: Format for datestamp in rotated files
        """
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.compress = compress
        self.datestamp_format = datestamp_format
        
    def doRollover(self):
        """
        Do a rollover with datestamp and optional compression.
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        
        # Get current time for datestamp
        current_time = datetime.now()
        datestamp = current_time.strftime(self.datestamp_format)
        
        # Create backup filename with datestamp
        base_filename = self.baseFilename
        backup_filename = f"{base_filename}.{datestamp}"
        
        # If backup file already exists, add time suffix
        if os.path.exists(backup_filename):
            time_suffix = current_time.strftime('%H%M%S')
            backup_filename = f"{base_filename}.{datestamp}_{time_suffix}"
        
        # Move current log to backup
        if os.path.exists(base_filename):
            shutil.move(base_filename, backup_filename)
            
            # Compress if enabled
            if self.compress:
                self._compress_file(backup_filename)
        
        # Clean up old backups
        self._cleanup_old_backups()
        
        # Create new log file
        if not self.delay:
            self.stream = self._open()
    
    def _compress_file(self, filename: str):
        """Compress a log file using gzip."""
        try:
            compressed_filename = f"{filename}.gz"
            with open(filename, 'rb') as f_in:
                with gzip.open(compressed_filename, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            
            # Remove original file after compression
            os.remove(filename)
            
        except Exception as e:
            # If compression fails, keep the original file
            logging.error(f"Failed to compress log file {filename}: {e}")
    
    def _cleanup_old_backups(self):
        """Clean up old backup files based on backupCount."""
        if self.backupCount <= 0:
            return
        
        # Get directory and base filename
        dir_name = os.path.dirname(self.baseFilename)
        base_name = os.path.basename(self.baseFilename)
        
        # Find all backup files
        backup_files = []
        for filename in os.listdir(dir_name):
            if filename.startswith(base_name + '.'):
                full_path = os.path.join(dir_name, filename)
                if os.path.isfile(full_path):
                    backup_files.append((full_path, os.path.getmtime(full_path)))
        
        # Sort by modification time (newest first)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove old backups
        for file_path, _ in backup_files[self.backupCount:]:
            try:
                os.remove(file_path)
            except Exception as e:
                logging.error(f"Failed to remove old backup {file_path}: {e}")


class LogRotationManager:
    """
    Manages log rotation for all N8N Builder and Enterprise Module log files.
    Implements 24-hour rotation with datestamps and compression.
    """
    
    def __init__(self, log_directory: Optional[Path] = None):
        """Initialize the log rotation manager."""
        self.log_directory = log_directory or Path("logs")
        self.log_directory.mkdir(exist_ok=True)
        
        # Configuration
        self.rotation_time = "00:00"  # Rotate at midnight
        self.backup_count = 30  # Keep 30 days of logs
        self.compress_logs = True
        self.max_log_size = 100 * 1024 * 1024  # 100MB emergency size limit
        
        # Tracking
        self.managed_handlers: Dict[str, DatestampedTimedRotatingFileHandler] = {}
        self.scheduler_thread: Optional[threading.Thread] = None
        self.is_running = False
        
        # Logger for this manager
        self.logger = logging.getLogger('n8n_builder.log_rotation')
        
    def setup_log_rotation(self, log_configs: Optional[Dict[str, Dict]] = None):
        """
        Set up log rotation for specified log files.
        
        Args:
            log_configs: Dictionary of log configurations
                        {log_name: {filename: str, level: str, format: str}}
        """
        if log_configs is None:
            log_configs = self._get_default_log_configs()
        
        for log_name, config in log_configs.items():
            self._setup_single_log_rotation(log_name, config)
        
        # Start the rotation scheduler
        self._start_scheduler()
        
        self.logger.info(f"Log rotation setup complete for {len(log_configs)} log files")
    
    def _get_default_log_configs(self) -> Dict[str, Dict]:
        """Get default log configurations for N8N Builder and Enterprise Module."""
        return {
            'main': {
                'filename': 'n8n_builder.log',
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
            },
            'errors': {
                'filename': 'errors.log',
                'level': 'ERROR',
                'format': '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
            },
            'Enterprise_Module': {
                'filename': 'Enterprise_Module.log',
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'performance': {
                'filename': 'performance.log',
                'level': 'INFO',
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'debug': {
                'filename': 'debug.log',
                'level': 'DEBUG',
                'format': '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
            }
        }
    
    def _setup_single_log_rotation(self, log_name: str, config: Dict):
        """Set up rotation for a single log file."""
        filename = config['filename']
        log_path = self.log_directory / filename
        
        # Create the rotating file handler
        handler = DatestampedTimedRotatingFileHandler(
            filename=str(log_path),
            when='midnight',
            interval=1,
            backupCount=self.backup_count,
            compress=self.compress_logs,
            datestamp_format='%Y%m%d'
        )
        
        # Set formatter
        formatter = logging.Formatter(config.get('format', 
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        handler.setFormatter(formatter)
        
        # Set level
        level = getattr(logging, config.get('level', 'INFO').upper())
        handler.setLevel(level)
        
        # Store the handler
        self.managed_handlers[log_name] = handler
        
        self.logger.info(f"Set up rotation for {filename} (level: {config.get('level', 'INFO')})")
    
    def _start_scheduler(self):
        """Start the background scheduler for log rotation checks."""
        if self.is_running:
            return
        
        self.is_running = True
        
        # Schedule daily rotation check
        schedule.every().day.at(self.rotation_time).do(self._perform_rotation_check)
        
        # Schedule hourly size check
        schedule.every().hour.do(self._perform_size_check)
        
        # Start scheduler thread
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.scheduler_thread.start()
        
        self.logger.info(f"Log rotation scheduler started (rotation time: {self.rotation_time})")
    
    def _run_scheduler(self):
        """Run the scheduler in a background thread."""
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _perform_rotation_check(self):
        """Perform scheduled rotation check."""
        self.logger.info("Performing scheduled log rotation check")
        
        for log_name, handler in self.managed_handlers.items():
            try:
                # Force rotation check
                handler.doRollover()
                self.logger.info(f"Rotated log: {log_name}")
            except Exception as e:
                self.logger.error(f"Failed to rotate log {log_name}: {e}")
    
    def _perform_size_check(self):
        """Check log file sizes and rotate if they exceed limits."""
        for log_name, handler in self.managed_handlers.items():
            try:
                log_path = Path(handler.baseFilename)
                if log_path.exists():
                    size_mb = log_path.stat().st_size / (1024 * 1024)
                    
                    if size_mb > (self.max_log_size / (1024 * 1024)):
                        self.logger.warning(f"Log file {log_name} exceeds size limit ({size_mb:.1f}MB), forcing rotation")
                        handler.doRollover()
                        
            except Exception as e:
                self.logger.error(f"Failed to check size for log {log_name}: {e}")
    
    def get_log_statistics(self) -> Dict[str, Dict]:
        """Get statistics about managed log files."""
        stats = {}
        
        for log_name, handler in self.managed_handlers.items():
            try:
                log_path = Path(handler.baseFilename)
                
                if log_path.exists():
                    stat = log_path.stat()
                    size_mb = stat.st_size / (1024 * 1024)
                    modified = datetime.fromtimestamp(stat.st_mtime)
                    
                    # Count backup files
                    backup_count = self._count_backup_files(log_path)
                    
                    stats[log_name] = {
                        'current_size_mb': round(size_mb, 2),
                        'last_modified': modified.isoformat(),
                        'backup_files': backup_count,
                        'rotation_enabled': True
                    }
                else:
                    stats[log_name] = {
                        'current_size_mb': 0,
                        'last_modified': None,
                        'backup_files': 0,
                        'rotation_enabled': True
                    }
                    
            except Exception as e:
                stats[log_name] = {
                    'error': str(e),
                    'rotation_enabled': True
                }
        
        return stats
    
    def _count_backup_files(self, log_path: Path) -> int:
        """Count backup files for a given log file."""
        try:
            base_name = log_path.name
            backup_count = 0
            
            for file_path in log_path.parent.iterdir():
                if file_path.name.startswith(base_name + '.') and file_path.is_file():
                    backup_count += 1
            
            return backup_count
        except:
            return 0
    
    def cleanup_old_logs(self, days_to_keep: int = 30):
        """Clean up log files older than specified days."""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        cleaned_count = 0
        
        try:
            for log_file in self.log_directory.iterdir():
                if log_file.is_file() and log_file.suffix in ['.log', '.gz']:
                    try:
                        file_date = datetime.fromtimestamp(log_file.stat().st_mtime)
                        if file_date < cutoff_date:
                            log_file.unlink()
                            cleaned_count += 1
                            self.logger.info(f"Cleaned up old log file: {log_file.name}")
                    except Exception as e:
                        self.logger.error(f"Failed to clean up {log_file.name}: {e}")
            
            self.logger.info(f"Log cleanup complete: removed {cleaned_count} old files")
            
        except Exception as e:
            self.logger.error(f"Log cleanup failed: {e}")
    
    def stop(self):
        """Stop the log rotation manager."""
        self.is_running = False
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
        
        self.logger.info("Log rotation manager stopped")


# Global instance
log_rotation_manager = None

def get_log_rotation_manager() -> LogRotationManager:
    """Get or create the global log rotation manager instance."""
    global log_rotation_manager
    if log_rotation_manager is None:
        log_rotation_manager = LogRotationManager()
    return log_rotation_manager

def setup_24hour_log_rotation():
    """Set up 24-hour log rotation for the entire system."""
    manager = get_log_rotation_manager()
    manager.setup_log_rotation()
    return manager
