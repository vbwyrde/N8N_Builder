from typing import Dict, Any, Optional
import os
import logging
from pathlib import Path
from pydantic import BaseModel

# Create logs directory if it doesn't exist
logs_dir = Path("logs")
logs_dir.mkdir(exist_ok=True)

# Configure enhanced logging with both console and file output
log_formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
)

# Create file handlers for different log types
main_file_handler = logging.FileHandler(logs_dir / "n8n_builder.log")
main_file_handler.setFormatter(log_formatter)
main_file_handler.setLevel(logging.INFO)

error_file_handler = logging.FileHandler(logs_dir / "errors.log")
error_file_handler.setFormatter(log_formatter)
error_file_handler.setLevel(logging.ERROR)

# Configure root logger with both console and file output
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Console output (existing)
        main_file_handler,        # Main log file
        error_file_handler        # Error log file
    ]
)

logger = logging.getLogger(__name__)

# Add file handlers to specialized loggers
specialized_loggers = [
    'n8n_builder.iteration',
    'n8n_builder.performance', 
    'n8n_builder.validation',
    'n8n_builder.llm',
    'n8n_builder.project',
    'n8n_builder.filesystem',
    'n8n_builder.diff',
    'n8n_builder.retry'
]

for logger_name in specialized_loggers:
    specialized_logger = logging.getLogger(logger_name)
    specialized_logger.addHandler(main_file_handler)
    specialized_logger.addHandler(error_file_handler)

logger.info(f"Enhanced logging configured - logs will be written to {logs_dir.absolute()}")

class LLMConfig(BaseModel):
    """Configuration for LLM endpoints and settings."""
    endpoint: str
    api_key: Optional[str] = None
    model: str
    temperature: float = 0.7
    max_tokens: int = 4000
    timeout: int = 360
    headers: Dict[str, str] = {}
    is_local: bool = False

class MCPResearchConfig(BaseModel):
    """Configuration for MCP Research Tool."""
    enabled: bool = True
    timeout: int = 30
    cache_ttl: int = 3600  # 1 hour
    max_content_length: int = 2000
    max_results_per_source: int = 5
    github_api_token: Optional[str] = None
    sources: Dict[str, str] = {
        'official_docs': 'https://docs.n8n.io/',
        'community_forum': 'https://community.n8n.io/',
        'github_main': 'https://github.com/n8n-io/n8n',
        'templates': 'https://n8n.io/workflows/'
    }

class MCPDatabaseConfig(BaseModel):
    """Configuration for MCP Database connections."""
    enabled: bool = True
    connections: Dict[str, Dict[str, str]] = {
        'Enterprise_Database': {
            'server': 'localhost',
            'database': 'Enterprise_Database',
            'driver': 'ODBC Driver 18 for SQL Server',
            'trusted_connection': 'yes',
            'connection_timeout': '30',
            'command_timeout': '30',
            'encrypt': 'no',
            'trust_server_certificate': 'yes'
        }
    }

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
            max_tokens=int(os.getenv("MIMO_MAX_TOKENS", "4000")),
            timeout=int(os.getenv("MIMO_TIMEOUT", "360")),
            is_local=is_local_mimo
        )

        # MCP Research configuration
        self.mcp_research = MCPResearchConfig(
            enabled=os.getenv("MCP_RESEARCH_ENABLED", "true").lower() == "true",
            timeout=int(os.getenv("MCP_RESEARCH_TIMEOUT", "30")),
            cache_ttl=int(os.getenv("MCP_RESEARCH_CACHE_TTL", "3600")),
            max_content_length=int(os.getenv("MCP_RESEARCH_MAX_CONTENT", "2000")),
            max_results_per_source=int(os.getenv("MCP_RESEARCH_MAX_RESULTS", "5")),
            github_api_token=os.getenv("GITHUB_API_TOKEN")
        )

        # MCP Database configuration
        self.mcp_database = MCPDatabaseConfig(
            enabled=os.getenv("MCP_DATABASE_ENABLED", "true").lower() == "true"
        )

        # Add MCP research attributes for backward compatibility
        self.enable_mcp_research = self.mcp_research.enabled
        self.research_timeout = self.mcp_research.timeout

        logger.debug(f"\nFinal LLM Configuration:")
        logger.debug(f"Mimo LLM Config: {self.mimo_llm}")
        logger.debug(f"MCP Research Config: {self.mcp_research}")

# Create a global config instance
config = Config() 