"""
Enhanced Prompt Builder with MCP Research Integration

This module enhances the existing prompt building process by integrating
real-time research from the MCP research tool to create more accurate
and sophisticated n8n workflows.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
import time

from .mcp_research_tool import N8NResearchTool
from .research_formatter import ResearchFormatter
from .research_validator import ResearchValidator

# Configure logging
logger = logging.getLogger(__name__)

class EnhancedPromptBuilder:
    """
    Enhanced prompt builder that integrates MCP research for better workflow generation.
    """
    
    def __init__(self, enable_research: bool = True, research_timeout: int = 30, github_api_token: Optional[str] = None):
        """
        Initialize the enhanced prompt builder.

        Args:
            enable_research: Whether to enable research functionality
            research_timeout: Timeout for research operations in seconds
            github_api_token: GitHub API token for authenticated requests
        """
        self.enable_research = enable_research
        self.research_timeout = research_timeout
        self.github_api_token = github_api_token
        self.research_tool = None
        self.formatter = ResearchFormatter()
        self.validator = ResearchValidator()
        
        # Performance tracking
        self.research_stats = {
            'total_requests': 0,
            'successful_research': 0,
            'cache_hits': 0,
            'research_time_total': 0.0
        }
    
    async def build_enhanced_prompt(self, description: str, use_research: Optional[bool] = None) -> str:
        """
        Build an enhanced prompt with research integration.
        
        Args:
            description: Plain English workflow description
            use_research: Override research setting for this request
            
        Returns:
            Enhanced prompt with research context
        """
        start_time = time.time()
        self.research_stats['total_requests'] += 1
        
        # Determine if research should be used
        should_research = use_research if use_research is not None else self.enable_research
        
        if not should_research:
            logger.info("Research disabled, using basic prompt")
            return self._build_basic_prompt(description)
        
        try:
            # Perform research with timeout
            research_data = await asyncio.wait_for(
                self._perform_research(description),
                timeout=self.research_timeout
            )
            
            if research_data:
                self.research_stats['successful_research'] += 1
                enhanced_prompt = self._build_research_enhanced_prompt(description, research_data)
                
                research_time = time.time() - start_time
                self.research_stats['research_time_total'] += research_time
                
                logger.info(f"Enhanced prompt built with research in {research_time:.2f}s")
                return enhanced_prompt
            else:
                logger.warning("Research returned no data, falling back to basic prompt")
                return self._build_basic_prompt(description)
        
        except asyncio.TimeoutError:
            logger.warning(f"Research timeout after {self.research_timeout}s, using basic prompt")
            return self._build_basic_prompt(description)
        
        except Exception as e:
            logger.error(f"Research failed: {str(e)}, using basic prompt")
            return self._build_basic_prompt(description)
    
    async def _perform_research(self, description: str) -> Optional[Dict[str, Any]]:
        """
        Perform comprehensive research for the workflow description.
        
        Args:
            description: Workflow description
            
        Returns:
            Research results or None if failed
        """
        try:
            # Initialize research tool if needed
            if not self.research_tool:
                self.research_tool = N8NResearchTool(github_api_token=self.github_api_token)
            
            # Use async context manager for proper session management
            async with self.research_tool as research:
                logger.info(f"Starting research for: {description[:50]}...")
                research_data = await research.comprehensive_research(description)
                
                # Validate research data
                validation_result = self.validator.validate_comprehensive_research(research_data)

                if validation_result.is_valid:
                    logger.info(f"Research completed successfully (quality: {validation_result.quality_score:.2f})")
                    return research_data
                else:
                    logger.warning(f"Research data validation failed (quality: {validation_result.quality_score:.2f})")
                    logger.warning(f"Issues: {', '.join(validation_result.issues[:3])}")

                    # Return data anyway if we have some useful information
                    if validation_result.quality_score > 0.3:
                        logger.info("Using research data despite validation issues")
                        return research_data
                    else:
                        return None
        
        except Exception as e:
            logger.error(f"Research operation failed: {str(e)}")
            return None
    

    
    def _build_research_enhanced_prompt(self, description: str, research_data: Dict[str, Any]) -> str:
        """
        Build a prompt enhanced with research findings.
        
        Args:
            description: Original description
            research_data: Research results
            
        Returns:
            Enhanced prompt
        """
        # Format research data for LLM consumption
        research_context = self.formatter.format_for_llm_prompt(description, research_data)
        
        # Build the enhanced prompt
        enhanced_prompt = f"""{research_context}

WORKFLOW GENERATION REQUIREMENTS:

You are an expert n8n workflow generation assistant with access to current documentation and best practices. Generate a valid n8n workflow JSON that follows this EXACT structure:

{{
  "name": "Descriptive Workflow Name",
  "nodes": [
    {{
      "id": "unique-node-id",
      "name": "Human Readable Node Name",
      "type": "n8n-nodes-base.nodetype",
      "parameters": {{
        "param1": "value1",
        "param2": "value2"
      }},
      "position": [x, y]
    }}
  ],
  "connections": {{
    "Node Name": {{
      "main": [
        [
          {{
            "node": "Target Node Name",
            "type": "main",
            "index": 0
          }}
        ]
      ]
    }}
  }},
  "settings": {{}},
  "active": true,
  "version": 1
}}

CRITICAL REQUIREMENTS:
1. Return ONLY valid JSON - no explanations, no code blocks, no extra text
2. Use the specific node types and patterns identified in the research above
3. Implement the best practices and recommendations provided
4. Include proper error handling where appropriate
5. Use realistic parameter values based on the research findings
6. Ensure all node connections are properly defined
7. Position nodes logically (start at [250, 300], space by 250px horizontally)

Generate the workflow now:"""

        return enhanced_prompt
    
    def _build_basic_prompt(self, description: str) -> str:
        """
        Build a basic prompt without research enhancement.
        
        Args:
            description: Workflow description
            
        Returns:
            Basic prompt
        """
        return f"""You are an n8n workflow generation assistant. Generate a valid n8n workflow JSON for the following description:

{description}

IMPORTANT: You must return a valid n8n workflow JSON with this EXACT structure:

{{
  "name": "Workflow Name Here",
  "nodes": [
    {{
      "id": "unique-node-id",
      "name": "Human Readable Node Name",
      "type": "n8n-nodes-base.nodetype",
      "parameters": {{
        "param1": "value1",
        "param2": "value2"
      }},
      "position": [x, y]
    }}
  ],
  "connections": {{
    "Node Name": {{
      "main": [
        [
          {{
            "node": "Target Node Name",
            "type": "main",
            "index": 0
          }}
        ]
      ]
    }}
  }},
  "settings": {{}},
  "active": true,
  "version": 1
}}

CRITICAL: Return ONLY the JSON workflow. No explanations, no code blocks, no extra text."""
    
    async def research_specific_node(self, node_name: str) -> Optional[str]:
        """
        Research a specific node and return formatted documentation.
        
        Args:
            node_name: Name of the n8n node to research
            
        Returns:
            Formatted node documentation or None
        """
        try:
            if not self.research_tool:
                self.research_tool = N8NResearchTool(github_api_token=self.github_api_token)
            
            async with self.research_tool as research:
                node_doc = await research.get_node_documentation(node_name)
                
                if node_doc:
                    return self.formatter.format_node_documentation(node_doc)
                else:
                    return None
        
        except Exception as e:
            logger.error(f"Node research failed for {node_name}: {str(e)}")
            return None
    
    def get_research_stats(self) -> Dict[str, Any]:
        """
        Get research performance statistics.
        
        Returns:
            Dictionary of research statistics
        """
        stats = self.research_stats.copy()
        
        if stats['total_requests'] > 0:
            stats['success_rate'] = stats['successful_research'] / stats['total_requests']
            stats['average_research_time'] = stats['research_time_total'] / stats['successful_research'] if stats['successful_research'] > 0 else 0
        else:
            stats['success_rate'] = 0
            stats['average_research_time'] = 0
        
        return stats
    
    def reset_stats(self):
        """Reset research statistics."""
        self.research_stats = {
            'total_requests': 0,
            'successful_research': 0,
            'cache_hits': 0,
            'research_time_total': 0.0
        }
    
    async def close(self):
        """Clean up resources."""
        if self.research_tool:
            # The research tool uses async context manager, so it cleans up automatically
            pass
