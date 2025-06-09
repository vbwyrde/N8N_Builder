import pytest
import asyncio
from typing import Dict, Any, List

from ..agents.integration.workflow_step_executor import (
    WorkflowStepExecutor,
    WorkflowStepExecutionResult,
    WorkflowStepExecutionError
)

pytestmark = pytest.mark.asyncio

class TestWorkflowStepExecutor:
    """Test suite for WorkflowStepExecutor."""
    
    def test_initialization(self):
        """Test proper initialization of step executor."""
        executor = WorkflowStepExecutor()
        assert executor is not None
    
    @pytest.mark.asyncio
    async def test_execute_step(self):
        """Test executing a step."""
        executor = WorkflowStepExecutor()
        
        # Test successful execution
        step_type = {
            "name": "test_step",
            "description": "Test step type",
            "version": "1.0.0",
            "category": "test",
            "inputs": {
                "input1": {
                    "type": "string",
                    "required": True
                }
            },
            "outputs": {
                "output1": {
                    "type": "string"
                }
            },
            "parameters": {
                "param1": {
                    "type": "number",
                    "required": True
                }
            }
        }
        
        inputs = {
            "input1": "test value"
        }
        
        parameters = {
            "param1": 42
        }
        
        result = await executor.execute_step(
            step_id="step1",
            step_type=step_type,
            inputs=inputs,
            parameters=parameters
        )
        
        assert result.is_success
        assert result.step_id == "step1"
        assert result.outputs["output1"] == "test value"
        assert result.metadata["execution_time"] > 0
    
    @pytest.mark.asyncio
    async def test_execute_step_with_error(self):
        """Test executing a step that raises an error."""
        executor = WorkflowStepExecutor()
        
        # Test execution with error
        step_type = {
            "name": "error_step",
            "description": "Step that raises an error",
            "version": "1.0.0",
            "category": "test",
            "inputs": {},
            "outputs": {},
            "parameters": {}
        }
        
        result = await executor.execute_step(
            step_id="step1",
            step_type=step_type,
            inputs={},
            parameters={}
        )
        
        assert not result.is_success
        assert result.step_id == "step1"
        assert result.error is not None
        assert "Error executing step" in result.error.message
    
    @pytest.mark.asyncio
    async def test_execute_step_with_timeout(self):
        """Test executing a step that times out."""
        executor = WorkflowStepExecutor()
        
        # Test execution with timeout
        step_type = {
            "name": "timeout_step",
            "description": "Step that times out",
            "version": "1.0.0",
            "category": "test",
            "inputs": {},
            "outputs": {},
            "parameters": {},
            "timeout": 1
        }
        
        result = await executor.execute_step(
            step_id="step1",
            step_type=step_type,
            inputs={},
            parameters={}
        )
        
        assert not result.is_success
        assert result.step_id == "step1"
        assert result.error is not None
        assert "Timeout" in result.error.message
    
    @pytest.mark.asyncio
    async def test_execute_step_with_invalid_inputs(self):
        """Test executing a step with invalid inputs."""
        executor = WorkflowStepExecutor()
        
        # Test execution with invalid inputs
        step_type = {
            "name": "test_step",
            "description": "Test step type",
            "version": "1.0.0",
            "category": "test",
            "inputs": {
                "input1": {
                    "type": "string",
                    "required": True
                }
            },
            "outputs": {},
            "parameters": {}
        }
        
        result = await executor.execute_step(
            step_id="step1",
            step_type=step_type,
            inputs={},
            parameters={}
        )
        
        assert not result.is_success
        assert result.step_id == "step1"
        assert result.error is not None
        assert "input1" in result.error.message
    
    @pytest.mark.asyncio
    async def test_execute_step_with_invalid_parameters(self):
        """Test executing a step with invalid parameters."""
        executor = WorkflowStepExecutor()
        
        # Test execution with invalid parameters
        step_type = {
            "name": "test_step",
            "description": "Test step type",
            "version": "1.0.0",
            "category": "test",
            "inputs": {},
            "outputs": {},
            "parameters": {
                "param1": {
                    "type": "number",
                    "required": True
                }
            }
        }
        
        result = await executor.execute_step(
            step_id="step1",
            step_type=step_type,
            inputs={},
            parameters={}
        )
        
        assert not result.is_success
        assert result.step_id == "step1"
        assert result.error is not None
        assert "param1" in result.error.message

class TestWorkflowStepExecutionResult:
    """Test suite for WorkflowStepExecutionResult."""
    
    def test_initialization(self):
        """Test proper initialization of execution result."""
        result = WorkflowStepExecutionResult(
            step_id="step1",
            is_success=True,
            outputs={
                "output1": "test value"
            },
            metadata={
                "execution_time": 0.1
            }
        )
        
        assert result.step_id == "step1"
        assert result.is_success
        assert result.outputs["output1"] == "test value"
        assert result.metadata["execution_time"] == 0.1
        assert result.error is None
    
    def test_initialization_with_error(self):
        """Test proper initialization of execution result with error."""
        error = WorkflowStepExecutionError(
            message="Test error message",
            code="TEST_ERROR",
            details={
                "field": "test_field",
                "value": "test_value"
            }
        )
        
        result = WorkflowStepExecutionResult(
            step_id="step1",
            is_success=False,
            error=error
        )
        
        assert result.step_id == "step1"
        assert not result.is_success
        assert result.error.message == "Test error message"
        assert result.error.code == "TEST_ERROR"
        assert result.error.details["field"] == "test_field"
        assert result.error.details["value"] == "test_value"
    
    def test_to_dict(self):
        """Test converting execution result to dictionary."""
        error = WorkflowStepExecutionError(
            message="Test error message",
            code="TEST_ERROR",
            details={
                "field": "test_field",
                "value": "test_value"
            }
        )
        
        result = WorkflowStepExecutionResult(
            step_id="step1",
            is_success=False,
            error=error,
            outputs={
                "output1": "test value"
            },
            metadata={
                "execution_time": 0.1
            }
        )
        
        data = result.to_dict()
        assert data["step_id"] == "step1"
        assert data["is_success"] is False
        assert data["outputs"]["output1"] == "test value"
        assert data["metadata"]["execution_time"] == 0.1
        assert data["error"]["message"] == "Test error message"
        assert data["error"]["code"] == "TEST_ERROR"
        assert data["error"]["details"]["field"] == "test_field"
        assert data["error"]["details"]["value"] == "test_value"

class TestWorkflowStepExecutionError:
    """Test suite for WorkflowStepExecutionError."""
    
    def test_initialization(self):
        """Test proper initialization of execution error."""
        error = WorkflowStepExecutionError(
            message="Test error message",
            code="TEST_ERROR",
            details={
                "field": "test_field",
                "value": "test_value"
            }
        )
        
        assert error.message == "Test error message"
        assert error.code == "TEST_ERROR"
        assert error.details["field"] == "test_field"
        assert error.details["value"] == "test_value"
    
    def test_to_dict(self):
        """Test converting execution error to dictionary."""
        error = WorkflowStepExecutionError(
            message="Test error message",
            code="TEST_ERROR",
            details={
                "field": "test_field",
                "value": "test_value"
            }
        )
        
        data = error.to_dict()
        assert data["message"] == "Test error message"
        assert data["code"] == "TEST_ERROR"
        assert data["details"]["field"] == "test_field"
        assert data["details"]["value"] == "test_value"
    
    def test_str_representation(self):
        """Test string representation of execution error."""
        error = WorkflowStepExecutionError(
            message="Test error message",
            code="TEST_ERROR",
            details={
                "field": "test_field",
                "value": "test_value"
            }
        )
        
        error_str = str(error)
        assert "Test error message" in error_str
        assert "TEST_ERROR" in error_str
        assert "test_field" in error_str
        assert "test_value" in error_str 