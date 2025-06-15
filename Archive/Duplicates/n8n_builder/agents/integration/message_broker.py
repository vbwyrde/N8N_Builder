import asyncio
import logging
from typing import Dict, Any, Set, Callable, Awaitable, Optional
from .message_protocol import AgentMessage, MessageType, MessagePriority

class MessageBroker:
    """Handles message routing and delivery between agents."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.message_queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[MessageType, Set[str]] = {
            message_type: set() for message_type in MessageType
        }
        self.handlers: Dict[str, Dict[MessageType, Callable[[AgentMessage], Awaitable[None]]]] = {}
        self.running = False
        self.logger.info("MessageBroker initialized")
    
    async def start(self):
        """Start the message broker."""
        self.running = True
        self.logger.info("MessageBroker started")
    
    async def stop(self):
        """Stop the message broker."""
        self.running = False
        # Clear all queues
        for queue in self.message_queues.values():
            while not queue.empty():
                try:
                    queue.get_nowait()
                except asyncio.QueueEmpty:
                    break
        self.logger.info("MessageBroker stopped")
    
    def register_agent(self, agent_id: str):
        """Register an agent with the broker."""
        if agent_id not in self.message_queues:
            self.message_queues[agent_id] = asyncio.Queue()
            self.handlers[agent_id] = {}
            self.logger.info(f"Agent {agent_id} registered with MessageBroker")
    
    def unregister_agent(self, agent_id: str):
        """Unregister an agent from the broker."""
        if agent_id in self.message_queues:
            del self.message_queues[agent_id]
            del self.handlers[agent_id]
            # Remove from all subscriber lists
            for subscribers in self.subscribers.values():
                subscribers.discard(agent_id)
            self.logger.info(f"Agent {agent_id} unregistered from MessageBroker")
    
    def subscribe(self, agent_id: str, message_type: MessageType):
        """Subscribe an agent to a message type."""
        if agent_id in self.message_queues:
            self.subscribers[message_type].add(agent_id)
            self.logger.info(f"Agent {agent_id} subscribed to {message_type.value}")
    
    def unsubscribe(self, agent_id: str, message_type: MessageType):
        """Unsubscribe an agent from a message type."""
        if agent_id in self.message_queues:
            self.subscribers[message_type].discard(agent_id)
            self.logger.info(f"Agent {agent_id} unsubscribed from {message_type.value}")
    
    def register_handler(
        self,
        agent_id: str,
        message_type: MessageType,
        handler: Callable[[AgentMessage], Awaitable[None]]
    ):
        """Register a message handler for an agent."""
        if agent_id in self.handlers:
            self.handlers[agent_id][message_type] = handler
            self.logger.info(f"Handler registered for agent {agent_id} on {message_type.value}")
    
    async def publish(self, message: AgentMessage):
        """Publish a message to all subscribed agents."""
        if not self.running:
            raise RuntimeError("MessageBroker is not running")
        
        self.logger.debug(f"Publishing message {message.message_id} of type {message.message_type.value}")
        
        # Get all subscribers for this message type
        subscribers = self.subscribers[message.message_type]
        
        # If message has a specific recipient, only send to that agent
        if message.recipient:
            if message.recipient in subscribers:
                await self._deliver_message(message.recipient, message)
        else:
            # Deliver to all subscribers
            for agent_id in subscribers:
                await self._deliver_message(agent_id, message)
    
    async def _deliver_message(self, agent_id: str, message: AgentMessage):
        """Deliver a message to a specific agent."""
        if agent_id in self.message_queues:
            try:
                # Check if agent has a handler for this message type
                if message.message_type in self.handlers[agent_id]:
                    # Execute handler directly
                    await self.handlers[agent_id][message.message_type](message)
                else:
                    # Queue message for later processing
                    await self.message_queues[agent_id].put(message)
                self.logger.debug(f"Message {message.message_id} delivered to agent {agent_id}")
            except Exception as e:
                self.logger.error(f"Error delivering message to agent {agent_id}: {str(e)}")
    
    async def get_next_message(self, agent_id: str) -> Optional[AgentMessage]:
        """Get the next message for an agent."""
        if agent_id in self.message_queues:
            try:
                return await self.message_queues[agent_id].get()
            except asyncio.CancelledError:
                return None
        return None
    
    def get_queue_size(self, agent_id: str) -> int:
        """Get the current queue size for an agent."""
        if agent_id in self.message_queues:
            return self.message_queues[agent_id].qsize()
        return 0
    
    def get_subscriber_count(self, message_type: MessageType) -> int:
        """Get the number of subscribers for a message type."""
        return len(self.subscribers[message_type])
    
    async def broadcast_status_update(self, agent_id: str, status: str, details: Dict[str, Any]):
        """Broadcast a status update from an agent."""
        from .message_protocol import StatusUpdate
        message = StatusUpdate(
            sender=agent_id,
            recipient="",  # Broadcast to all
            status=status,
            details=details
        )
        await self.publish(message)
    
    async def send_error(self, sender: str, recipient: str, error: str, error_type: str, details: Dict[str, Any]):
        """Send an error message to a specific agent."""
        from .message_protocol import ErrorMessage
        message = ErrorMessage(
            sender=sender,
            recipient=recipient,
            error=error,
            error_type=error_type,
            details=details
        )
        await self.publish(message) 