import logging
import json
import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class WorkflowExecutorAgent(BaseAgent):
    """Specialized agent for executing n8n workflows and managing their state"""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.llm_client = LLMClient(
            endpoint=config.llm_endpoint,
            model=config.llm_model,
            temperature=config.llm_temperature,
            max_tokens=config.llm_max_tokens,
            timeout=config.llm_timeout,
            api_key=config.api_key,
            is_local=config.is_local
        )
        self.active_workflows: Dict[str, Dict[str, Any]] = {}
        self.logger.info("Workflow Executor agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and execute the workflow"""
        try:
            self.log_operation("Starting workflow execution", {"input_type": type(input_data).__name__})
            
            # 1. Prepare workflow for execution
            preparation_result = await self._prepare_workflow(input_data)
            if not preparation_result.success:
                return preparation_result
            
            # 2. Initialize workflow state
            init_result = await self._initialize_workflow_state(preparation_result.data)
            if not init_result.success:
                return init_result
            
            # 3. Execute workflow
            execution_result = await self._execute_workflow(init_result.data)
            if not execution_result.success:
                return execution_result
            
            # 4. Monitor execution
            monitoring_result = await self._monitor_execution(execution_result.data)
            if not monitoring_result.success:
                return monitoring_result
            
            # 5. Return the final execution result
            return AgentResult(
                success=True,
                data=monitoring_result.data,
                metadata={
                    "preparation": preparation_result.metadata,
                    "initialization": init_result.metadata,
                    "execution": execution_result.metadata,
                    "monitoring": monitoring_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _prepare_workflow(self, workflow: Dict[str, Any]) -> AgentResult:
        """Prepare the workflow for execution"""
        try:
            system_prompt = """You are an expert at preparing n8n workflows for execution. Your task is to:
1. Verify all required node configurations
2. Check for any missing credentials or connections
3. Validate execution prerequisites
4. Return the prepared workflow

If preparation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the prepared workflow
            try:
                prepared_workflow = json.loads(response)
                return AgentResult(
                    success=True,
                    data=prepared_workflow,
                    metadata={"preparation_method": "llm", "prompt_type": "workflow_preparation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse prepared workflow: {str(e)}",
                    metadata={"preparation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _initialize_workflow_state(self, workflow: Dict[str, Any]) -> AgentResult:
        """Initialize the workflow execution state"""
        try:
            workflow_id = workflow.get("id", "default")
            self.active_workflows[workflow_id] = {
                "workflow": workflow,
                "status": "initializing",
                "current_node": None,
                "execution_history": [],
                "start_time": None,
                "end_time": None,
                "error": None
            }
            
            return AgentResult(
                success=True,
                data=workflow,
                metadata={
                    "workflow_id": workflow_id,
                    "status": "initialized",
                    "active_workflows_count": len(self.active_workflows)
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _execute_workflow(self, workflow: Dict[str, Any]) -> AgentResult:
        """Execute the workflow"""
        try:
            workflow_id = workflow.get("id", "default")
            workflow_state = self.active_workflows[workflow_id]
            workflow_state["status"] = "executing"
            workflow_state["start_time"] = asyncio.get_event_loop().time()
            
            system_prompt = """You are an expert at executing n8n workflows. Your task is to:
1. Execute each node in the correct order
2. Handle node execution results
3. Manage data flow between nodes
4. Return the execution results

If execution fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the execution results
            try:
                execution_results = json.loads(response)
                workflow_state["execution_history"].append(execution_results)
                return AgentResult(
                    success=True,
                    data=execution_results,
                    metadata={
                        "workflow_id": workflow_id,
                        "status": "executed",
                        "execution_time": asyncio.get_event_loop().time() - workflow_state["start_time"]
                    }
                )
            except json.JSONDecodeError as e:
                workflow_state["error"] = str(e)
                workflow_state["status"] = "error"
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse execution results: {str(e)}",
                    metadata={"workflow_id": workflow_id, "status": "error"}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _monitor_execution(self, execution_results: Dict[str, Any]) -> AgentResult:
        """Monitor the workflow execution"""
        try:
            workflow_id = execution_results.get("workflow_id", "default")
            workflow_state = self.active_workflows[workflow_id]
            workflow_state["status"] = "monitoring"
            
            system_prompt = """You are an expert at monitoring n8n workflow execution. Your task is to:
1. Check execution status
2. Monitor node performance
3. Track data flow
4. Return the monitoring results

If monitoring fails, explain the issues in the error field."""
            
            # Convert execution results to string for LLM processing
            results_str = json.dumps(execution_results, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=results_str
            )
            
            # Parse the monitoring results
            try:
                monitoring_results = json.loads(response)
                workflow_state["end_time"] = asyncio.get_event_loop().time()
                workflow_state["status"] = "completed"
                return AgentResult(
                    success=True,
                    data=monitoring_results,
                    metadata={
                        "workflow_id": workflow_id,
                        "status": "completed",
                        "total_execution_time": workflow_state["end_time"] - workflow_state["start_time"]
                    }
                )
            except json.JSONDecodeError as e:
                workflow_state["error"] = str(e)
                workflow_state["status"] = "error"
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse monitoring results: {str(e)}",
                    metadata={"workflow_id": workflow_id, "status": "error"}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get the current status of a workflow"""
        return self.active_workflows.get(workflow_id, {
            "status": "not_found",
            "error": f"Workflow {workflow_id} not found"
        })
    
    async def stop_workflow(self, workflow_id: str) -> bool:
        """Stop a running workflow"""
        if workflow_id in self.active_workflows:
            workflow_state = self.active_workflows[workflow_id]
            workflow_state["status"] = "stopped"
            workflow_state["end_time"] = asyncio.get_event_loop().time()
            return True
        return False
    
    async def close(self):
        """Clean up resources"""
        # Stop all active workflows
        for workflow_id in list(self.active_workflows.keys()):
            await self.stop_workflow(workflow_id)
        await self.llm_client.close() 