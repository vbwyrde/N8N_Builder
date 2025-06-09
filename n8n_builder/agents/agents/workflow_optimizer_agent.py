import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class WorkflowOptimizerAgent(BaseAgent):
    """Specialized agent for analyzing and optimizing n8n workflow performance"""
    
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
        self.optimization_history: Dict[str, List[Dict[str, Any]]] = {}
        self.logger.info("Workflow Optimizer agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and optimize the workflow"""
        try:
            self.log_operation("Starting workflow optimization", {"input_type": type(input_data).__name__})
            
            # 1. Analyze workflow performance
            analysis_result = await self._analyze_performance(input_data)
            if not analysis_result.success:
                return analysis_result
            
            # 2. Identify optimization opportunities
            opportunities_result = await self._identify_opportunities(analysis_result.data)
            if not opportunities_result.success:
                return opportunities_result
            
            # 3. Generate optimization strategies
            strategies_result = await self._generate_optimization_strategies(opportunities_result.data)
            if not strategies_result.success:
                return strategies_result
            
            # 4. Apply optimizations
            optimization_result = await self._apply_optimizations(strategies_result.data)
            if not optimization_result.success:
                return optimization_result
            
            # 5. Return the final optimization result
            return AgentResult(
                success=True,
                data=optimization_result.data,
                metadata={
                    "analysis": analysis_result.metadata,
                    "opportunities": opportunities_result.metadata,
                    "strategies": strategies_result.metadata,
                    "optimization": optimization_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _analyze_performance(self, workflow: Dict[str, Any]) -> AgentResult:
        """Analyze the workflow's current performance"""
        try:
            system_prompt = """You are an expert at analyzing n8n workflow performance. Your task is to:
1. Identify performance bottlenecks
2. Analyze node execution patterns
3. Evaluate resource utilization
4. Return the performance analysis

If analysis fails, explain the issues in the error field."""
            
            # Convert workflow to string for LLM processing
            workflow_str = json.dumps(workflow, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=workflow_str
            )
            
            # Parse the performance analysis
            try:
                performance_analysis = json.loads(response)
                return AgentResult(
                    success=True,
                    data=performance_analysis,
                    metadata={"analysis_method": "llm", "prompt_type": "performance_analysis"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse performance analysis: {str(e)}",
                    metadata={"analysis_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _identify_opportunities(self, analysis: Dict[str, Any]) -> AgentResult:
        """Identify optimization opportunities in the workflow"""
        try:
            system_prompt = """You are an expert at identifying n8n workflow optimization opportunities. Your task is to:
1. Identify potential performance improvements
2. Find redundant or inefficient operations
3. Suggest better node configurations
4. Return the optimization opportunities

If opportunity identification fails, explain the issues in the error field."""
            
            # Convert analysis to string for LLM processing
            analysis_str = json.dumps(analysis, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis_str
            )
            
            # Parse the optimization opportunities
            try:
                opportunities = json.loads(response)
                return AgentResult(
                    success=True,
                    data=opportunities,
                    metadata={"opportunity_method": "llm", "prompt_type": "optimization_opportunities"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse optimization opportunities: {str(e)}",
                    metadata={"opportunity_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_optimization_strategies(self, opportunities: Dict[str, Any]) -> AgentResult:
        """Generate optimization strategies for the identified opportunities"""
        try:
            system_prompt = """You are an expert at generating n8n workflow optimization strategies. Your task is to:
1. Generate specific optimization strategies
2. Evaluate potential performance gains
3. Consider implementation complexity
4. Return the optimization strategies

If strategy generation fails, explain the issues in the error field."""
            
            # Convert opportunities to string for LLM processing
            opportunities_str = json.dumps(opportunities, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=opportunities_str
            )
            
            # Parse the optimization strategies
            try:
                strategies = json.loads(response)
                return AgentResult(
                    success=True,
                    data=strategies,
                    metadata={"strategy_method": "llm", "prompt_type": "optimization_strategies"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse optimization strategies: {str(e)}",
                    metadata={"strategy_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _apply_optimizations(self, strategies: Dict[str, Any]) -> AgentResult:
        """Apply the optimization strategies to the workflow"""
        try:
            system_prompt = """You are an expert at applying n8n workflow optimizations. Your task is to:
1. Apply the optimization strategies
2. Verify the optimizations
3. Ensure workflow functionality
4. Return the optimized workflow

If optimization application fails, explain the issues in the error field."""
            
            # Convert strategies to string for LLM processing
            strategies_str = json.dumps(strategies, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=strategies_str
            )
            
            # Parse the optimized workflow
            try:
                optimized_workflow = json.loads(response)
                # Store optimization attempt in history
                workflow_id = strategies.get("workflow_id", "default")
                if workflow_id not in self.optimization_history:
                    self.optimization_history[workflow_id] = []
                self.optimization_history[workflow_id].append({
                    "strategies": strategies,
                    "optimized_workflow": optimized_workflow,
                    "timestamp": asyncio.get_event_loop().time()
                })
                return AgentResult(
                    success=True,
                    data=optimized_workflow,
                    metadata={"optimization_method": "llm", "prompt_type": "optimization_application"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse optimized workflow: {str(e)}",
                    metadata={"optimization_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def get_optimization_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get the optimization history for a workflow"""
        return self.optimization_history.get(workflow_id, [])
    
    async def clear_optimization_history(self, workflow_id: str) -> bool:
        """Clear the optimization history for a workflow"""
        if workflow_id in self.optimization_history:
            del self.optimization_history[workflow_id]
            return True
        return False
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 