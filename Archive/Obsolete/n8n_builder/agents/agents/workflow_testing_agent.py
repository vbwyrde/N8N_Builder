import logging
import json
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class WorkflowTestingAgent(BaseAgent):
    """Specialized agent for testing and validating n8n workflows"""
    
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
        self.test_history: Dict[str, List[Dict[str, Any]]] = {}
        self.logger.info("Workflow Testing agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and test the workflow"""
        try:
            self.log_operation("Starting workflow testing", {"input_type": type(input_data).__name__})
            
            # 1. Generate test cases
            test_cases_result = await self._generate_test_cases(input_data)
            if not test_cases_result.success:
                return test_cases_result
            
            # 2. Execute functional tests
            functional_result = await self._execute_functional_tests(test_cases_result.data)
            if not functional_result.success:
                return functional_result
            
            # 3. Execute performance tests
            performance_result = await self._execute_performance_tests(test_cases_result.data)
            if not performance_result.success:
                return performance_result
            
            # 4. Execute integration tests
            integration_result = await self._execute_integration_tests(test_cases_result.data)
            if not integration_result.success:
                return integration_result
            
            # 5. Return the final test results
            final_results = {
                "functional": functional_result.data,
                "performance": performance_result.data,
                "integration": integration_result.data
            }
            
            # Store test results in history
            workflow_id = input_data.get("workflow_id", "default")
            if workflow_id not in self.test_history:
                self.test_history[workflow_id] = []
            self.test_history[workflow_id].append({
                "test_cases": test_cases_result.data,
                "results": final_results,
                "timestamp": asyncio.get_event_loop().time()
            })
            
            return AgentResult(
                success=True,
                data=final_results,
                metadata={
                    "test_cases": test_cases_result.metadata,
                    "functional": functional_result.metadata,
                    "performance": performance_result.metadata,
                    "integration": integration_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_test_cases(self, workflow: Dict[str, Any]) -> AgentResult:
        """Generate test cases for the workflow"""
        try:
            system_prompt = """You are an expert at generating test cases for n8n workflows. Your task is to:
1. Generate functional test cases
2. Create performance test scenarios
3. Design integration test cases
4. Return the test cases

If test case generation fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the test cases
            try:
                test_cases = json.loads(response)
                return AgentResult(
                    success=True,
                    data=test_cases,
                    metadata={"test_method": "llm", "prompt_type": "test_case_generation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse test cases: {str(e)}",
                    metadata={"test_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _execute_functional_tests(self, test_cases: Dict[str, Any]) -> AgentResult:
        """Execute functional tests for the workflow"""
        try:
            system_prompt = """You are an expert at executing functional tests for n8n workflows. Your task is to:
1. Execute each functional test case
2. Verify expected outputs
3. Check error handling
4. Return the test results

If test execution fails, explain the issues in the error field."""
            
            # Convert test cases to string for LLM processing
            test_cases_str = json.dumps(test_cases, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=test_cases_str
            )
            
            # Parse the functional test results
            try:
                functional_results = json.loads(response)
                return AgentResult(
                    success=True,
                    data=functional_results,
                    metadata={"test_method": "llm", "prompt_type": "functional_testing"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse functional test results: {str(e)}",
                    metadata={"test_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _execute_performance_tests(self, test_cases: Dict[str, Any]) -> AgentResult:
        """Execute performance tests for the workflow"""
        try:
            system_prompt = """You are an expert at executing performance tests for n8n workflows. Your task is to:
1. Execute performance test scenarios
2. Measure response times
3. Monitor resource usage
4. Return the test results

If test execution fails, explain the issues in the error field."""
            
            # Convert test cases to string for LLM processing
            test_cases_str = json.dumps(test_cases, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=test_cases_str
            )
            
            # Parse the performance test results
            try:
                performance_results = json.loads(response)
                return AgentResult(
                    success=True,
                    data=performance_results,
                    metadata={"test_method": "llm", "prompt_type": "performance_testing"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse performance test results: {str(e)}",
                    metadata={"test_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _execute_integration_tests(self, test_cases: Dict[str, Any]) -> AgentResult:
        """Execute integration tests for the workflow"""
        try:
            system_prompt = """You are an expert at executing integration tests for n8n workflows. Your task is to:
1. Execute integration test cases
2. Verify system interactions
3. Check data flow between components
4. Return the test results

If test execution fails, explain the issues in the error field."""
            
            # Convert test cases to string for LLM processing
            test_cases_str = json.dumps(test_cases, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=test_cases_str
            )
            
            # Parse the integration test results
            try:
                integration_results = json.loads(response)
                return AgentResult(
                    success=True,
                    data=integration_results,
                    metadata={"test_method": "llm", "prompt_type": "integration_testing"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse integration test results: {str(e)}",
                    metadata={"test_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def get_test_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get the test history for a workflow"""
        return self.test_history.get(workflow_id, [])
    
    async def clear_test_history(self, workflow_id: str) -> bool:
        """Clear the test history for a workflow"""
        if workflow_id in self.test_history:
            del self.test_history[workflow_id]
            return True
        return False
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 