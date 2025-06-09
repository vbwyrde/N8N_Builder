import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class WorkflowDocumentationAgent(BaseAgent):
    """Specialized agent for generating comprehensive workflow documentation"""
    
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
        self.documentation_history: Dict[str, List[Dict[str, Any]]] = {}
        self.logger.info("Workflow Documentation agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and generate workflow documentation"""
        try:
            self.log_operation("Starting workflow documentation", {"input_type": type(input_data).__name__})
            
            # 1. Analyze workflow structure
            analysis_result = await self._analyze_workflow(input_data)
            if not analysis_result.success:
                return analysis_result
            
            # 2. Generate technical documentation
            technical_result = await self._generate_technical_docs(analysis_result.data)
            if not technical_result.success:
                return technical_result
            
            # 3. Generate user documentation
            user_result = await self._generate_user_docs(analysis_result.data)
            if not user_result.success:
                return user_result
            
            # 4. Generate API documentation
            api_result = await self._generate_api_docs(analysis_result.data)
            if not api_result.success:
                return api_result
            
            # 5. Return the final documentation
            final_docs = {
                "technical": technical_result.data,
                "user": user_result.data,
                "api": api_result.data
            }
            
            # Store documentation in history
            workflow_id = input_data.get("workflow_id", "default")
            if workflow_id not in self.documentation_history:
                self.documentation_history[workflow_id] = []
            self.documentation_history[workflow_id].append({
                "documentation": final_docs,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            return AgentResult(
                success=True,
                data=final_docs,
                metadata={
                    "analysis": analysis_result.metadata,
                    "technical": technical_result.metadata,
                    "user": user_result.metadata,
                    "api": api_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _analyze_workflow(self, workflow: Dict[str, Any]) -> AgentResult:
        """Analyze the workflow structure and components"""
        try:
            system_prompt = """You are an expert at analyzing n8n workflow structures. Your task is to:
1. Identify workflow components and their relationships
2. Analyze node configurations and parameters
3. Map data flow and dependencies
4. Return the workflow analysis

If analysis fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the workflow analysis
            try:
                workflow_analysis = json.loads(response)
                return AgentResult(
                    success=True,
                    data=workflow_analysis,
                    metadata={"analysis_method": "llm", "prompt_type": "workflow_analysis"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse workflow analysis: {str(e)}",
                    metadata={"analysis_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_technical_docs(self, analysis: Dict[str, Any]) -> AgentResult:
        """Generate technical documentation for the workflow"""
        try:
            system_prompt = """You are an expert at generating technical documentation for n8n workflows. Your task is to:
1. Document workflow architecture and design
2. Explain node configurations and parameters
3. Detail data flow and transformations
4. Return the technical documentation

If documentation generation fails, explain the issues in the error field."""
            
            # Convert analysis to string for LLM processing
            analysis_str = json.dumps(analysis, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis_str
            )
            
            # Parse the technical documentation
            try:
                technical_docs = json.loads(response)
                return AgentResult(
                    success=True,
                    data=technical_docs,
                    metadata={"doc_method": "llm", "prompt_type": "technical_documentation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse technical documentation: {str(e)}",
                    metadata={"doc_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_user_docs(self, analysis: Dict[str, Any]) -> AgentResult:
        """Generate user documentation for the workflow"""
        try:
            system_prompt = """You are an expert at generating user documentation for n8n workflows. Your task is to:
1. Create user-friendly workflow descriptions
2. Explain workflow purpose and functionality
3. Provide usage instructions and examples
4. Return the user documentation

If documentation generation fails, explain the issues in the error field."""
            
            # Convert analysis to string for LLM processing
            analysis_str = json.dumps(analysis, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis_str
            )
            
            # Parse the user documentation
            try:
                user_docs = json.loads(response)
                return AgentResult(
                    success=True,
                    data=user_docs,
                    metadata={"doc_method": "llm", "prompt_type": "user_documentation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse user documentation: {str(e)}",
                    metadata={"doc_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_api_docs(self, analysis: Dict[str, Any]) -> AgentResult:
        """Generate API documentation for the workflow"""
        try:
            system_prompt = """You are an expert at generating API documentation for n8n workflows. Your task is to:
1. Document workflow endpoints and methods
2. Explain input/output data structures
3. Detail authentication and security requirements
4. Return the API documentation

If documentation generation fails, explain the issues in the error field."""
            
            # Convert analysis to string for LLM processing
            analysis_str = json.dumps(analysis, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis_str
            )
            
            # Parse the API documentation
            try:
                api_docs = json.loads(response)
                return AgentResult(
                    success=True,
                    data=api_docs,
                    metadata={"doc_method": "llm", "prompt_type": "api_documentation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse API documentation: {str(e)}",
                    metadata={"doc_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def get_documentation_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get the documentation history for a workflow"""
        return self.documentation_history.get(workflow_id, [])
    
    async def clear_documentation_history(self, workflow_id: str) -> bool:
        """Clear the documentation history for a workflow"""
        if workflow_id in self.documentation_history:
            del self.documentation_history[workflow_id]
            return True
        return False
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 