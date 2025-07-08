from typing import Dict, Any, Optional, List, Set
import asyncio
import logging
import psutil
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
from .event_types import Event, EventType, EventPriority

class MetricType(Enum):
    """Types of metrics that can be collected."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"

class HealthStatus(Enum):
    """Health status of a component."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    UNKNOWN = "unknown"

@dataclass
class Metric:
    """Represents a metric with metadata."""
    name: str
    value: float
    metric_type: MetricType
    labels: Dict[str, str]
    timestamp: datetime

class MonitoringManager:
    """Manages system monitoring and metrics collection."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.collection_interval = self.config.get('collection_interval', 60)  # seconds
        self.metric_thresholds = self.config.get('metric_thresholds', {})
        self.metrics_history: Dict[str, List[Metric]] = {}
        self.metrics: Dict[str, List[Metric]] = {}  # For compatibility
        self.health_status: Dict[str, HealthStatus] = {}
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the monitoring manager."""
        if self._running:
            return

        self._running = True
        self._tasks = [
            asyncio.create_task(self._collect_metrics()),
            asyncio.create_task(self._check_health())
        ]
        self.logger.info("Monitoring Manager started")

    async def stop(self):
        """Stop the monitoring manager."""
        if not self._running:
            return

        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self.logger.info("Monitoring Manager stopped")

    async def record_metric(self, name: str, value: float, metric_type: MetricType, labels: Optional[Dict[str, str]] = None) -> None:
        """Record a metric value."""
        metric = Metric(
            name=name,
            value=value,
            metric_type=metric_type,
            labels=labels or {},
            timestamp=datetime.now()
        )
        
        if name not in self.metrics_history:
            self.metrics_history[name] = []
            self.metrics[name] = []  # For compatibility
            
        self.metrics_history[name].append(metric)
        self.metrics[name].append(metric)  # For compatibility
        
        # Keep only last 24 hours of metrics
        cutoff = datetime.now() - timedelta(hours=24)
        self.metrics_history[name] = [
            m for m in self.metrics_history[name]
            if m.timestamp > cutoff
        ]
        self.metrics[name] = self.metrics_history[name]  # For compatibility
        
        self.logger.debug(f"Recorded metric: {name}={value} ({metric_type.value})")

    async def get_metric_history(
        self,
        metric_name: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Metric]:
        """Get historical data for a specific metric."""
        metrics = self.metrics_history.get(metric_name, [])
        
        if start_time or end_time:
            filtered_metrics = metrics
            if start_time:
                filtered_metrics = [m for m in filtered_metrics if m.timestamp >= start_time]
            if end_time:
                filtered_metrics = [m for m in filtered_metrics if m.timestamp <= end_time]
            return filtered_metrics
            
        return metrics

    async def _collect_metrics(self):
        """Collect system metrics periodically."""
        while self._running:
            try:
                # Collect CPU metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                await self.record_metric("system.cpu_usage", cpu_percent, MetricType.GAUGE, {"component": "system"})

                # Collect memory metrics
                memory = psutil.virtual_memory()
                await self.record_metric("system.memory_usage", memory.percent, MetricType.GAUGE, {"component": "system"})

                # Collect disk metrics
                try:
                    disk = psutil.disk_usage('/')
                    await self.record_metric("system.disk_usage", disk.percent, MetricType.GAUGE, {"component": "system"})
                except:
                    # Fallback for Windows
                    disk = psutil.disk_usage('C:')
                    await self.record_metric("system.disk_usage", disk.percent, MetricType.GAUGE, {"component": "system"})

                # Collect network metrics
                net_io = psutil.net_io_counters()
                await self.record_metric("system.network_bytes_sent", float(net_io.bytes_sent), MetricType.COUNTER, {"component": "system"})
                await self.record_metric("system.network_bytes_recv", float(net_io.bytes_recv), MetricType.COUNTER, {"component": "system"})

                await asyncio.sleep(self.collection_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error collecting metrics: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    async def _check_health(self):
        """Check system health based on metrics."""
        while self._running:
            try:
                for metric_name in ["system.cpu_usage", "system.memory_usage", "system.disk_usage"]:
                    latest_metrics = self.metrics_history.get(metric_name, [])
                    if latest_metrics:
                        current_value = latest_metrics[-1].value
                        status = self._evaluate_health(metric_name, current_value)
                        self.health_status[metric_name] = status
                        
                        if status != HealthStatus.HEALTHY:
                            self._create_health_event(metric_name, status, current_value)
                
                await asyncio.sleep(self.collection_interval)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error checking health: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    def _evaluate_health(self, metric_name: str, value: float) -> HealthStatus:
        """Evaluate health status based on metric value."""
        thresholds = self.metric_thresholds.get(metric_name, {})
        
        if value >= thresholds.get('critical', 90):
            return HealthStatus.UNHEALTHY
        elif value >= thresholds.get('warning', 70):
            return HealthStatus.DEGRADED
        return HealthStatus.HEALTHY

    def _create_health_event(self, metric_name: str, status: HealthStatus, value: float):
        """Create a health-related event."""
        event = Event(
            type=EventType.RESOURCE_WARNING,
            data={
                'metric_name': metric_name,
                'status': status.value,
                'value': value,
                'threshold': self.metric_thresholds.get(metric_name, {})
            },
            priority=EventPriority.HIGH if status == HealthStatus.UNHEALTHY else EventPriority.NORMAL,
            source='monitoring_manager'
        )
        self.logger.warning(f"Health event created: {metric_name} - {status.value}")

    async def get_metrics(
        self,
        metric_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get metrics with optional filtering."""
        if metric_name:
            metrics = await self.get_metric_history(metric_name, start_time, end_time)
            return {
                metric_name: [
                    {
                        'value': m.value,
                        'timestamp': m.timestamp.isoformat(),
                        'labels': m.labels
                    }
                    for m in metrics
                ]
            }
        else:
            all_metrics = {}
            for name in self.metrics_history:
                metrics = await self.get_metric_history(name, start_time, end_time)
                all_metrics[name] = [
                    {
                        'value': m.value,
                        'timestamp': m.timestamp.isoformat(),
                        'labels': m.labels
                    }
                    for m in metrics
                ]
            return all_metrics

    async def get_health_status(self) -> Dict[str, str]:
        """Get current health status for all metrics."""
        return {k: v.value for k, v in self.health_status.items()} 