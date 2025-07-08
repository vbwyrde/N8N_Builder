from typing import Dict, Any, Optional, List, Callable
import asyncio
import logging
from datetime import datetime, timedelta
from enum import Enum
from .event_types import Event, EventType, EventPriority

class CircuitState(Enum):
    """States for the circuit breaker pattern."""
    CLOSED = "closed"  # Normal operation, requests allowed
    OPEN = "open"      # Circuit is open, requests blocked
    HALF_OPEN = "half_open"  # Testing if service is recovered

class ErrorRecoveryManager:
    """Manages error recovery and retry logic."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.max_retries = self.config.get('max_retries', 3)
        self.retry_delay = self.config.get('retry_delay', 5)  # seconds
        self.error_handlers: Dict[str, Callable] = {}
        self.recovery_strategies: Dict[str, Callable] = {}
        self.circuit_states: Dict[str, CircuitState] = {}  # Track circuit states for different services
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the error recovery manager."""
        if self._running:
            return

        self._running = True
        self._tasks = [
            asyncio.create_task(self._process_error_queue())
        ]
        self.logger.info("Error Recovery Manager started")

    async def stop(self):
        """Stop the error recovery manager."""
        if not self._running:
            return

        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self.logger.info("Error Recovery Manager stopped")

    def register_error_handler(self, error_type: str, handler: Callable):
        """Register a handler for a specific error type."""
        self.error_handlers[error_type] = handler
        self.logger.debug(f"Registered error handler for type: {error_type}")

    def register_recovery_strategy(self, error_type: str, strategy: Callable):
        """Register a recovery strategy for a specific error type."""
        self.recovery_strategies[error_type] = strategy
        self.logger.debug(f"Registered recovery strategy for type: {error_type}")

    async def handle_error(self, error: Exception, context: Dict[str, Any]) -> bool:
        """Handle an error and attempt recovery."""
        try:
            error_type = type(error).__name__
            
            # Create error event
            event = Event(
                type=EventType.SYSTEM_ERROR,
                data={
                    "error_type": error_type,
                    "error_message": str(error),
                    "context": context
                },
                priority=EventPriority.HIGH,
                source="error_recovery_manager"
            )
            
            # Log the error
            self.logger.error(f"Error occurred: {error_type} - {str(error)}")
            
            # Try to handle the error
            if error_type in self.error_handlers:
                handler = self.error_handlers[error_type]
                await handler(error, context)
            
            # Try to recover
            if error_type in self.recovery_strategies:
                strategy = self.recovery_strategies[error_type]
                return await strategy(error, context)
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error in error handler: {str(e)}")
            return False

    async def retry_operation(self, operation: Callable, *args, **kwargs) -> Any:
        """Retry an operation with exponential backoff."""
        retries = 0
        while retries < self.max_retries:
            try:
                return await operation(*args, **kwargs)
            except Exception as e:
                retries += 1
                if retries == self.max_retries:
                    raise
                
                delay = self.retry_delay * (2 ** (retries - 1))  # Exponential backoff
                self.logger.warning(f"Operation failed, retrying in {delay} seconds...")
                await asyncio.sleep(delay)

    async def _process_error_queue(self):
        """Process the error queue."""
        while self._running:
            try:
                # This would typically process errors from a queue
                # For now, just sleep as this is a placeholder
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in error queue processing: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    def create_error_event(self, error: Exception, context: Dict[str, Any]) -> Event:
        """Create an error event."""
        return Event(
            type=EventType.SYSTEM_ERROR,
            data={
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context,
                "timestamp": datetime.now().isoformat()
            },
            priority=EventPriority.HIGH,
            source="error_recovery_manager"
        )

    async def get_error_history(
        self,
        error_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Get error history with optional filtering."""
        # This would typically query a database or storage system
        # For now, return an empty list as this is a placeholder
        return [] 