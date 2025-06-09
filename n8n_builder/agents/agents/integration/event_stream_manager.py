import asyncio
import json
import logging
from typing import Dict, Set, Optional, List, Any
from datetime import datetime
from .event_types import Event, EventType

class EventStreamManager:
    """Manages event streams and SSE connections."""
    
    def __init__(self, max_buffer_size: int = 1000):
        self.logger = logging.getLogger(__name__)
        self.max_buffer_size = max_buffer_size
        self.event_streams: Dict[str, asyncio.Queue] = {}
        self.event_subscribers: Dict[str, Set[str]] = {}
        self.event_buffer: List[Event] = []
        self._running = False
        self._event_processor = None
    
    async def start(self):
        """Start the event stream manager."""
        if self._running:
            return
        
        self._running = True
        self._event_processor = asyncio.create_task(self._process_events())
        self.logger.info("EventStreamManager started")
    
    async def stop(self):
        """Stop the event stream manager."""
        if not self._running:
            return
        
        self._running = False
        if self._event_processor:
            self._event_processor.cancel()
            try:
                await self._event_processor
            except asyncio.CancelledError:
                pass
        
        # Clear all streams and subscribers
        self.event_streams.clear()
        self.event_subscribers.clear()
        self.event_buffer.clear()
        
        self.logger.info("EventStreamManager stopped")
    
    async def create_stream(self, stream_id: str) -> asyncio.Queue:
        """Create a new event stream."""
        if stream_id in self.event_streams:
            return self.event_streams[stream_id]
        
        queue = asyncio.Queue(maxsize=self.max_buffer_size)
        self.event_streams[stream_id] = queue
        self.event_subscribers[stream_id] = set()
        
        self.logger.info(f"Created event stream: {stream_id}")
        return queue
    
    async def remove_stream(self, stream_id: str):
        """Remove an event stream."""
        if stream_id in self.event_streams:
            del self.event_streams[stream_id]
            del self.event_subscribers[stream_id]
            self.logger.info(f"Removed event stream: {stream_id}")
    
    async def subscribe(self, stream_id: str, event_types: Set[EventType]):
        """Subscribe a stream to specific event types."""
        if stream_id not in self.event_subscribers:
            raise ValueError(f"Stream {stream_id} does not exist")
        
        self.event_subscribers[stream_id].update(event_types)
        self.logger.info(f"Stream {stream_id} subscribed to events: {event_types}")
    
    async def unsubscribe(self, stream_id: str, event_types: Set[EventType]):
        """Unsubscribe a stream from specific event types."""
        if stream_id not in self.event_subscribers:
            return
        
        self.event_subscribers[stream_id].difference_update(event_types)
        self.logger.info(f"Stream {stream_id} unsubscribed from events: {event_types}")
    
    async def publish_event(self, event: Event):
        """Publish an event to all subscribed streams."""
        # Add to buffer
        self.event_buffer.append(event)
        if len(self.event_buffer) > self.max_buffer_size:
            self.event_buffer.pop(0)
        
        # Publish to subscribers
        for stream_id, queue in self.event_streams.items():
            if event.event_type in self.event_subscribers[stream_id]:
                try:
                    await queue.put(event)
                except asyncio.QueueFull:
                    self.logger.warning(f"Event queue full for stream {stream_id}")
    
    async def get_event_history(self, event_types: Optional[Set[EventType]] = None,
                              limit: int = 100) -> List[Event]:
        """Get event history, optionally filtered by event types."""
        events = self.event_buffer[-limit:] if limit else self.event_buffer
        if event_types:
            events = [e for e in events if e.event_type in event_types]
        return events
    
    async def _process_events(self):
        """Background task to process and distribute events."""
        while self._running:
            try:
                # Process any pending events
                for stream_id, queue in self.event_streams.items():
                    if not queue.empty():
                        event = await queue.get()
                        # Convert event to SSE format
                        sse_data = self._format_sse_event(event)
                        # Send to stream
                        await self._send_sse_event(stream_id, sse_data)
                        queue.task_done()
                
                await asyncio.sleep(0.1)  # Prevent CPU spinning
            except Exception as e:
                self.logger.error(f"Error processing events: {str(e)}")
                await asyncio.sleep(1)  # Back off on error
    
    def _format_sse_event(self, event: Event) -> str:
        """Format an event as an SSE message."""
        data = {
            'type': event.event_type.value,
            'timestamp': event.timestamp.isoformat(),
            'source': event.source,
            'correlation_id': event.correlation_id,
            'parent_event_id': event.parent_event_id,
            'metadata': event.metadata
        }
        
        # Add type-specific data
        if hasattr(event, 'workflow_id'):
            data['workflow_id'] = event.workflow_id
            data['workflow_status'] = event.workflow_status
            data['progress'] = event.progress
            data['error_message'] = event.error_message
        elif hasattr(event, 'agent_id'):
            data['agent_id'] = event.agent_id
            data['agent_status'] = event.agent_status
            data['operation'] = event.operation
            data['result'] = event.result
            data['error_message'] = event.error_message
        
        return f"data: {json.dumps(data)}\n\n"
    
    async def _send_sse_event(self, stream_id: str, sse_data: str):
        """Send an SSE event to a specific stream."""
        if stream_id not in self.event_streams:
            return
        
        try:
            queue = self.event_streams[stream_id]
            await queue.put(sse_data)
        except Exception as e:
            self.logger.error(f"Error sending SSE event to stream {stream_id}: {str(e)}")
    
    async def get_stream_events(self, stream_id: str, timeout: Optional[float] = None) -> Optional[str]:
        """Get the next event from a stream."""
        if stream_id not in self.event_streams:
            return None
        
        try:
            return await asyncio.wait_for(
                self.event_streams[stream_id].get(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return None
        except Exception as e:
            self.logger.error(f"Error getting events from stream {stream_id}: {str(e)}")
            return None 