import logging
import asyncio
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentConfig:
    """Configuration for an agent"""
    name: str
    description: str
    capabilities: list[str]
    llm_endpoint: str
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int
    llm_timeout: int
    is_local: bool = True
    api_key: Optional[str] = None

@dataclass
class AgentResult:
    """Result from an agent's operation"""
    success: bool
    data: Any
    error: Optional[str] = None
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = None

class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{config.name}")
        self.logger.info(f"Initializing {config.name} agent with capabilities: {config.capabilities}")
        
    @abstractmethod
    async def process(self, input_data: Any) -> AgentResult:
        """Process the input data and return a result"""
        pass
    
    async def validate_input(self, input_data: Any) -> bool:
        """Validate the input data before processing"""
        return True
    
    async def handle_error(self, error: Exception) -> AgentResult:
        """Handle errors during processing"""
        self.logger.error(f"Error in {self.config.name}: {str(error)}", exc_info=True)
        return AgentResult(
            success=False,
            data=None,
            error=str(error),
            metadata={"error_type": type(error).__name__}
        )
    
    async def retry_operation(self, operation, max_retries: int = 3, delay: float = 1.0) -> Any:
        """Retry an operation with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return await operation()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = delay * (2 ** attempt)
                self.logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
    
    def log_operation(self, operation: str, details: Dict[str, Any] = None):
        """Log an operation with details"""
        self.logger.info(f"{operation} - {details or ''}")
    
    def log_result(self, result: AgentResult):
        """Log the result of an operation"""
        if result.success:
            self.logger.info(f"Operation successful: {result.metadata or ''}")
        else:
            self.logger.error(f"Operation failed: {result.error}") 