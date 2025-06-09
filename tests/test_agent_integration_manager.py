import pytest
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any

from n8n_builder.agents.integration.agent_integration_manager import (
    AgentIntegrationManager,
    WorkflowPriority,
    WorkflowTask
)
from n8n_builder.agents.integration.security import SecurityError, AuthorizationError
from n8n_builder.agents.integration.error_recovery import CircuitState

pytestmark = pytest.mark.asyncio

class TestAgentIntegrationManager:
    """Test suite for AgentIntegrationManager."""
    
    async def test_initialization(self, agent_integration_manager):
        """Test proper initialization of the manager."""
        assert agent_integration_manager is not None
        assert agent_integration_manager.agents is not None
        assert agent_integration_manager.agent_states is not None
        assert agent_integration_manager.active_workflows is not None
    
    async def test_workflow_processing(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test workflow processing functionality."""
        # Process workflow
        result = await agent_integration_manager.process_workflow(sample_workflow_data, test_token)
        
        assert result is not None
        assert result.success is True
        assert result.error is None
        
        # Verify workflow state
        workflow_id = sample_workflow_data['workflow_id']
        state = await agent_integration_manager.state_manager.get_state(f"workflow_{workflow_id}")
        assert state is not None
        assert state['status'] == 'completed'
    
    async def test_workflow_processing_without_auth(self, agent_integration_manager, sample_workflow_data):
        """Test workflow processing without authentication."""
        with pytest.raises(AuthorizationError):
            await agent_integration_manager.process_workflow(sample_workflow_data)
    
    async def test_workflow_processing_invalid_data(self, agent_integration_manager, test_token):
        """Test workflow processing with invalid data."""
        invalid_data = {'invalid': 'data'}
        
        with pytest.raises(SecurityError):
            await agent_integration_manager.process_workflow(invalid_data, test_token)
    
    async def test_workflow_status(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test workflow status retrieval."""
        # Process workflow first
        await agent_integration_manager.process_workflow(sample_workflow_data, test_token)
        
        # Get status
        status = await agent_integration_manager.get_workflow_status(
            sample_workflow_data['workflow_id'],
            test_token
        )
        
        assert status is not None
        assert 'status' in status
        assert 'priority' in status
        assert 'assigned_agent' in status
    
    async def test_parallel_workflow_processing(
        self,
        agent_integration_manager,
        sample_workflow_data,
        test_token
    ):
        """Test parallel processing of multiple workflows."""
        # Create multiple workflows
        workflows = []
        for i in range(3):
            workflow = sample_workflow_data.copy()
            workflow['workflow_id'] = f"test_workflow_{i}_{datetime.now().timestamp()}"
            workflows.append(workflow)
        
        # Process workflows in parallel
        tasks = [
            agent_integration_manager.process_workflow(workflow, test_token)
            for workflow in workflows
        ]
        results = await asyncio.gather(*tasks)
        
        # Verify results
        assert len(results) == 3
        assert all(result.success for result in results)
    
    async def test_workflow_priority(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test workflow priority handling."""
        # Create workflows with different priorities
        high_priority = sample_workflow_data.copy()
        high_priority['workflow_id'] = f"high_priority_{datetime.now().timestamp()}"
        
        low_priority = sample_workflow_data.copy()
        low_priority['workflow_id'] = f"low_priority_{datetime.now().timestamp()}"
        
        # Process workflows
        await agent_integration_manager.process_workflow_parallel(
            high_priority,
            WorkflowPriority.HIGH,
            test_token
        )
        await agent_integration_manager.process_workflow_parallel(
            low_priority,
            WorkflowPriority.LOW,
            test_token
        )
        
        # Verify priority queue
        assert len(agent_integration_manager.workflow_queue[WorkflowPriority.HIGH]) > 0
        assert len(agent_integration_manager.workflow_queue[WorkflowPriority.LOW]) > 0
    
    async def test_error_handling(self, agent_integration_manager, test_token):
        """Test error handling in workflow processing."""
        # Create workflow that will fail
        failing_workflow = {
            'workflow_id': f"failing_workflow_{datetime.now().timestamp()}",
            'name': 'Failing Workflow',
            'nodes': [
                {
                    'id': 'node1',
                    'type': 'error',
                    'position': {'x': 0, 'y': 0}
                }
            ],
            'edges': []
        }
        
        # Process workflow
        result = await agent_integration_manager.process_workflow(failing_workflow, test_token)
        
        assert result is not None
        assert result.success is False
        assert result.error is not None
    
    async def test_resource_management(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test resource management during workflow processing."""
        # Process workflow
        await agent_integration_manager.process_workflow(sample_workflow_data, test_token)
        
        # Check resource usage
        for agent, usage in agent_integration_manager.current_resources.items():
            assert usage <= agent_integration_manager.resource_limits.get(agent, float('inf'))
    
    async def test_health_status(self, agent_integration_manager):
        """Test health status retrieval."""
        health = await agent_integration_manager.get_health_status()
        
        assert health is not None
        assert 'system' in health
        assert 'agents' in health
        assert 'workflows' in health
        assert 'timestamp' in health
    
    async def test_metrics_collection(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test metrics collection during workflow processing."""
        # Process workflow
        await agent_integration_manager.process_workflow(sample_workflow_data, test_token)
        
        # Get metrics
        metrics = await agent_integration_manager.get_metrics()
        
        assert metrics is not None
        assert 'workflow.started' in metrics
        assert 'workflow.completed' in metrics
        assert 'workflow.processing_time' in metrics
    
    async def test_cleanup(self, agent_integration_manager, sample_workflow_data, test_token):
        """Test cleanup of completed workflows."""
        # Process workflow
        await agent_integration_manager.process_workflow(sample_workflow_data, test_token)
        
        # Wait for cleanup
        await asyncio.sleep(2)
        
        # Verify cleanup
        workflow_id = sample_workflow_data['workflow_id']
        state = await agent_integration_manager.state_manager.get_state(f"workflow_{workflow_id}")
        assert state is not None
        assert state['status'] in ['completed', 'failed'] 