import logging
from typing import Dict, Any, Optional
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class OrchestratorAgent(BaseAgent):
    """Orchestrates the workflow generation process by coordinating other agents"""
    
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
        self.logger.info("Orchestrator agent initialized")
    
    async def process(self, input_data: str) -> AgentResult:
        """Process the input description and coordinate workflow generation"""
        try:
            self.log_operation("Starting workflow generation", {"input": input_data})
            
            # 1. Generate workflow description
            workflow_result = await self._generate_workflow(input_data)
            if not workflow_result.success:
                return workflow_result
            
            # 2. Extract JSON from the description
            json_result = await self._extract_json(workflow_result.data)
            if not json_result.success:
                return json_result
            
            # 3. Validate the workflow
            validation_result = await self._validate_workflow(json_result.data)
            if not validation_result.success:
                return validation_result
            
            # 4. Return the final result
            return AgentResult(
                success=True,
                data=validation_result.data,
                metadata={
                    "workflow_generation": workflow_result.metadata,
                    "json_extraction": json_result.metadata,
                    "validation": validation_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_workflow(self, description: str) -> AgentResult:
        """Generate a workflow description using the LLM"""
        try:
            system_prompt = """You are an expert N8N workflow generator. Your task is to describe the workflow in natural language, including:
1. The nodes needed
2. Their connections
3. Required parameters
4. Any special considerations

Focus on being clear and detailed in your description. Do not include JSON or code blocks."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=description
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"generation_method": "llm", "prompt_type": "workflow_description"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _extract_json(self, description: str) -> AgentResult:
        """Extract JSON from the workflow description"""
        try:
            system_prompt = """You are an expert at extracting structured data from text. Your task is to:
1. Find any JSON in the text
2. Clean and normalize it
3. Ensure it's valid JSON
4. Return ONLY the JSON, no other text

If no valid JSON is found, return an empty object {}."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=description
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"extraction_method": "llm", "prompt_type": "json_extraction"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_workflow(self, workflow_json: str) -> AgentResult:
        """Validate the workflow JSON structure"""
        try:
            system_prompt = """You are an expert at validating N8N workflows. Your task is to:
1. Verify the JSON structure
2. Check for required fields (nodes, connections)
3. Validate node types and parameters
4. Ensure proper connections
5. Return the validated workflow

If validation fails, explain the issues in the error field."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_json
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"validation_method": "llm", "prompt_type": "workflow_validation"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 