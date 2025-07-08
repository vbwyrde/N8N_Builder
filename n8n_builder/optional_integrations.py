"""
Optional Integrations Module

This module provides a clean interface for optional advanced components
like Enterprise Module and Enterprise_Database systems. It allows the core N8N_Builder
to work with or without these advanced features.
"""

import logging
import asyncio
from typing import Optional, Any, Dict, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class OptionalComponent(ABC):
    """Base class for optional system components."""
    
    @abstractmethod
    async def start(self) -> bool:
        """Start the component. Returns True if successful."""
        pass
    
    @abstractmethod
    async def stop(self) -> bool:
        """Stop the component. Returns True if successful."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the component is available and functional."""
        pass

class BasicErrorHandler:
    """Basic error handler for public version."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".BasicErrorHandler")
        self.error_count = 0
        
    async def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> bool:
        """Handle an error with basic logging and retry logic."""
        self.error_count += 1
        
        # Log the error
        self.logger.error(f"Error #{self.error_count}: {str(error)}")
        if context:
            self.logger.error(f"Context: {context}")
        
        # Basic retry logic for common issues
        if "connection" in str(error).lower():
            self.logger.info("Connection error detected - implementing basic retry")
            await asyncio.sleep(1)
            return True  # Indicate retry should be attempted
        
        return False  # No retry needed
    
    def get_error_stats(self) -> Dict[str, Any]:
        """Get basic error statistics."""
        return {
            "total_errors": self.error_count,
            "handler_type": "basic"
        }

class OptionalIntegrationManager:
    """Manages optional integrations like Enterprise Module and Enterprise_Database."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__ + ".OptionalIntegrationManager")
        self.components: Dict[str, OptionalComponent] = {}
        self.error_handler = BasicErrorHandler()
        self.advanced_available = False
        
    def register_component(self, name: str, component: OptionalComponent):
        """Register an optional component."""
        self.components[name] = component
        self.logger.info(f"Registered optional component: {name}")
    
    async def start_all(self) -> Dict[str, bool]:
        """Start all registered components."""
        results = {}
        
        for name, component in self.components.items():
            try:
                success = await component.start()
                results[name] = success
                if success:
                    self.logger.info(f"Started optional component: {name}")
                else:
                    self.logger.warning(f"Failed to start optional component: {name}")
            except Exception as e:
                self.logger.error(f"Error starting component {name}: {e}")
                results[name] = False
        
        return results
    
    async def stop_all(self) -> Dict[str, bool]:
        """Stop all registered components."""
        results = {}
        
        for name, component in self.components.items():
            try:
                success = await component.stop()
                results[name] = success
                if success:
                    self.logger.info(f"Stopped optional component: {name}")
                else:
                    self.logger.warning(f"Failed to stop optional component: {name}")
            except Exception as e:
                self.logger.error(f"Error stopping component {name}: {e}")
                results[name] = False
        
        return results
    
    def get_component(self, name: str) -> Optional[OptionalComponent]:
        """Get a registered component by name."""
        return self.components.get(name)
    
    def is_component_available(self, name: str) -> bool:
        """Check if a component is available and functional."""
        component = self.components.get(name)
        return component is not None and component.is_available()
    
    async def handle_error(self, error: Exception, context: Dict[str, Any] = None) -> bool:
        """Handle an error using available error handling components."""
        
        # Try advanced error handler first (if available)
        advanced_handler = self.get_component("Enterprise_Module")
        if advanced_handler and advanced_handler.is_available():
            try:
                # Advanced error handling would go here
                self.logger.info("Using advanced error handling")
                return await self._handle_with_advanced(error, context, advanced_handler)
            except Exception as e:
                self.logger.warning(f"Advanced error handling failed: {e}, falling back to basic")
        
        # Fall back to basic error handling
        return await self.error_handler.handle_error(error, context)
    
    async def _handle_with_advanced(self, error: Exception, context: Dict[str, Any], handler: OptionalComponent) -> bool:
        """Handle error with advanced component (placeholder for private implementation)."""
        # This would be implemented by the advanced component
        # For public version, we just log and use basic handling
        self.logger.info("Advanced error handling not implemented in community edition")
        return await self.error_handler.handle_error(error, context)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get status of all optional components."""
        status = {
            "basic_error_handler": self.error_handler.get_error_stats(),
            "optional_components": {}
        }
        
        for name, component in self.components.items():
            status["optional_components"][name] = {
                "available": component.is_available(),
                "type": type(component).__name__
            }
        
        return status

# Global instance for the application
integration_manager = OptionalIntegrationManager()

def get_integration_manager() -> OptionalIntegrationManager:
    """Get the global integration manager instance."""
    return integration_manager

def try_import_advanced_components() -> bool:
    """
    Try to import and register advanced components.
    Returns True if any advanced components were loaded.
    """
    advanced_loaded = False
    
    # Try to import Enterprise Module (private component)
    try:
        # This import will fail in public version - that's expected
        from Enterprise_Module.core.healer_manager import EnterpriseModuleManager
        
        class EnterpriseModuleComponent(OptionalComponent):
            def __init__(self):
                self.healer = EnterpriseModuleManager()
                self.running = False
            
            async def start(self) -> bool:
                try:
                    await self.healer.start()
                    self.running = True
                    return True
                except Exception:
                    return False
            
            async def stop(self) -> bool:
                try:
                    await self.healer.stop()
                    self.running = False
                    return True
                except Exception:
                    return False
            
            def is_available(self) -> bool:
                return self.running
        
        integration_manager.register_component("Enterprise_Module", EnterpriseModuleComponent())
        integration_manager.advanced_available = True
        advanced_loaded = True
        logger.info("✅ Advanced Enterprise Module component loaded")
        
    except ImportError:
        logger.info("ℹ️ Advanced Enterprise Module component not available (Community Edition)")
    except Exception as e:
        logger.warning(f"⚠️ Error loading Enterprise Module component: {e}")
    
    # Try to import Enterprise_Database (private component)
    try:
        # This import will fail in public version - that's expected
        from Enterprise_Module.core.knowledge_integration import EnterpriseDatabaseIntegrator
        
        class Enterprise_DatabaseComponent(OptionalComponent):
            def __init__(self):
                self.kb = EnterpriseDatabaseIntegrator()
                self.running = False
            
            async def start(self) -> bool:
                try:
                    # Initialize knowledge base connection
                    self.running = True
                    return True
                except Exception:
                    return False
            
            async def stop(self) -> bool:
                try:
                    self.running = False
                    return True
                except Exception:
                    return False
            
            def is_available(self) -> bool:
                return self.running
        
        integration_manager.register_component("Enterprise_Database", Enterprise_DatabaseComponent())
        advanced_loaded = True
        logger.info("✅ Advanced Enterprise_Database component loaded")
        
    except ImportError:
        logger.info("ℹ️ Advanced Enterprise_Database component not available (Community Edition)")
    except Exception as e:
        logger.warning(f"⚠️ Error loading Enterprise_Database component: {e}")
    
    return advanced_loaded
