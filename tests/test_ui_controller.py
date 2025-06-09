import pytest
import asyncio
from datetime import datetime
from typing import Dict, Any

from n8n_builder.agents.integration.ui_controller import (
    UIController,
    UIEvent,
    UIEventType,
    UIComponent,
    UIComponentType
)

pytestmark = pytest.mark.asyncio

class TestUIController:
    """Test suite for UIController."""
    
    async def test_initialization(self, ui_controller):
        """Test proper initialization of the controller."""
        assert ui_controller is not None
        assert ui_controller.components is not None
        assert ui_controller.event_handlers is not None
        assert ui_controller.config is not None
    
    async def test_component_registration(self, ui_controller):
        """Test component registration functionality."""
        # Create a test component
        component = UIComponent(
            id="test_component",
            type=UIComponentType.BUTTON,
            properties={
                "label": "Test Button",
                "enabled": True
            }
        )
        
        # Register component
        await ui_controller.register_component(component)
        
        # Verify component was registered
        retrieved_component = await ui_controller.get_component("test_component")
        assert retrieved_component is not None
        assert retrieved_component.id == "test_component"
        assert retrieved_component.type == UIComponentType.BUTTON
        assert retrieved_component.properties["label"] == "Test Button"
    
    async def test_component_update(self, ui_controller):
        """Test component update functionality."""
        # Create and register a test component
        component = UIComponent(
            id="test_component",
            type=UIComponentType.BUTTON,
            properties={
                "label": "Test Button",
                "enabled": True
            }
        )
        await ui_controller.register_component(component)
        
        # Update component
        updated_properties = {
            "label": "Updated Button",
            "enabled": False
        }
        await ui_controller.update_component("test_component", updated_properties)
        
        # Verify component was updated
        updated_component = await ui_controller.get_component("test_component")
        assert updated_component.properties["label"] == "Updated Button"
        assert updated_component.properties["enabled"] is False
    
    async def test_event_handling(self, ui_controller):
        """Test event handling functionality."""
        # Create event handlers
        received_events = []
        async def test_handler(event: UIEvent):
            received_events.append(event)
        
        # Register event handler
        await ui_controller.register_event_handler(
            UIEventType.CLICK,
            test_handler
        )
        
        # Create and emit test event
        event = UIEvent(
            type=UIEventType.CLICK,
            component_id="test_component",
            data={"x": 100, "y": 100}
        )
        await ui_controller.emit_event(event)
        
        # Wait for event processing
        await asyncio.sleep(0.1)
        
        # Verify event was handled
        assert len(received_events) == 1
        assert received_events[0].type == UIEventType.CLICK
        assert received_events[0].component_id == "test_component"
    
    async def test_component_visibility(self, ui_controller):
        """Test component visibility control."""
        # Create and register a test component
        component = UIComponent(
            id="test_component",
            type=UIComponentType.PANEL,
            properties={
                "visible": True,
                "content": "Test Content"
            }
        )
        await ui_controller.register_component(component)
        
        # Hide component
        await ui_controller.set_component_visibility("test_component", False)
        
        # Verify component is hidden
        hidden_component = await ui_controller.get_component("test_component")
        assert not hidden_component.properties["visible"]
        
        # Show component
        await ui_controller.set_component_visibility("test_component", True)
        
        # Verify component is visible
        visible_component = await ui_controller.get_component("test_component")
        assert visible_component.properties["visible"]
    
    async def test_component_layout(self, ui_controller):
        """Test component layout management."""
        # Create and register test components
        parent = UIComponent(
            id="parent",
            type=UIComponentType.CONTAINER,
            properties={
                "layout": "vertical",
                "children": []
            }
        )
        child1 = UIComponent(
            id="child1",
            type=UIComponentType.BUTTON,
            properties={"label": "Button 1"}
        )
        child2 = UIComponent(
            id="child2",
            type=UIComponentType.BUTTON,
            properties={"label": "Button 2"}
        )
        
        await ui_controller.register_component(parent)
        await ui_controller.register_component(child1)
        await ui_controller.register_component(child2)
        
        # Add children to parent
        await ui_controller.add_child_component("parent", "child1")
        await ui_controller.add_child_component("parent", "child2")
        
        # Verify layout
        updated_parent = await ui_controller.get_component("parent")
        assert len(updated_parent.properties["children"]) == 2
        assert "child1" in updated_parent.properties["children"]
        assert "child2" in updated_parent.properties["children"]
        
        # Remove child
        await ui_controller.remove_child_component("parent", "child1")
        
        # Verify child was removed
        final_parent = await ui_controller.get_component("parent")
        assert len(final_parent.properties["children"]) == 1
        assert "child1" not in final_parent.properties["children"]
    
    async def test_component_styling(self, ui_controller):
        """Test component styling functionality."""
        # Create and register a test component
        component = UIComponent(
            id="test_component",
            type=UIComponentType.PANEL,
            properties={
                "style": {
                    "backgroundColor": "white",
                    "padding": "10px"
                }
            }
        )
        await ui_controller.register_component(component)
        
        # Update style
        new_style = {
            "backgroundColor": "blue",
            "color": "white",
            "borderRadius": "5px"
        }
        await ui_controller.update_component_style("test_component", new_style)
        
        # Verify style was updated
        updated_component = await ui_controller.get_component("test_component")
        assert updated_component.properties["style"]["backgroundColor"] == "blue"
        assert updated_component.properties["style"]["color"] == "white"
        assert updated_component.properties["style"]["borderRadius"] == "5px"
    
    async def test_component_validation(self, ui_controller):
        """Test component validation functionality."""
        # Create invalid component (missing required property)
        invalid_component = UIComponent(
            id="invalid_component",
            type=UIComponentType.BUTTON,
            properties={}  # Missing label
        )
        
        # Verify component validation fails
        with pytest.raises(Exception):
            await ui_controller.register_component(invalid_component)
    
    async def test_component_cleanup(self, ui_controller):
        """Test component cleanup functionality."""
        # Create and register test components
        component1 = UIComponent(
            id="component1",
            type=UIComponentType.BUTTON,
            properties={"label": "Button 1"}
        )
        component2 = UIComponent(
            id="component2",
            type=UIComponentType.BUTTON,
            properties={"label": "Button 2"}
        )
        
        await ui_controller.register_component(component1)
        await ui_controller.register_component(component2)
        
        # Remove component
        await ui_controller.remove_component("component1")
        
        # Verify component was removed
        with pytest.raises(Exception):
            await ui_controller.get_component("component1")
        
        # Verify other component remains
        assert await ui_controller.get_component("component2") is not None
    
    async def test_start_stop(self, ui_controller):
        """Test starting and stopping the UI controller."""
        # Stop the controller
        await ui_controller.stop()
        
        # Verify controller is stopped
        assert not ui_controller._running
        
        # Start the controller
        await ui_controller.start()
        
        # Verify controller is running
        assert ui_controller._running
        
        # Test component operations after restart
        component = UIComponent(
            id="test_component",
            type=UIComponentType.BUTTON,
            properties={"label": "Test Button"}
        )
        await ui_controller.register_component(component)
        
        retrieved_component = await ui_controller.get_component("test_component")
        assert retrieved_component is not None
        assert retrieved_component.id == "test_component" 