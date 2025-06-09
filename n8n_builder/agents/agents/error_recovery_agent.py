import logging
import json
from typing import Dict, Any, List, Optional, Tuple
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class ErrorRecoveryAgent(BaseAgent):
    """Specialized agent for handling workflow failures and providing recovery strategies"""
    
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
        self.recovery_history: Dict[str, List[Dict[str, Any]]] = {}
        self.logger.info("Error Recovery agent initialized")
    
    async def process(self, input_data: Dict[str, Any]) -> AgentResult:
        """Process and handle workflow errors"""
        try:
            self.log_operation("Starting error recovery", {"input_type": type(input_data).__name__})
            
            # 1. Analyze the error
            analysis_result = await self._analyze_error(input_data)
            if not analysis_result.success:
                return analysis_result
            
            # 2. Generate recovery strategies
            strategies_result = await self._generate_recovery_strategies(analysis_result.data)
            if not strategies_result.success:
                return strategies_result
            
            # 3. Select best strategy
            selection_result = await self._select_best_strategy(strategies_result.data)
            if not selection_result.success:
                return selection_result
            
            # 4. Apply recovery strategy
            recovery_result = await self._apply_recovery_strategy(selection_result.data)
            if not recovery_result.success:
                return recovery_result
            
            # 5. Return the final recovery result
            return AgentResult(
                success=True,
                data=recovery_result.data,
                metadata={
                    "analysis": analysis_result.metadata,
                    "strategies": strategies_result.metadata,
                    "selection": selection_result.metadata,
                    "recovery": recovery_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _analyze_error(self, error_data: Dict[str, Any]) -> AgentResult:
        """Analyze the error and determine its type and impact"""
        try:
            system_prompt = """You are an expert at analyzing n8n workflow errors. Your task is to:
1. Identify the error type and cause
2. Determine the impact on the workflow
3. Identify affected nodes and connections
4. Return the error analysis

If analysis fails, explain the issues in the error field."""
            
            # Convert error data to string for LLM processing
            error_str = json.dumps(error_data, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=error_str
            )
            
            # Parse the error analysis
            try:
                error_analysis = json.loads(response)
                return AgentResult(
                    success=True,
                    data=error_analysis,
                    metadata={"analysis_method": "llm", "prompt_type": "error_analysis"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse error analysis: {str(e)}",
                    metadata={"analysis_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _generate_recovery_strategies(self, error_analysis: Dict[str, Any]) -> AgentResult:
        """Generate possible recovery strategies for the error"""
        try:
            system_prompt = """You are an expert at generating n8n workflow recovery strategies. Your task is to:
1. Generate multiple recovery strategies
2. Evaluate each strategy's effectiveness
3. Consider potential side effects
4. Return the strategies with their evaluations

If strategy generation fails, explain the issues in the error field."""
            
            # Convert error analysis to string for LLM processing
            analysis_str = json.dumps(error_analysis, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=analysis_str
            )
            
            # Parse the recovery strategies
            try:
                recovery_strategies = json.loads(response)
                return AgentResult(
                    success=True,
                    data=recovery_strategies,
                    metadata={"strategy_method": "llm", "prompt_type": "recovery_strategies"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse recovery strategies: {str(e)}",
                    metadata={"strategy_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _select_best_strategy(self, strategies: Dict[str, Any]) -> AgentResult:
        """Select the best recovery strategy based on the error context"""
        try:
            system_prompt = """You are an expert at selecting n8n workflow recovery strategies. Your task is to:
1. Evaluate each strategy's suitability
2. Consider workflow context and requirements
3. Assess potential risks and benefits
4. Return the selected strategy with justification

If strategy selection fails, explain the issues in the error field."""
            
            # Convert strategies to string for LLM processing
            strategies_str = json.dumps(strategies, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=strategies_str
            )
            
            # Parse the selected strategy
            try:
                selected_strategy = json.loads(response)
                return AgentResult(
                    success=True,
                    data=selected_strategy,
                    metadata={"selection_method": "llm", "prompt_type": "strategy_selection"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse selected strategy: {str(e)}",
                    metadata={"selection_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _apply_recovery_strategy(self, strategy: Dict[str, Any]) -> AgentResult:
        """Apply the selected recovery strategy"""
        try:
            system_prompt = """You are an expert at applying n8n workflow recovery strategies. Your task is to:
1. Apply the selected recovery strategy
2. Monitor the recovery process
3. Verify the recovery success
4. Return the recovery results

If recovery application fails, explain the issues in the error field."""
            
            # Convert strategy to string for LLM processing
            strategy_str = json.dumps(strategy, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=strategy_str
            )
            
            # Parse the recovery results
            try:
                recovery_results = json.loads(response)
                # Store recovery attempt in history
                workflow_id = strategy.get("workflow_id", "default")
                if workflow_id not in self.recovery_history:
                    self.recovery_history[workflow_id] = []
                self.recovery_history[workflow_id].append({
                    "strategy": strategy,
                    "results": recovery_results,
                    "timestamp": asyncio.get_event_loop().time()
                })
                return AgentResult(
                    success=True,
                    data=recovery_results,
                    metadata={"recovery_method": "llm", "prompt_type": "strategy_application"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse recovery results: {str(e)}",
                    metadata={"recovery_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def get_recovery_history(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Get the recovery history for a workflow"""
        return self.recovery_history.get(workflow_id, [])
    
    async def clear_recovery_history(self, workflow_id: str) -> bool:
        """Clear the recovery history for a workflow"""
        if workflow_id in self.recovery_history:
            del self.recovery_history[workflow_id]
            return True
        return False
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 