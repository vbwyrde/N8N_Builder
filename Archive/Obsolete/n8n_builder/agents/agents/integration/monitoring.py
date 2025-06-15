import logging
import time
import json
import asyncio
from typing import Dict, Any, Optional, List, Set
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import psutil
import aiohttp
from logging.handlers import RotatingFileHandler

class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"

class HealthStatus(Enum):
    """Health check status levels."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class Metric:
    """Represents a collected metric."""
    name: str
    value: float
    type: MetricType
    timestamp: datetime
    labels: Dict[str, str]
    description: Optional[str] = None

@dataclass
class HealthCheck:
    """Represents a health check result."""
    name: str
    status: HealthStatus
    message: str
    timestamp: datetime
    details: Dict[str, Any]

class MonitoringManager:
    """Manages monitoring, metrics collection, and logging."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = self._setup_logger()
        
        # Metrics storage
        self.metrics: Dict[str, List[Metric]] = {}
        self.metric_retention = config.get('metrics', {}).get('retention_hours', 24)
        
        # Health check storage
        self.health_checks: Dict[str, HealthCheck] = {}
        self.health_check_interval = config.get('health_checks', {}).get('interval_seconds', 60)
        
        # Resource monitoring
        self.resource_limits = config.get('resources', {}).get('limits', {})
        self.resource_warnings = config.get('resources', {}).get('warnings', {})
        
        # Initialize background tasks
        self._running = False
        self._tasks: Set[asyncio.Task] = set()
    
    def _setup_logger(self) -> logging.Logger:
        """Set up the logging system."""
        logger = logging.getLogger('n8n_monitoring')
        logger.setLevel(logging.INFO)
        
        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(
            self.config.get('logging', {}).get('file', 'logs/n8n.log'),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    async def start(self):
        """Start the monitoring system."""
        if self._running:
            return
        
        self._running = True
        
        # Start background tasks
        self._tasks.add(asyncio.create_task(self._collect_system_metrics()))
        self._tasks.add(asyncio.create_task(self._run_health_checks()))
        self._tasks.add(asyncio.create_task(self._cleanup_old_metrics()))
        
        self.logger.info("Monitoring system started")
    
    async def stop(self):
        """Stop the monitoring system."""
        if not self._running:
            return
        
        self._running = False
        
        # Cancel all background tasks
        for task in self._tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        
        self.logger.info("Monitoring system stopped")
    
    async def _collect_system_metrics(self):
        """Collect system metrics periodically."""
        while self._running:
            try:
                # CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                await self.record_metric(
                    'system.cpu.usage',
                    cpu_percent,
                    MetricType.GAUGE,
                    {'type': 'system'}
                )
                
                # Memory metrics
                memory = psutil.virtual_memory()
                await self.record_metric(
                    'system.memory.usage',
                    memory.percent,
                    MetricType.GAUGE,
                    {'type': 'system'}
                )
                
                # Disk metrics
                disk = psutil.disk_usage('/')
                await self.record_metric(
                    'system.disk.usage',
                    disk.percent,
                    MetricType.GAUGE,
                    {'type': 'system'}
                )
                
                # Network metrics
                net_io = psutil.net_io_counters()
                await self.record_metric(
                    'system.network.bytes_sent',
                    net_io.bytes_sent,
                    MetricType.COUNTER,
                    {'type': 'system'}
                )
                await self.record_metric(
                    'system.network.bytes_recv',
                    net_io.bytes_recv,
                    MetricType.COUNTER,
                    {'type': 'system'}
                )
                
                # Check resource limits
                await self._check_resource_limits()
                
            except Exception as e:
                self.logger.error(f"Error collecting system metrics: {str(e)}")
            
            await asyncio.sleep(self.config.get('metrics', {}).get('collection_interval', 60))
    
    async def _check_resource_limits(self):
        """Check if any resource usage exceeds limits."""
        for resource, limit in self.resource_limits.items():
            current_usage = await self.get_latest_metric(f'system.{resource}.usage')
            if current_usage and current_usage.value > limit:
                self.logger.warning(
                    f"Resource {resource} usage ({current_usage.value}%) exceeds limit ({limit}%)"
                )
    
    async def _run_health_checks(self):
        """Run health checks periodically."""
        while self._running:
            try:
                # System health
                await self._check_system_health()
                
                # Service health
                await self._check_service_health()
                
                # Dependency health
                await self._check_dependency_health()
                
            except Exception as e:
                self.logger.error(f"Error running health checks: {str(e)}")
            
            await asyncio.sleep(self.health_check_interval)
    
    async def _check_system_health(self):
        """Check system health."""
        try:
            # Check CPU usage
            cpu_usage = psutil.cpu_percent()
            status = HealthStatus.HEALTHY
            if cpu_usage > 90:
                status = HealthStatus.UNHEALTHY
            elif cpu_usage > 70:
                status = HealthStatus.DEGRADED
            
            await self.record_health_check(
                'system.cpu',
                status,
                f"CPU usage: {cpu_usage}%",
                {'usage': cpu_usage}
            )
            
            # Check memory usage
            memory = psutil.virtual_memory()
            status = HealthStatus.HEALTHY
            if memory.percent > 90:
                status = HealthStatus.UNHEALTHY
            elif memory.percent > 70:
                status = HealthStatus.DEGRADED
            
            await self.record_health_check(
                'system.memory',
                status,
                f"Memory usage: {memory.percent}%",
                {'usage': memory.percent}
            )
            
        except Exception as e:
            self.logger.error(f"Error checking system health: {str(e)}")
    
    async def _check_service_health(self):
        """Check health of internal services."""
        # Implement service-specific health checks
        pass
    
    async def _check_dependency_health(self):
        """Check health of external dependencies."""
        # Implement dependency-specific health checks
        pass
    
    async def _cleanup_old_metrics(self):
        """Clean up old metrics."""
        while self._running:
            try:
                cutoff_time = datetime.now() - timedelta(hours=self.metric_retention)
                
                for metric_name in self.metrics:
                    self.metrics[metric_name] = [
                        m for m in self.metrics[metric_name]
                        if m.timestamp > cutoff_time
                    ]
                
            except Exception as e:
                self.logger.error(f"Error cleaning up old metrics: {str(e)}")
            
            await asyncio.sleep(3600)  # Run cleanup every hour
    
    async def record_metric(self, name: str, value: float, type: MetricType,
                          labels: Dict[str, str], description: Optional[str] = None):
        """Record a new metric."""
        if name not in self.metrics:
            self.metrics[name] = []
        
        metric = Metric(
            name=name,
            value=value,
            type=type,
            timestamp=datetime.now(),
            labels=labels,
            description=description
        )
        
        self.metrics[name].append(metric)
        
        # Log metric
        self.logger.debug(
            f"Recorded metric: {name}={value} ({type.value}) "
            f"labels={json.dumps(labels)}"
        )
    
    async def get_latest_metric(self, name: str) -> Optional[Metric]:
        """Get the latest value for a metric."""
        if name not in self.metrics or not self.metrics[name]:
            return None
        
        return self.metrics[name][-1]
    
    async def get_metric_history(self, name: str, 
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None) -> List[Metric]:
        """Get historical values for a metric."""
        if name not in self.metrics:
            return []
        
        metrics = self.metrics[name]
        
        if start_time:
            metrics = [m for m in metrics if m.timestamp >= start_time]
        if end_time:
            metrics = [m for m in metrics if m.timestamp <= end_time]
        
        return metrics
    
    async def record_health_check(self, name: str, status: HealthStatus,
                                message: str, details: Dict[str, Any]):
        """Record a health check result."""
        health_check = HealthCheck(
            name=name,
            status=status,
            message=message,
            timestamp=datetime.now(),
            details=details
        )
        
        self.health_checks[name] = health_check
        
        # Log health check
        self.logger.info(
            f"Health check {name}: {status.value} - {message}"
        )
    
    async def get_health_status(self, name: Optional[str] = None) -> Dict[str, Any]:
        """Get health status for a specific check or all checks."""
        if name:
            check = self.health_checks.get(name)
            return {
                'name': name,
                'status': check.status.value if check else HealthStatus.UNKNOWN.value,
                'message': check.message if check else "No health check data",
                'timestamp': check.timestamp.isoformat() if check else None,
                'details': check.details if check else {}
            }
        
        return {
            name: {
                'status': check.status.value,
                'message': check.message,
                'timestamp': check.timestamp.isoformat(),
                'details': check.details
            }
            for name, check in self.health_checks.items()
        }
    
    def log_event(self, level: int, message: str, **kwargs):
        """Log an event with additional context."""
        self.logger.log(level, message, extra=kwargs)
    
    def log_metric(self, name: str, value: float, **kwargs):
        """Log a metric with additional context."""
        self.logger.info(
            f"Metric: {name}={value}",
            extra={'metric_name': name, 'metric_value': value, **kwargs}
        )
    
    def log_health(self, name: str, status: HealthStatus, message: str, **kwargs):
        """Log a health check with additional context."""
        self.logger.info(
            f"Health: {name} - {status.value} - {message}",
            extra={'health_check': name, 'status': status.value, 'message': message, **kwargs}
        ) 