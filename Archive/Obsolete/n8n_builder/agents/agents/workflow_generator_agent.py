import logging
from typing import Dict, Any, Optional, List
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class WorkflowGeneratorAgent(BaseAgent):
    """Specialized agent for generating detailed workflow descriptions"""
    
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
        self.logger.info("Workflow Generator agent initialized")
    
    async def process(self, input_data: str) -> AgentResult:
        """Process the input description and generate a detailed workflow description"""
        try:
            self.log_operation("Starting workflow description generation", {"input": input_data})
            
            # 1. Analyze the input requirements
            analysis_result = await self._analyze_requirements(input_data)
            if not analysis_result.success:
                return analysis_result
            
            # 2. Generate the workflow description
            description_result = await self._generate_description(analysis_result.data)
            if not description_result.success:
                return description_result
            
            # 3. Validate the description
            validation_result = await self._validate_description(description_result.data)
            if not validation_result.success:
                return validation_result
            
            # 4. Return the final result
            return AgentResult(
                success=True,
                data=validation_result.data,
                metadata={
                    "analysis": analysis_result.metadata,
                    "generation": description_result.metadata,
                    "validation": validation_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _analyze_requirements(self, description: str) -> AgentResult:
        """Analyze the input requirements to identify key components"""
        try:
            system_prompt = """You are an expert at analyzing N8N workflow requirements. Your task is to:
1. Identify the main purpose of the workflow
2. List all required nodes and their purposes
3. Identify any special requirements or constraints
4. Note any potential challenges or considerations

Format your response as a structured analysis with clear sections."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=description
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"analysis_method": "llm", "prompt_type": "requirements_analysis"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_description(self, analysis: str) -> AgentResult:
        """Generate a detailed workflow description based on the analysis"""
        try:
            system_prompt = """You are an expert N8N workflow designer. Based on the analysis, create a detailed workflow description that includes:
1. A clear overview of the workflow purpose
2. Detailed description of each node and its role
3. Specific parameters and settings for each node
4. How nodes connect and pass data between them
5. Any special configurations or considerations

Be specific and detailed, but do not include any JSON or code blocks."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"generation_method": "llm", "prompt_type": "workflow_description"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_description(self, description: str) -> AgentResult:
        """Validate the generated workflow description"""
        try:
            system_prompt = """You are an expert at validating N8N workflow descriptions. Your task is to:
1. Verify all required components are described
2. Check for logical flow and connections
3. Ensure all parameters are properly specified
4. Validate that the description is clear and complete
5. Suggest any improvements if needed

If validation fails, explain the issues in the error field."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=description
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"validation_method": "llm", "prompt_type": "description_validation"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 