import os
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass
from .base_agent import AgentConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentTypeConfig:
    """Configuration for a type of agent"""
    name: str
    description: str
    capabilities: list[str]
    llm_model: str
    llm_temperature: float
    llm_max_tokens: int
    llm_timeout: int

class ConfigManager:
    """Manages configuration for all agents"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ConfigManager")
        self.agent_configs: Dict[str, AgentTypeConfig] = {}
        self._load_environment()
        self._initialize_agent_configs()
    
    def _load_environment(self):
        """Load configuration from environment variables"""
        self.llm_endpoint = os.getenv("LLM_ENDPOINT", "http://localhost:1234/v1/chat/completions")
        self.is_local = os.getenv("LLM_IS_LOCAL", "true").lower() == "true"
        self.api_key = os.getenv("LLM_API_KEY")
        
        self.logger.info(f"Loaded environment: endpoint={self.llm_endpoint}, is_local={self.is_local}")
    
    def _initialize_agent_configs(self):
        """Initialize configurations for different agent types"""
        # Orchestrator Agent
        self.agent_configs["orchestrator"] = AgentTypeConfig(
            name="Orchestrator",
            description="Coordinates workflow generation process",
            capabilities=["coordination", "workflow_management"],
            llm_model="mimo-vl-7b",
            llm_temperature=0.7,
            llm_max_tokens=2000,
            llm_timeout=30
        )
        
        # Workflow Generator Agent
        self.agent_configs["workflow_generator"] = AgentTypeConfig(
            name="WorkflowGenerator",
            description="Generates workflow descriptions",
            capabilities=["workflow_generation", "pattern_recognition"],
            llm_model="mimo-vl-7b",
            llm_temperature=0.7,
            llm_max_tokens=2000,
            llm_timeout=30
        )
        
        # JSON Extractor Agent
        self.agent_configs["json_extractor"] = AgentTypeConfig(
            name="JSONExtractor",
            description="Extracts and validates JSON from responses",
            capabilities=["json_extraction", "pattern_matching"],
            llm_model="mimo-vl-7b",
            llm_temperature=0.3,  # Lower temperature for more precise extraction
            llm_max_tokens=2000,
            llm_timeout=30
        )
        
        # Validation Agent
        self.agent_configs["validator"] = AgentTypeConfig(
            name="Validator",
            description="Validates n8n workflow structure",
            capabilities=["validation", "structure_verification"],
            llm_model="mimo-vl-7b",
            llm_temperature=0.3,  # Lower temperature for more precise validation
            llm_max_tokens=2000,
            llm_timeout=30
        )
    
    def get_agent_config(self, agent_type: str) -> AgentConfig:
        """Get configuration for a specific agent type"""
        if agent_type not in self.agent_configs:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        base_config = self.agent_configs[agent_type]
        return AgentConfig(
            name=base_config.name,
            description=base_config.description,
            capabilities=base_config.capabilities,
            llm_endpoint=self.llm_endpoint,
            llm_model=base_config.llm_model,
            llm_temperature=base_config.llm_temperature,
            llm_max_tokens=base_config.llm_max_tokens,
            llm_timeout=base_config.llm_timeout,
            is_local=self.is_local,
            api_key=self.api_key
        )
    
    def validate_config(self, config: AgentConfig) -> bool:
        """Validate an agent configuration"""
        try:
            # Check required fields
            assert config.name, "Agent name is required"
            assert config.description, "Agent description is required"
            assert config.capabilities, "Agent capabilities are required"
            assert config.llm_endpoint, "LLM endpoint is required"
            assert config.llm_model, "LLM model is required"
            
            # Validate numeric fields
            assert 0 <= config.llm_temperature <= 1, "Temperature must be between 0 and 1"
            assert config.llm_max_tokens > 0, "Max tokens must be positive"
            assert config.llm_timeout > 0, "Timeout must be positive"
            
            return True
        except AssertionError as e:
            self.logger.error(f"Configuration validation failed: {str(e)}")
            return False 