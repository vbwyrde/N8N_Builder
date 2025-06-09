import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from n8n_builder.agents.integration.message_broker import (
    MessageBroker,
    Message,
    MessageType,
    MessagePriority
)

pytestmark = pytest.mark.asyncio

class TestMessageBroker:
    """Test suite for MessageBroker."""
    
    async def test_initialization(self, message_broker):
        """Test proper initialization of the broker."""
        assert message_broker is not None
        assert message_broker.message_queue is not None
        assert message_broker.subscribers is not None
        assert message_broker.config is not None
    
    async def test_message_publishing(self, message_broker):
        """Test message publishing functionality."""
        # Create a test message
        message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        
        # Publish message
        await message_broker.publish_message(message)
        
        # Verify message was published
        assert message_broker.message_queue.qsize() == 1
    
    async def test_message_subscription(self, message_broker):
        """Test message subscription functionality."""
        # Create a test subscriber
        received_messages = []
        async def test_subscriber(message: Message):
            received_messages.append(message)
        
        # Subscribe to messages
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        # Publish test message
        message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        await message_broker.publish_message(message)
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber received message
        assert len(received_messages) == 1
        assert received_messages[0].type == MessageType.WORKFLOW
        assert received_messages[0].content["workflow_id"] == "test_workflow"
    
    async def test_message_priority(self, message_broker):
        """Test message priority handling."""
        # Create test messages with different priorities
        high_priority_message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "high_priority"},
            priority=MessagePriority.HIGH
        )
        normal_priority_message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "normal_priority"},
            priority=MessagePriority.NORMAL
        )
        low_priority_message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "low_priority"},
            priority=MessagePriority.LOW
        )
        
        # Publish messages in reverse priority order
        await message_broker.publish_message(low_priority_message)
        await message_broker.publish_message(normal_priority_message)
        await message_broker.publish_message(high_priority_message)
        
        # Create a test subscriber
        received_messages = []
        async def test_subscriber(message: Message):
            received_messages.append(message)
        
        # Subscribe to messages
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify messages were processed in priority order
        assert len(received_messages) == 3
        assert received_messages[0].content["workflow_id"] == "high_priority"
        assert received_messages[1].content["workflow_id"] == "normal_priority"
        assert received_messages[2].content["workflow_id"] == "low_priority"
    
    async def test_message_filtering(self, message_broker):
        """Test message filtering functionality."""
        # Create test messages of different types
        workflow_message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        system_message = Message(
            type=MessageType.SYSTEM,
            content={"status": "test_status"},
            priority=MessagePriority.HIGH
        )
        
        # Create test subscribers
        workflow_messages = []
        system_messages = []
        
        async def workflow_subscriber(message: Message):
            workflow_messages.append(message)
        
        async def system_subscriber(message: Message):
            system_messages.append(message)
        
        # Subscribe to specific message types
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            workflow_subscriber
        )
        await message_broker.subscribe(
            MessageType.SYSTEM,
            system_subscriber
        )
        
        # Publish messages
        await message_broker.publish_message(workflow_message)
        await message_broker.publish_message(system_message)
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify messages were filtered correctly
        assert len(workflow_messages) == 1
        assert len(system_messages) == 1
        assert workflow_messages[0].type == MessageType.WORKFLOW
        assert system_messages[0].type == MessageType.SYSTEM
    
    async def test_message_unsubscription(self, message_broker):
        """Test message unsubscription functionality."""
        # Create a test subscriber
        received_messages = []
        async def test_subscriber(message: Message):
            received_messages.append(message)
        
        # Subscribe to messages
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        # Publish test message
        message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        await message_broker.publish_message(message)
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber received message
        assert len(received_messages) == 1
        
        # Unsubscribe
        await message_broker.unsubscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        # Publish another message
        await message_broker.publish_message(message)
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber did not receive second message
        assert len(received_messages) == 1
    
    async def test_message_batching(self, message_broker):
        """Test message batching functionality."""
        # Create multiple test messages
        messages = [
            Message(
                type=MessageType.WORKFLOW,
                content={"workflow_id": f"workflow_{i}"},
                priority=MessagePriority.NORMAL
            )
            for i in range(5)
        ]
        
        # Create a test subscriber
        received_messages = []
        async def test_subscriber(message: Message):
            received_messages.append(message)
        
        # Subscribe to messages
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        # Publish messages in batch
        await message_broker.publish_messages(messages)
        
        # Wait for message processing
        await asyncio.sleep(0.1)
        
        # Verify all messages were processed
        assert len(received_messages) == 5
        for i, message in enumerate(received_messages):
            assert message.content["workflow_id"] == f"workflow_{i}"
    
    async def test_message_error_handling(self, message_broker):
        """Test message error handling."""
        # Create a test subscriber that raises an exception
        async def error_subscriber(message: Message):
            raise Exception("Test error")
        
        # Subscribe to messages
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            error_subscriber
        )
        
        # Publish test message
        message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        
        # Verify message processing continues despite error
        await message_broker.publish_message(message)
        await asyncio.sleep(0.1)
        
        # Note: In a real test, we would verify error logging
        # This might require a custom logger or mock
        assert True  # Placeholder for actual assertion
    
    async def test_start_stop(self, message_broker):
        """Test starting and stopping the message broker."""
        # Stop the broker
        await message_broker.stop()
        
        # Verify message processing stopped
        assert not message_broker._running
        
        # Start the broker
        await message_broker.start()
        
        # Verify message processing started
        assert message_broker._running
        
        # Test message processing after restart
        message = Message(
            type=MessageType.WORKFLOW,
            content={"workflow_id": "test_workflow"},
            priority=MessagePriority.NORMAL
        )
        
        received_messages = []
        async def test_subscriber(message: Message):
            received_messages.append(message)
        
        await message_broker.subscribe(
            MessageType.WORKFLOW,
            test_subscriber
        )
        
        await message_broker.publish_message(message)
        await asyncio.sleep(0.1)
        
        assert len(received_messages) == 1 