import logging
import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class ValidationAgent(BaseAgent):
    """Specialized agent for validating n8n workflow JSON structures"""
    
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
        self.logger.info("Validation agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and validate the workflow JSON"""
        try:
            self.log_operation("Starting workflow validation", {"input_type": type(input_data).__name__})
            
            # 1. Validate basic structure
            structure_result = await self._validate_basic_structure(input_data)
            if not structure_result.success:
                return structure_result
            
            # 2. Validate nodes
            nodes_result = await self._validate_nodes(structure_result.data)
            if not nodes_result.success:
                return nodes_result
            
            # 3. Validate connections
            connections_result = await self._validate_connections(nodes_result.data)
            if not connections_result.success:
                return connections_result
            
            # 4. Validate node parameters
            parameters_result = await self._validate_node_parameters(connections_result.data)
            if not parameters_result.success:
                return parameters_result
            
            # 5. Return the final validated result
            return AgentResult(
                success=True,
                data=parameters_result.data,
                metadata={
                    "structure": structure_result.metadata,
                    "nodes": nodes_result.metadata,
                    "connections": connections_result.metadata,
                    "parameters": parameters_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_basic_structure(self, workflow: Dict[str, Any]) -> AgentResult:
        """Validate the basic structure of the workflow JSON"""
        try:
            system_prompt = """You are an expert at validating n8n workflow structure. Your task is to:
1. Verify the workflow has the required top-level fields (nodes, connections)
2. Check that nodes is an array
3. Check that connections is an object
4. Return the validated workflow

If validation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the validated workflow
            try:
                validated_workflow = json.loads(response)
                return AgentResult(
                    success=True,
                    data=validated_workflow,
                    metadata={"validation_method": "llm", "prompt_type": "basic_structure"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse validated workflow: {str(e)}",
                    metadata={"validation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_nodes(self, workflow: Dict[str, Any]) -> AgentResult:
        """Validate the nodes in the workflow"""
        try:
            system_prompt = """You are an expert at validating n8n workflow nodes. Your task is to:
1. Verify each node has required fields (name, type, typeVersion, position, parameters)
2. Check that node types are valid n8n node types
3. Ensure node names are unique
4. Validate position coordinates are numbers
5. Return the validated workflow

If validation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the validated workflow
            try:
                validated_workflow = json.loads(response)
                return AgentResult(
                    success=True,
                    data=validated_workflow,
                    metadata={"validation_method": "llm", "prompt_type": "nodes"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse validated workflow: {str(e)}",
                    metadata={"validation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_connections(self, workflow: Dict[str, Any]) -> AgentResult:
        """Validate the connections between nodes"""
        try:
            system_prompt = """You are an expert at validating n8n workflow connections. Your task is to:
1. Verify connections reference valid node names
2. Check that connection types are valid (inputData, outputData)
3. Ensure connection indices are valid
4. Validate that connections form a valid workflow graph
5. Return the validated workflow

If validation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the validated workflow
            try:
                validated_workflow = json.loads(response)
                return AgentResult(
                    success=True,
                    data=validated_workflow,
                    metadata={"validation_method": "llm", "prompt_type": "connections"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse validated workflow: {str(e)}",
                    metadata={"validation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_node_parameters(self, workflow: Dict[str, Any]) -> AgentResult:
        """Validate the parameters of each node"""
        try:
            system_prompt = """You are an expert at validating n8n node parameters. Your task is to:
1. Verify parameters match the node type requirements
2. Check that required parameters are present
3. Validate parameter value types
4. Ensure parameter values are within valid ranges
5. Return the validated workflow

If validation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the validated workflow
            try:
                validated_workflow = json.loads(response)
                return AgentResult(
                    success=True,
                    data=validated_workflow,
                    metadata={"validation_method": "llm", "prompt_type": "parameters"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse validated workflow: {str(e)}",
                    metadata={"validation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 