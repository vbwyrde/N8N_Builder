"""
AG-UI compatible message broker for N8N Workflow Builder.

This module provides message routing and handling that is compatible with AG-UI
event streams while managing N8N workflow-specific messaging.
"""

import asyncio
import logging
from typing import Dict, Any, List, Callable, Optional, Set, Union
from datetime import datetime
from collections import defaultdict
import uuid

# Import AG-UI core types
from ag_ui.core import (
    Event as AGUIEvent,
    EventType as AGUIEventType,
    BaseEvent
)

from .event_types import WorkflowEvent, EventPriority, WorkflowEventType
from .message_protocol import (
    MessageType,
    WorkflowRequest,
    WorkflowResponse,
    StatusUpdate,
    ToolCallRequest,
    ToolCallResponse
)


class MessageBroker:
    """
    AG-UI compatible message broker for routing events and messages.
    
    Handles both AG-UI standard events and workflow-specific messages.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the message broker."""
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Message routing
        self._subscribers: Dict[Union[AGUIEventType, WorkflowEventType, MessageType], Set[Callable]] = defaultdict(set)
        self._wildcard_subscribers: Set[Callable] = set()
        
        # Message queues
        self._message_queue = asyncio.PriorityQueue()
        self._response_handlers: Dict[str, Callable] = {}
        
        # Broker state
        self._running = False
        self._tasks: List[asyncio.Task] = []
        self._message_history: List[Dict[str, Any]] = []
        self._max_history_size = self.config.get('max_history_size', 1000)
        
        # Performance metrics
        self._messages_processed = 0
        self._messages_failed = 0
        self._start_time = None
    
    async def start(self) -> None:
        """Start the message broker."""
        if self._running:
            return
        
        self._running = True
        self._start_time = datetime.now()
        
        # Start message processing tasks
        self._tasks = [
            asyncio.create_task(self._process_messages()),
            asyncio.create_task(self._cleanup_expired_handlers())
        ]
        
        self.logger.info("Message broker started")
    
    async def stop(self) -> None:
        """Stop the message broker."""
        if not self._running:
            return
        
        self._running = False
        
        # Cancel all tasks
        for task in self._tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks.clear()
        
        # Clear handlers and subscribers
        self._response_handlers.clear()
        self._subscribers.clear()
        self._wildcard_subscribers.clear()
        
        self.logger.info("Message broker stopped")
    
    async def publish_ag_ui_event(self, event: AGUIEvent, priority: EventPriority = EventPriority.NORMAL) -> None:
        """Publish an AG-UI event."""
        await self._publish_message({
            'type': 'ag_ui_event',
            'event': event,
            'priority': priority,
            'timestamp': datetime.now(),
            'message_id': str(uuid.uuid4())
        })
    
    async def publish_workflow_event(self, event: WorkflowEvent) -> None:
        """Publish a workflow-specific event."""
        await self._publish_message({
            'type': 'workflow_event',
            'event': event,
            'priority': event.priority,
            'timestamp': event.timestamp,
            'message_id': str(uuid.uuid4())
        })
    
    async def publish_message(self, message_type: MessageType, data: Any, priority: EventPriority = EventPriority.NORMAL) -> None:
        """Publish a general message."""
        await self._publish_message({
            'type': 'message',
            'message_type': message_type,
            'data': data,
            'priority': priority,
            'timestamp': datetime.now(),
            'message_id': str(uuid.uuid4())
        })
    
    async def send_request(self, request: WorkflowRequest, timeout: float = 30.0) -> WorkflowResponse:
        """Send a request and wait for response."""
        request_id = str(uuid.uuid4())
        response_future = asyncio.Future()
        
        # Register response handler
        self._response_handlers[request_id] = response_future
        
        # Publish request
        await self._publish_message({
            'type': 'request',
            'request': request,
            'request_id': request_id,
            'priority': EventPriority.HIGH,
            'timestamp': datetime.now(),
            'message_id': str(uuid.uuid4())
        })
        
        try:
            # Wait for response with timeout
            response = await asyncio.wait_for(response_future, timeout=timeout)
            return response
        except asyncio.TimeoutError:
            # Clean up handler on timeout
            if request_id in self._response_handlers:
                del self._response_handlers[request_id]
            raise
        finally:
            # Ensure handler is cleaned up
            if request_id in self._response_handlers:
                del self._response_handlers[request_id]
    
    async def send_response(self, request_id: str, response: WorkflowResponse) -> None:
        """Send a response to a request."""
        if request_id in self._response_handlers:
            handler = self._response_handlers[request_id]
            if not handler.done():
                handler.set_result(response)
    
    async def subscribe(self, event_type: Union[AGUIEventType, WorkflowEventType, MessageType], callback: Callable) -> None:
        """Subscribe to specific event types."""
        self._subscribers[event_type].add(callback)
        self.logger.debug(f"Added subscriber for {event_type}")
    
    async def subscribe_all(self, callback: Callable) -> None:
        """Subscribe to all events (wildcard subscription)."""
        self._wildcard_subscribers.add(callback)
        self.logger.debug("Added wildcard subscriber")
    
    async def unsubscribe(self, event_type: Union[AGUIEventType, WorkflowEventType, MessageType], callback: Callable) -> None:
        """Unsubscribe from specific event types."""
        if event_type in self._subscribers:
            self._subscribers[event_type].discard(callback)
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]
        self.logger.debug(f"Removed subscriber for {event_type}")
    
    async def unsubscribe_all(self, callback: Callable) -> None:
        """Unsubscribe from all events."""
        self._wildcard_subscribers.discard(callback)
        for subscribers in self._subscribers.values():
            subscribers.discard(callback)
        self.logger.debug("Removed wildcard subscriber")
    
    async def get_metrics(self) -> Dict[str, Any]:
        """Get broker performance metrics."""
        uptime = (datetime.now() - self._start_time).total_seconds() if self._start_time else 0
        
        return {
            'running': self._running,
            'uptime_seconds': uptime,
            'messages_processed': self._messages_processed,
            'messages_failed': self._messages_failed,
            'success_rate': (self._messages_processed / max(self._messages_processed + self._messages_failed, 1)) * 100,
            'queue_size': self._message_queue.qsize(),
            'active_subscribers': sum(len(subs) for subs in self._subscribers.values()),
            'wildcard_subscribers': len(self._wildcard_subscribers),
            'pending_responses': len(self._response_handlers),
            'history_size': len(self._message_history)
        }
    
    async def get_message_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get message processing history."""
        history = self._message_history.copy()
        if limit:
            history = history[-limit:]
        return history
    
    async def _publish_message(self, message: Dict[str, Any]) -> None:
        """Internal method to publish a message to the queue."""
        if not self._running:
            raise RuntimeError("Message broker is not running")
        
        # Calculate priority (negative for min-heap)
        priority = -message.get('priority', EventPriority.NORMAL).value
        
        await self._message_queue.put((priority, message))
        self.logger.debug(f"Published message: {message.get('type')}")
    
    async def _process_messages(self) -> None:
        """Process messages from the queue."""
        while self._running:
            try:
                # Get message from queue
                _, message = await self._message_queue.get()
                
                # Process the message
                await self._handle_message(message)
                
                # Mark task as done
                self._message_queue.task_done()
                
                # Update metrics
                self._messages_processed += 1
                
                # Add to history
                self._add_to_history(message, 'processed')
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error processing message: {e}")
                self._messages_failed += 1
                await asyncio.sleep(0.1)  # Brief pause on error
    
    async def _handle_message(self, message: Dict[str, Any]) -> None:
        """Handle a specific message."""
        message_type = message.get('type')
        
        try:
            if message_type == 'ag_ui_event':
                await self._handle_ag_ui_event(message['event'])
            elif message_type == 'workflow_event':
                await self._handle_workflow_event(message['event'])
            elif message_type == 'message':
                await self._handle_general_message(message['message_type'], message['data'])
            elif message_type == 'request':
                await self._handle_request(message['request'], message['request_id'])
            else:
                self.logger.warning(f"Unknown message type: {message_type}")
                
        except Exception as e:
            self.logger.error(f"Error handling message {message_type}: {e}")
            raise
    
    async def _handle_ag_ui_event(self, event: AGUIEvent) -> None:
        """Handle AG-UI events."""
        # Notify specific subscribers
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                await self._call_subscriber(callback, event)
        
        # Notify wildcard subscribers
        for callback in self._wildcard_subscribers:
            await self._call_subscriber(callback, event)
    
    async def _handle_workflow_event(self, event: WorkflowEvent) -> None:
        """Handle workflow-specific events."""
        # Notify specific subscribers
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                await self._call_subscriber(callback, event)
        
        # Notify wildcard subscribers
        for callback in self._wildcard_subscribers:
            await self._call_subscriber(callback, event)
    
    async def _handle_general_message(self, message_type: MessageType, data: Any) -> None:
        """Handle general messages."""
        # Notify specific subscribers
        if message_type in self._subscribers:
            for callback in self._subscribers[message_type]:
                await self._call_subscriber(callback, data)
        
        # Notify wildcard subscribers
        for callback in self._wildcard_subscribers:
            await self._call_subscriber(callback, {'type': message_type, 'data': data})
    
    async def _handle_request(self, request: WorkflowRequest, request_id: str) -> None:
        """Handle workflow requests."""
        # This would typically be handled by specific request processors
        # For now, just notify subscribers
        if request.request_type in self._subscribers:
            for callback in self._subscribers[request.request_type]:
                await self._call_subscriber(callback, {'request': request, 'request_id': request_id})
    
    async def _call_subscriber(self, callback: Callable, data: Any) -> None:
        """Call a subscriber callback safely."""
        try:
            if asyncio.iscoroutinefunction(callback):
                await callback(data)
            else:
                callback(data)
        except Exception as e:
            self.logger.error(f"Error in subscriber callback: {e}")
    
    async def _cleanup_expired_handlers(self) -> None:
        """Clean up expired response handlers."""
        while self._running:
            try:
                # Clean up handlers that have been waiting too long
                current_time = datetime.now()
                expired_handlers = []
                
                for request_id, handler in self._response_handlers.items():
                    if handler.done() or (current_time - handler.get_loop().time()) > 300:  # 5 minutes
                        expired_handlers.append(request_id)
                
                for request_id in expired_handlers:
                    if request_id in self._response_handlers:
                        del self._response_handlers[request_id]
                
                # Sleep before next cleanup
                await asyncio.sleep(60)  # Clean up every minute
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in cleanup task: {e}")
                await asyncio.sleep(60)
    
    def _add_to_history(self, message: Dict[str, Any], status: str) -> None:
        """Add message to processing history."""
        history_entry = {
            'message_id': message.get('message_id'),
            'type': message.get('type'),
            'status': status,
            'timestamp': datetime.now().isoformat(),
            'priority': message.get('priority', EventPriority.NORMAL).value if hasattr(message.get('priority', EventPriority.NORMAL), 'value') else str(message.get('priority', EventPriority.NORMAL))
        }
        
        self._message_history.append(history_entry)
        
        # Trim history if needed
        if len(self._message_history) > self._max_history_size:
            self._message_history = self._message_history[-self._max_history_size:]


__all__ = ['MessageBroker']
