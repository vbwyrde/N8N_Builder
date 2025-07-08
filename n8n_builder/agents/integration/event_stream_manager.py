from typing import Dict, Any, List, Callable, Optional, Set
import asyncio
import logging
from datetime import datetime
from .event_types import Event, EventType, EventPriority

class EventStreamManager:
    """Manages event streams and subscriptions."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.event_queue = asyncio.PriorityQueue()
        self.subscribers: Dict[EventType, Set[Callable]] = {}
        self.logger = logging.getLogger(__name__)
        self._running = False
        self._tasks: List[asyncio.Task] = []

    async def start(self):
        """Start the event stream manager."""
        if self._running:
            return

        self._running = True
        self._tasks = [
            asyncio.create_task(self._process_events())
        ]
        self.logger.info("Event Stream Manager started")

    async def stop(self):
        """Stop the event stream manager."""
        if not self._running:
            return

        self._running = False
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self.logger.info("Event Stream Manager stopped")

    async def publish_event(self, event: Event):
        """Publish an event to the stream."""
        if not self._running:
            raise RuntimeError("Event Stream Manager is not running")

        # Calculate priority (higher number = higher priority)
        priority = -event.priority.value  # Negative because PriorityQueue is min-heap
        await self.event_queue.put((priority, event))
        self.logger.debug(f"Published event: {event.type.value}")

    async def publish_events(self, events: List[Event]):
        """Publish multiple events to the stream."""
        for event in events:
            await self.publish_event(event)

    async def subscribe(self, event_type: EventType, callback: Callable):
        """Subscribe to events of a specific type."""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = set()
        self.subscribers[event_type].add(callback)
        self.logger.debug(f"Added subscriber for event type: {event_type.value}")

    async def unsubscribe(self, event_type: EventType, callback: Callable):
        """Unsubscribe from events of a specific type."""
        if event_type in self.subscribers:
            self.subscribers[event_type].discard(callback)
            if not self.subscribers[event_type]:
                del self.subscribers[event_type]
            self.logger.debug(f"Removed subscriber for event type: {event_type.value}")

    async def _process_events(self):
        """Process events from the queue."""
        while self._running:
            try:
                # Get event from queue
                _, event = await self.event_queue.get()
                
                # Notify subscribers
                if event.type in self.subscribers:
                    for callback in self.subscribers[event.type]:
                        try:
                            await callback(event)
                        except Exception as e:
                            self.logger.error(f"Error in event subscriber: {str(e)}")
                
                self.event_queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing event: {str(e)}")
                await asyncio.sleep(1)  # Back off on error

    async def get_event_history(
        self,
        event_type: Optional[EventType] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Event]:
        """Get event history with optional filtering."""
        # This would typically query a database or storage system
        # For now, return an empty list as this is a placeholder
        return []

    async def clear_event_history(self):
        """Clear event history."""
        # This would typically clear a database or storage system
        # For now, do nothing as this is a placeholder
        pass 