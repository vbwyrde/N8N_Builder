from typing import Dict, Any, Optional
import os
import logging
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class LLMConfig(BaseModel):
    """Configuration for LLM endpoints and settings."""
    endpoint: str
    api_key: Optional[str] = None
    model: str
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30
    headers: Dict[str, str] = {}
    is_local: bool = False

class Config:
    """Main configuration class."""
    def __init__(self):
        # Log all environment variables for debugging
        logger.debug("All environment variables:")
        for key, value in os.environ.items():
            logger.debug(f"{key}={value}")

        # Get and log the is_local value
        is_local = os.getenv("MIMO_IS_LOCAL", "true")
        logger.debug(f"\nRaw is_local value: MIMO_IS_LOCAL={is_local}")
        
        # Convert to boolean, ensuring case-insensitive comparison
        is_local_mimo = str(is_local).lower() == "true"
        logger.debug(f"\nParsed is_local value: is_local_mimo={is_local_mimo}")
        
        # Set default endpoint based on is_local flag
        endpoint = os.getenv("MIMO_ENDPOINT")
        logger.debug(f"\nEndpoint value: MIMO_ENDPOINT={endpoint}")
        
        if not endpoint:
            endpoint = "http://localhost:1234/v1/chat/completions" if is_local_mimo else "https://api.openai.com/v1/chat/completions"
        
        logger.debug(f"\nFinal endpoint value: endpoint={endpoint}")
        
        # Get model name
        model = os.getenv("MIMO_MODEL", "mimo-vl-7b" if is_local_mimo else "gpt-4")
        logger.debug(f"\nModel value: model={model}")
        
        self.mimo_llm = LLMConfig(
            endpoint=endpoint,
            api_key=None if is_local_mimo else os.getenv("MIMO_API_KEY"),
            model=model,
            temperature=float(os.getenv("MIMO_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("MIMO_MAX_TOKENS", "2000")),
            timeout=int(os.getenv("MIMO_TIMEOUT", "30")),
            is_local=is_local_mimo
        )
        
        logger.debug(f"\nFinal LLM Configuration:")
        logger.debug(f"Mimo LLM Config: {self.mimo_llm}")

# Create a global config instance
config = Config() 