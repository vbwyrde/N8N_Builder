import aiohttp
import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LLMMessage:
    """A message in the LLM conversation"""
    role: str
    content: str

class LLMClient:
    """Shared LLM client for making API calls"""
    
    def __init__(self, endpoint: str, model: str, temperature: float = 0.7,
                 max_tokens: int = 2000, timeout: int = 30, api_key: Optional[str] = None,
                 is_local: bool = True):
        self.endpoint = endpoint
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.api_key = api_key
        self.is_local = is_local
        self.session = None
        self.logger = logging.getLogger(f"{__name__}.LLMClient")
        self.logger.info(f"Initializing LLM client: endpoint={endpoint}, model={model}, is_local={is_local}")

    async def _ensure_session(self):
        """Ensure we have an active aiohttp session"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """Close the aiohttp session"""
        if self.session:
            await self.session.close()
            self.session = None

    async def call_llm(self, messages: List[LLMMessage], max_retries: int = 3) -> str:
        """Call the LLM API with retries and proper error handling"""
        await self._ensure_session()
        
        payload = {
            "model": self.model,
            "messages": [{"role": msg.role, "content": msg.content} for msg in messages],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        for attempt in range(max_retries):
            try:
                async with self.session.post(
                    self.endpoint,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"LLM API error: {response.status} - {error_text}")
                    
                    result = await response.json()
                    return result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
            except Exception as e:
                if attempt == max_retries - 1:
                    self.logger.error(f"LLM API call failed after {max_retries} attempts: {str(e)}")
                    raise
                wait_time = 1.0 * (2 ** attempt)
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)

    async def call_llm_with_system_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Helper method to call LLM with a system prompt and user prompt"""
        messages = [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_prompt)
        ]
        return await self.call_llm(messages) 