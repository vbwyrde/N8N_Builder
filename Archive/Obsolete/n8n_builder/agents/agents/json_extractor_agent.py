import logging
import json
import re
from typing import Dict, Any, Optional, List, Tuple
from .base_agent import BaseAgent, AgentConfig, AgentResult
from .llm_client import LLMClient, LLMMessage

class JSONExtractorAgent(BaseAgent):
    """Specialized agent for extracting and cleaning JSON from workflow descriptions"""
    
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
        self.logger.info("JSON Extractor agent initialized")
    
    async def process(self, input_data: str) -> AgentResult:
        """Process the input description and extract JSON"""
        try:
            self.log_operation("Starting JSON extraction", {"input_length": len(input_data)})
            
            # 1. Pre-process the input
            preprocessed_result = await self._preprocess_input(input_data)
            if not preprocessed_result.success:
                return preprocessed_result
            
            # 2. Extract potential JSON blocks
            extraction_result = await self._extract_json_blocks(preprocessed_result.data)
            if not extraction_result.success:
                return extraction_result
            
            # 3. Clean and normalize the JSON
            cleaning_result = await self._clean_json(extraction_result.data)
            if not cleaning_result.success:
                return cleaning_result
            
            # 4. Validate the JSON structure
            validation_result = await self._validate_json_structure(cleaning_result.data)
            if not validation_result.success:
                return validation_result
            
            # 5. Return the final result
            return AgentResult(
                success=True,
                data=validation_result.data,
                metadata={
                    "preprocessing": preprocessed_result.metadata,
                    "extraction": extraction_result.metadata,
                    "cleaning": cleaning_result.metadata,
                    "validation": validation_result.metadata
                }
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _preprocess_input(self, input_data: str) -> AgentResult:
        """Pre-process the input to prepare for JSON extraction"""
        try:
            system_prompt = """You are an expert at preparing text for JSON extraction. Your task is to:
1. Remove any non-JSON text
2. Preserve any JSON-like structures
3. Format the text for easier JSON extraction
4. Return the cleaned text

Focus on preserving any JSON-like structures while removing irrelevant text."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=input_data
            )
            
            return AgentResult(
                success=True,
                data=response,
                metadata={"preprocessing_method": "llm", "prompt_type": "json_preprocessing"}
            )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _extract_json_blocks(self, preprocessed_text: str) -> AgentResult:
        """Extract potential JSON blocks from the preprocessed text"""
        try:
            # First try direct JSON parsing
            try:
                json_data = json.loads(preprocessed_text)
                return AgentResult(
                    success=True,
                    data=json_data,
                    metadata={"extraction_method": "direct_parse"}
                )
            except json.JSONDecodeError:
                pass
            
            # If direct parsing fails, use LLM to extract JSON
            system_prompt = """You are an expert at extracting JSON from text. Your task is to:
1. Find any JSON-like structures
2. Extract them as valid JSON
3. Return ONLY the JSON, no other text
4. If multiple JSON blocks exist, return the most complete one

If no valid JSON is found, return an empty object {}."""
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=preprocessed_text
            )
            
            # Try to parse the extracted JSON
            try:
                json_data = json.loads(response)
                return AgentResult(
                    success=True,
                    data=json_data,
                    metadata={"extraction_method": "llm", "prompt_type": "json_extraction"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse extracted JSON: {str(e)}",
                    metadata={"extraction_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _clean_json(self, json_data: Dict[str, Any]) -> AgentResult:
        """Clean and normalize the extracted JSON"""
        try:
            system_prompt = """You are an expert at cleaning and normalizing JSON. Your task is to:
1. Fix any formatting issues
2. Normalize field names
3. Ensure consistent data types
4. Remove any invalid or redundant fields
5. Return the cleaned JSON

Focus on making the JSON valid and consistent."""
            
            # Convert JSON to string for LLM processing
            json_str = json.dumps(json_data, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=json_str
            )
            
            # Parse the cleaned JSON
            try:
                cleaned_json = json.loads(response)
                return AgentResult(
                    success=True,
                    data=cleaned_json,
                    metadata={"cleaning_method": "llm", "prompt_type": "json_cleaning"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse cleaned JSON: {str(e)}",
                    metadata={"cleaning_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def _validate_json_structure(self, json_data: Dict[str, Any]) -> AgentResult:
        """Validate the JSON structure for n8n workflow format"""
        try:
            system_prompt = """You are an expert at validating n8n workflow JSON. Your task is to:
1. Verify the JSON has the correct structure
2. Check for required fields (nodes, connections)
3. Validate node types and parameters
4. Ensure proper connections
5. Return the validated JSON

If validation fails, explain the issues in the error field."""
            
            # Convert JSON to string for LLM processing
            json_str = json.dumps(json_data, indent=2)
            
            response = await self.llm_client.call_llm_with_system_prompt(
                system_prompt=system_prompt,
                user_prompt=json_str
            )
            
            # Parse the validated JSON
            try:
                validated_json = json.loads(response)
                return AgentResult(
                    success=True,
                    data=validated_json,
                    metadata={"validation_method": "llm", "prompt_type": "json_validation"}
                )
            except json.JSONDecodeError as e:
                return AgentResult(
                    success=False,
                    data=None,
                    error=f"Failed to parse validated JSON: {str(e)}",
                    metadata={"validation_method": "llm", "error": str(e)}
                )
            
        except Exception as e:
            return await self.handle_error(e)
    
    async def close(self):
        """Clean up resources"""
        await self.llm_client.close() 