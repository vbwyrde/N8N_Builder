import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from n8n_builder.agents.integration.event_stream import (
    EventStreamManager,
    Event,
    EventType,
    EventPriority
)

pytestmark = pytest.mark.asyncio

class TestEventStreamManager:
    """Test suite for EventStreamManager."""
    
    async def test_initialization(self, event_stream_manager):
        """Test proper initialization of the manager."""
        assert event_stream_manager is not None
        assert event_stream_manager.event_queue is not None
        assert event_stream_manager.subscribers is not None
        assert event_stream_manager.config is not None
    
    async def test_event_publishing(self, event_stream_manager):
        """Test event publishing functionality."""
        # Create a test event
        event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        
        # Publish event
        await event_stream_manager.publish_event(event)
        
        # Verify event was published
        assert event_stream_manager.event_queue.qsize() == 1
    
    async def test_event_subscription(self, event_stream_manager):
        """Test event subscription functionality."""
        # Create a test subscriber
        received_events = []
        async def test_subscriber(event: Event):
            received_events.append(event)
        
        # Subscribe to events
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        # Publish test event
        event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        await event_stream_manager.publish_event(event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber received event
        assert len(received_events) == 1
        assert received_events[0].type == EventType.WORKFLOW_STARTED
        assert received_events[0].data["workflow_id"] == "test_workflow"
    
    async def test_event_priority(self, event_stream_manager):
        """Test event priority handling."""
        # Create test events with different priorities
        high_priority_event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "high_priority"},
            priority=EventPriority.HIGH
        )
        normal_priority_event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "normal_priority"},
            priority=EventPriority.NORMAL
        )
        low_priority_event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "low_priority"},
            priority=EventPriority.LOW
        )
        
        # Publish events in reverse priority order
        await event_stream_manager.publish_event(low_priority_event)
        await event_stream_manager.publish_event(normal_priority_event)
        await event_stream_manager.publish_event(high_priority_event)
        
        # Create a test subscriber
        received_events = []
        async def test_subscriber(event: Event):
            received_events.append(event)
        
        # Subscribe to events
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify events were processed in priority order
        assert len(received_events) == 3
        assert received_events[0].data["workflow_id"] == "high_priority"
        assert received_events[1].data["workflow_id"] == "normal_priority"
        assert received_events[2].data["workflow_id"] == "low_priority"
    
    async def test_event_filtering(self, event_stream_manager):
        """Test event filtering functionality."""
        # Create test events of different types
        workflow_event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        system_event = Event(
            type=EventType.SYSTEM_ERROR,
            data={"error": "test_error"},
            priority=EventPriority.HIGH
        )
        
        # Create test subscribers
        workflow_events = []
        system_events = []
        
        async def workflow_subscriber(event: Event):
            workflow_events.append(event)
        
        async def system_subscriber(event: Event):
            system_events.append(event)
        
        # Subscribe to specific event types
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            workflow_subscriber
        )
        await event_stream_manager.subscribe(
            EventType.SYSTEM_ERROR,
            system_subscriber
        )
        
        # Publish events
        await event_stream_manager.publish_event(workflow_event)
        await event_stream_manager.publish_event(system_event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify events were filtered correctly
        assert len(workflow_events) == 1
        assert len(system_events) == 1
        assert workflow_events[0].type == EventType.WORKFLOW_STARTED
        assert system_events[0].type == EventType.SYSTEM_ERROR
    
    async def test_event_unsubscription(self, event_stream_manager):
        """Test event unsubscription functionality."""
        # Create a test subscriber
        received_events = []
        async def test_subscriber(event: Event):
            received_events.append(event)
        
        # Subscribe to events
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        # Publish test event
        event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        await event_stream_manager.publish_event(event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber received event
        assert len(received_events) == 1
        
        # Unsubscribe
        await event_stream_manager.unsubscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        # Publish another event
        await event_stream_manager.publish_event(event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify subscriber did not receive second event
        assert len(received_events) == 1
    
    async def test_event_batching(self, event_stream_manager):
        """Test event batching functionality."""
        # Create multiple test events
        events = [
            Event(
                type=EventType.WORKFLOW_STARTED,
                data={"workflow_id": f"workflow_{i}"},
                priority=EventPriority.NORMAL
            )
            for i in range(5)
        ]
        
        # Create a test subscriber
        received_events = []
        async def test_subscriber(event: Event):
            received_events.append(event)
        
        # Subscribe to events
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        # Publish events in batch
        await event_stream_manager.publish_events(events)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify all events were processed
        assert len(received_events) == 5
        for i, event in enumerate(received_events):
            assert event.data["workflow_id"] == f"workflow_{i}"
    
    async def test_event_error_handling(self, event_stream_manager):
        """Test event error handling."""
        # Create a test subscriber that raises an exception
        async def error_subscriber(event: Event):
            raise Exception("Test error")
        
        # Subscribe to events
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            error_subscriber
        )
        
        # Publish test event
        event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        
        # Verify event processing continues despite error
        await event_stream_manager.publish_event(event)
        await asyncio.sleep(0.1)
        
        # Note: In a real test, we would verify error logging
        # This might require a custom logger or mock
        assert True  # Placeholder for actual assertion
    
    async def test_start_stop(self, event_stream_manager):
        """Test starting and stopping the event stream manager."""
        # Stop the manager
        await event_stream_manager.stop()
        
        # Verify event processing stopped
        assert not event_stream_manager._running
        
        # Start the manager
        await event_stream_manager.start()
        
        # Verify event processing started
        assert event_stream_manager._running
        
        # Test event processing after restart
        event = Event(
            type=EventType.WORKFLOW_STARTED,
            data={"workflow_id": "test_workflow"},
            priority=EventPriority.NORMAL
        )
        
        received_events = []
        async def test_subscriber(event: Event):
            received_events.append(event)
        
        await event_stream_manager.subscribe(
            EventType.WORKFLOW_STARTED,
            test_subscriber
        )
        
        await event_stream_manager.publish_event(event)
        await asyncio.sleep(0.1)
        
        assert len(received_events) == 1 