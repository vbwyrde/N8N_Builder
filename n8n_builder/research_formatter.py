"""
Research Results Formatter for N8N Workflow Generation

This module formats research results from the MCP research tool into
structured prompts for the LLM to generate better workflows.
"""

import json
from typing import Dict, List, Any
from dataclasses import asdict

from .mcp_research_tool import ResearchResult, NodeDocumentation, WorkflowPattern

class ResearchFormatter:
    """
    Formats research results into structured prompts for LLM consumption.
    """
    
    def __init__(self, max_content_length: int = 2000):
        """
        Initialize the formatter.
        
        Args:
            max_content_length: Maximum length of formatted content
        """
        self.max_content_length = max_content_length
    
    def format_comprehensive_research(self, research_data: Dict[str, Any]) -> str:
        """
        Format comprehensive research results into a structured prompt section.
        
        Args:
            research_data: Research results from comprehensive_research()
            
        Returns:
            Formatted research content for prompt inclusion
        """
        sections = []
        
        # Format official documentation
        if research_data.get('official_docs'):
            docs_section = self._format_official_docs(research_data['official_docs'])
            if docs_section:
                sections.append(docs_section)
        
        # Format community examples
        if research_data.get('community_examples'):
            community_section = self._format_community_examples(research_data['community_examples'])
            if community_section:
                sections.append(community_section)
        
        # Format best practices
        if research_data.get('best_practices'):
            practices_section = self._format_best_practices(research_data['best_practices'])
            if practices_section:
                sections.append(practices_section)
        
        # Format integration patterns
        if research_data.get('integration_patterns'):
            patterns_section = self._format_integration_patterns(research_data['integration_patterns'])
            if patterns_section:
                sections.append(patterns_section)
        
        # Format detected concepts
        if research_data.get('concepts'):
            concepts_section = self._format_concepts(research_data['concepts'])
            if concepts_section:
                sections.append(concepts_section)
        
        # Combine all sections
        formatted_content = "\n\n".join(sections)
        
        # Truncate if too long
        if len(formatted_content) > self.max_content_length:
            formatted_content = formatted_content[:self.max_content_length] + "\n... [Content truncated for length]"
        
        return formatted_content
    
    def _format_official_docs(self, docs_results: List[ResearchResult]) -> str:
        """Format official documentation results."""
        if not docs_results:
            return ""
        
        content = ["=== OFFICIAL N8N DOCUMENTATION ==="]
        
        for result in docs_results[:3]:  # Top 3 results
            content.append(f"📖 {result.title}")
            content.append(f"   {result.content[:200]}...")
            if result.metadata and result.metadata.get('node_type'):
                content.append(f"   Node Type: {result.metadata['node_type']}")
            content.append("")
        
        return "\n".join(content)
    
    def _format_community_examples(self, community_results: List[ResearchResult]) -> str:
        """Format community examples."""
        if not community_results:
            return ""
        
        content = ["=== COMMUNITY EXAMPLES ==="]
        
        for result in community_results[:2]:  # Top 2 results
            content.append(f"💬 {result.title}")
            content.append(f"   {result.content[:150]}...")
            content.append(f"   Relevance: {result.relevance_score:.2f}")
            content.append("")
        
        return "\n".join(content)
    
    def _format_best_practices(self, best_practices: List[str]) -> str:
        """Format best practices."""
        if not best_practices:
            return ""
        
        content = ["=== BEST PRACTICES ==="]
        
        for practice in best_practices[:5]:  # Top 5 practices
            content.append(f"✅ {practice}")
        
        content.append("")
        return "\n".join(content)
    
    def _format_integration_patterns(self, patterns: Dict[str, List[WorkflowPattern]]) -> str:
        """Format integration patterns."""
        if not patterns:
            return ""
        
        content = ["=== INTEGRATION PATTERNS ==="]
        
        for service, service_patterns in patterns.items():
            if service_patterns:
                content.append(f"🔗 {service.upper()} INTEGRATION:")
                for pattern in service_patterns[:1]:  # One pattern per service
                    content.append(f"   Pattern: {pattern.pattern_name}")
                    content.append(f"   Use Cases: {', '.join(pattern.use_cases[:3])}")
                    content.append(f"   Required Nodes: {', '.join(pattern.required_nodes)}")
                content.append("")
        
        return "\n".join(content)
    
    def _format_concepts(self, concepts: Dict[str, List[str]]) -> str:
        """Format detected concepts."""
        if not concepts:
            return ""
        
        content = ["=== DETECTED CONCEPTS ==="]
        
        if concepts.get('services'):
            content.append(f"🔧 Services: {', '.join(concepts['services'])}")
        
        if concepts.get('actions'):
            content.append(f"⚡ Actions: {', '.join(concepts['actions'])}")
        
        if concepts.get('triggers'):
            content.append(f"🎯 Triggers: {', '.join(concepts['triggers'])}")
        
        content.append("")
        return "\n".join(content)
    
    def format_node_documentation(self, node_doc: NodeDocumentation) -> str:
        """
        Format node documentation for prompt inclusion.
        
        Args:
            node_doc: NodeDocumentation object
            
        Returns:
            Formatted node documentation
        """
        content = [f"=== {node_doc.node_name.upper()} NODE DOCUMENTATION ==="]
        content.append(f"Type: {node_doc.node_type}")
        content.append(f"Description: {node_doc.description}")
        
        if node_doc.parameters:
            content.append("Parameters:")
            for param, details in list(node_doc.parameters.items())[:5]:  # Top 5 parameters
                content.append(f"  - {param}: {details}")
        
        if node_doc.best_practices:
            content.append("Best Practices:")
            for practice in node_doc.best_practices[:3]:  # Top 3 practices
                content.append(f"  ✅ {practice}")
        
        if node_doc.common_issues:
            content.append("Common Issues:")
            for issue in node_doc.common_issues[:2]:  # Top 2 issues
                content.append(f"  ⚠️ {issue}")
        
        return "\n".join(content)
    
    def create_enhanced_prompt_context(self, description: str, research_data: Dict[str, Any]) -> str:
        """
        Create enhanced prompt context with research data.
        
        Args:
            description: Original workflow description
            research_data: Comprehensive research results
            
        Returns:
            Enhanced context for prompt building
        """
        context_parts = []
        
        # Add research summary
        research_summary = self.format_comprehensive_research(research_data)
        if research_summary:
            context_parts.append("=== RESEARCH-INFORMED CONTEXT ===")
            context_parts.append(research_summary)
        
        # Add specific recommendations based on research
        recommendations = self._generate_recommendations(description, research_data)
        if recommendations:
            context_parts.append("=== IMPLEMENTATION RECOMMENDATIONS ===")
            context_parts.extend(recommendations)
        
        return "\n\n".join(context_parts)
    
    def _generate_recommendations(self, description: str, research_data: Dict[str, Any]) -> List[str]:
        """Generate specific recommendations based on research."""
        recommendations = []
        
        concepts = research_data.get('concepts', {})
        
        # Service-specific recommendations
        if 'email' in concepts.get('services', []):
            recommendations.append("🔧 Use 'n8n-nodes-base.emailSend' for email functionality")
            recommendations.append("🔐 Configure SMTP credentials or use Gmail OAuth")
        
        if 'slack' in concepts.get('services', []):
            recommendations.append("🔧 Use 'n8n-nodes-base.slack' for Slack integration")
            recommendations.append("🔐 Set up Slack app with proper OAuth scopes")
        
        if 'webhook' in concepts.get('triggers', []):
            recommendations.append("🎯 Use 'n8n-nodes-base.webhook' as trigger node")
            recommendations.append("🔗 Configure webhook URL in external service")
        
        if 'schedule' in concepts.get('triggers', []):
            recommendations.append("🎯 Use 'n8n-nodes-base.cron' for scheduled execution")
            recommendations.append("⏰ Set appropriate cron expression for timing")
        
        # Add error handling recommendation
        recommendations.append("🛡️ Include error handling nodes for robust workflows")
        
        # Add testing recommendation
        recommendations.append("🧪 Test workflow with sample data before activation")
        
        return recommendations
    
    def format_for_llm_prompt(self, description: str, research_data: Dict[str, Any]) -> str:
        """
        Format research data specifically for LLM prompt inclusion.
        
        Args:
            description: Original workflow description
            research_data: Research results
            
        Returns:
            Formatted content ready for LLM prompt
        """
        enhanced_context = self.create_enhanced_prompt_context(description, research_data)
        
        # Create the final formatted section
        formatted_prompt = f"""
RESEARCH-ENHANCED WORKFLOW GENERATION

USER REQUEST: {description}

{enhanced_context}

INSTRUCTIONS:
- Use the research findings above to inform your workflow generation
- Follow the best practices and recommendations provided
- Use the specific node types and patterns identified in the research
- Implement proper error handling and security measures
- Generate a production-ready workflow that follows current n8n standards
"""
        
        return formatted_prompt.strip()
