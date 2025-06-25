"""
Context Analyzer - Gathers comprehensive context for detected errors.

This module analyzes detected errors and gathers relevant documentation,
code context, and system state information to provide comprehensive
context for solution generation.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, field
import json
import re

# Import existing N8N Builder components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.error_handler import ErrorDetail
from n8n_builder.logging_config import get_logger
from n8n_builder.project_manager import project_manager, filesystem_utils


@dataclass
class ContextInfo:
    """Comprehensive context information for an error."""
    error_id: str
    timestamp: datetime
    
    # Error context
    error_detail: ErrorDetail
    error_category: str
    error_severity: str
    
    # Code context
    related_files: List[Dict[str, Any]] = field(default_factory=list)
    code_snippets: List[Dict[str, Any]] = field(default_factory=list)
    function_calls: List[str] = field(default_factory=list)
    
    # Documentation context
    relevant_docs: List[Dict[str, Any]] = field(default_factory=list)
    api_references: List[str] = field(default_factory=list)
    
    # System context
    system_state: Dict[str, Any] = field(default_factory=dict)
    recent_changes: List[Dict[str, Any]] = field(default_factory=list)
    
    # Historical context
    similar_errors: List[Dict[str, Any]] = field(default_factory=list)
    previous_solutions: List[Dict[str, Any]] = field(default_factory=list)
    
    # Dependencies and relationships
    affected_components: List[str] = field(default_factory=list)
    dependency_chain: List[str] = field(default_factory=list)


class ContextAnalyzer:
    """
    Analyzes detected errors and gathers comprehensive context.
    
    Features:
    - Documentation retrieval from structured docs
    - Code context gathering using existing tools
    - System state analysis
    - Historical pattern analysis
    - Dependency mapping
    """
    
    def __init__(self):
        """Initialize the Context Analyzer."""
        self.logger = get_logger('self_healer.context_analyzer')
        
        # Paths
        self.project_root = Path(__file__).parent.parent.parent
        self.docs_path = self.project_root / "Documentation"
        self.code_path = self.project_root / "n8n_builder"
        
        # Context cache
        self.context_cache: Dict[str, ContextInfo] = {}
        self.doc_index: Dict[str, List[str]] = {}
        self.code_index: Dict[str, List[str]] = {}
        
        # Analysis patterns
        self.error_patterns = self._load_error_patterns()
        self.doc_keywords = self._load_doc_keywords()
        
        # State
        self.is_running = False
        
        self.logger.info("Context Analyzer initialized")
    
    def _load_error_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for mapping errors to relevant context."""
        return {
            'llm_communication': [
                'llm', 'ai', 'model', 'endpoint', 'connection', 'timeout',
                'mimo', 'lm_studio', 'api', 'request', 'response'
            ],
            'json_parsing': [
                'json', 'parse', 'format', 'syntax', 'structure',
                'workflow', 'nodes', 'connections', 'validation'
            ],
            'workflow_structure': [
                'workflow', 'node', 'connection', 'validation',
                'structure', 'format', 'required', 'field'
            ],
            'file_operations': [
                'file', 'path', 'directory', 'read', 'write',
                'permission', 'access', 'not found', 'exists'
            ],
            'performance': [
                'memory', 'timeout', 'slow', 'performance',
                'optimization', 'cache', 'processing'
            ],
            'system': [
                'system', 'environment', 'configuration', 'setup',
                'initialization', 'startup', 'service'
            ]
        }
    
    def _load_doc_keywords(self) -> Dict[str, List[str]]:
        """Load keywords for mapping errors to documentation."""
        return {
            'setup': ['installation', 'setup', 'configuration', 'getting started'],
            'api': ['api', 'endpoint', 'request', 'response', 'authentication'],
            'workflow': ['workflow', 'node', 'connection', 'execution'],
            'troubleshooting': ['error', 'problem', 'issue', 'fix', 'solution'],
            'integration': ['integration', 'external', 'service', 'connection'],
            'performance': ['performance', 'optimization', 'speed', 'memory']
        }
    
    async def start(self):
        """Start the context analyzer."""
        if self.is_running:
            self.logger.warning("Context Analyzer is already running")
            return
        
        self.is_running = True
        
        # Build documentation and code indices
        await self._build_documentation_index()
        await self._build_code_index()
        
        self.logger.info("Context Analyzer started successfully")
    
    async def stop(self):
        """Stop the context analyzer."""
        if not self.is_running:
            return
        
        self.is_running = False
        self.logger.info("Context Analyzer stopped")
    
    async def analyze_error(self, error_detail: ErrorDetail) -> Dict[str, Any]:
        """
        Analyze an error and gather comprehensive context.
        
        Args:
            error_detail: The error to analyze
            
        Returns:
            Dictionary containing comprehensive context information
        """
        try:
            # Get error_id from context if available
            error_id = error_detail.context.get('error_id', 'unknown') if error_detail.context else 'unknown'
            
            self.logger.info(f"Analyzing context for error: {error_id}")
            
            # Create context info structure
            context_info = ContextInfo(
                error_id=error_id,
                timestamp=datetime.now(),
                error_detail=error_detail,
                error_category=error_detail.category.value if hasattr(error_detail.category, 'value') else str(error_detail.category),
                error_severity=error_detail.severity.value if hasattr(error_detail.severity, 'value') else str(error_detail.severity)
            )
            
            # Gather different types of context
            await asyncio.gather(
                self._gather_code_context(context_info),
                self._gather_documentation_context(context_info),
                self._gather_system_context(context_info),
                self._gather_historical_context(context_info),
                self._analyze_dependencies(context_info)
            )
            
            # Cache the context
            self.context_cache[error_id] = context_info
            
            # Convert to dictionary for return
            context_dict = {
                'error_id': context_info.error_id,
                'timestamp': context_info.timestamp.isoformat(),
                'error_category': context_info.error_category,
                'error_severity': context_info.error_severity,
                'related_files': context_info.related_files,
                'code_snippets': context_info.code_snippets,
                'function_calls': context_info.function_calls,
                'relevant_docs': context_info.relevant_docs,
                'api_references': context_info.api_references,
                'system_state': context_info.system_state,
                'recent_changes': context_info.recent_changes,
                'similar_errors': context_info.similar_errors,
                'previous_solutions': context_info.previous_solutions,
                'affected_components': context_info.affected_components,
                'dependency_chain': context_info.dependency_chain
            }
            
            self.logger.info(f"Context analysis completed for error: {error_id}")
            return context_dict
            
        except Exception as e:
            self.logger.error(f"Error during context analysis: {e}")
            return {
                'error_id': error_id,
                'timestamp': datetime.now().isoformat(),
                'error_category': 'unknown',
                'error_severity': 'error',
                'analysis_error': str(e)
            }
    
    async def _gather_code_context(self, context_info: ContextInfo):
        """Gather relevant code context for the error."""
        try:
            error_message = context_info.error_detail.message.lower()
            technical_details = (context_info.error_detail.technical_details or "").lower()
            
            # Extract potential file names and function names from error
            file_patterns = re.findall(r'[\w/\\]+\.py', error_message + " " + technical_details)
            function_patterns = re.findall(r'(\w+)\(', error_message + " " + technical_details)
            
            # Search for relevant files
            for pattern in file_patterns:
                file_path = self.project_root / pattern
                if file_path.exists():
                    context_info.related_files.append({
                        'path': str(file_path),
                        'type': 'direct_reference',
                        'relevance': 'high'
                    })
            
            # Search for files containing error keywords
            error_keywords = self._extract_error_keywords(context_info)
            for keyword in error_keywords:
                matching_files = await self._search_code_for_keyword(keyword)
                for file_info in matching_files[:5]:  # Limit to top 5 matches
                    context_info.related_files.append(file_info)
            
            # Store function calls mentioned in error
            context_info.function_calls.extend(function_patterns)
            
        except Exception as e:
            self.logger.error(f"Error gathering code context: {e}")
    
    async def _gather_documentation_context(self, context_info: ContextInfo):
        """Gather relevant documentation context for the error."""
        try:
            error_keywords = self._extract_error_keywords(context_info)
            
            # Search documentation for relevant content
            for keyword in error_keywords:
                matching_docs = await self._search_docs_for_keyword(keyword)
                for doc_info in matching_docs[:3]:  # Limit to top 3 matches
                    context_info.relevant_docs.append(doc_info)
            
            # Add category-specific documentation
            category_docs = await self._get_category_documentation(context_info.error_category)
            context_info.relevant_docs.extend(category_docs)
            
        except Exception as e:
            self.logger.error(f"Error gathering documentation context: {e}")
    
    async def _gather_system_context(self, context_info: ContextInfo):
        """Gather current system state context."""
        try:
            # Get basic system information
            context_info.system_state = {
                'timestamp': datetime.now().isoformat(),
                'project_root': str(self.project_root),
                'python_version': sys.version,
                'platform': os.name
            }
            
            # Check if key services are running
            # This would be expanded based on specific system requirements
            
        except Exception as e:
            self.logger.error(f"Error gathering system context: {e}")
    
    async def _gather_historical_context(self, context_info: ContextInfo):
        """Gather historical context about similar errors."""
        try:
            # Search for similar errors in cache
            similar_errors = []
            for cached_id, cached_context in self.context_cache.items():
                if cached_id != context_info.error_id:
                    similarity = self._calculate_error_similarity(context_info, cached_context)
                    if similarity > 0.7:  # High similarity threshold
                        similar_errors.append({
                            'error_id': cached_id,
                            'similarity': similarity,
                            'timestamp': cached_context.timestamp.isoformat(),
                            'category': cached_context.error_category
                        })
            
            # Sort by similarity and take top 5
            similar_errors.sort(key=lambda x: x['similarity'], reverse=True)
            context_info.similar_errors = similar_errors[:5]
            
        except Exception as e:
            self.logger.error(f"Error gathering historical context: {e}")
    
    async def _analyze_dependencies(self, context_info: ContextInfo):
        """Analyze component dependencies and affected systems."""
        try:
            # Map error categories to affected components
            category_components = {
                'llm_communication': ['n8n_builder.py', 'enhanced_prompt_builder.py', 'config.py'],
                'json_parsing': ['validators.py', 'workflow_differ.py'],
                'workflow_structure': ['n8n_builder.py', 'validators.py', 'project_manager.py'],
                'performance': ['performance_optimizer.py', 'retry_manager.py'],
                'system': ['config.py', 'logging_config.py', 'app.py']
            }
            
            components = category_components.get(context_info.error_category, [])
            context_info.affected_components = components
            
            # Build dependency chain (simplified)
            context_info.dependency_chain = self._build_dependency_chain(components)
            
        except Exception as e:
            self.logger.error(f"Error analyzing dependencies: {e}")
    
    def _extract_error_keywords(self, context_info: ContextInfo) -> List[str]:
        """Extract relevant keywords from error information."""
        keywords = set()
        
        # Extract from error message and technical details
        text_sources = [
            context_info.error_detail.message,
            context_info.error_detail.technical_details or "",
            context_info.error_detail.title
        ]
        
        for text in text_sources:
            if text:
                # Simple keyword extraction (could be enhanced with NLP)
                words = re.findall(r'\b\w+\b', text.lower())
                keywords.update(word for word in words if len(word) > 3)
        
        # Add category-specific keywords
        category_keywords = self.error_patterns.get(context_info.error_category, [])
        keywords.update(category_keywords)
        
        return list(keywords)[:20]  # Limit to top 20 keywords

    async def _build_documentation_index(self):
        """Build an index of documentation files and their content."""
        try:
            if not self.docs_path.exists():
                self.logger.warning(f"Documentation path does not exist: {self.docs_path}")
                return

            for doc_file in self.docs_path.rglob("*.md"):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()

                    # Extract keywords from content
                    keywords = re.findall(r'\b\w+\b', content)
                    keyword_counts = {}
                    for keyword in keywords:
                        if len(keyword) > 3:
                            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

                    # Store top keywords for this document
                    top_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)[:50]
                    self.doc_index[str(doc_file)] = [kw[0] for kw in top_keywords]

                except Exception as e:
                    self.logger.error(f"Error indexing document {doc_file}: {e}")

            self.logger.info(f"Indexed {len(self.doc_index)} documentation files")

        except Exception as e:
            self.logger.error(f"Error building documentation index: {e}")

    async def _build_code_index(self):
        """Build an index of code files and their content."""
        try:
            if not self.code_path.exists():
                self.logger.warning(f"Code path does not exist: {self.code_path}")
                return

            for code_file in self.code_path.rglob("*.py"):
                try:
                    with open(code_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()

                    # Extract function names, class names, and keywords
                    functions = re.findall(r'def (\w+)', content)
                    classes = re.findall(r'class (\w+)', content)
                    keywords = re.findall(r'\b\w+\b', content)

                    # Combine all identifiers
                    all_identifiers = functions + classes + [kw for kw in keywords if len(kw) > 3]

                    # Count occurrences
                    identifier_counts = {}
                    for identifier in all_identifiers:
                        identifier_counts[identifier] = identifier_counts.get(identifier, 0) + 1

                    # Store top identifiers for this file
                    top_identifiers = sorted(identifier_counts.items(), key=lambda x: x[1], reverse=True)[:50]
                    self.code_index[str(code_file)] = [id[0] for id in top_identifiers]

                except Exception as e:
                    self.logger.error(f"Error indexing code file {code_file}: {e}")

            self.logger.info(f"Indexed {len(self.code_index)} code files")

        except Exception as e:
            self.logger.error(f"Error building code index: {e}")

    async def _search_code_for_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search code files for a specific keyword."""
        matches = []

        for file_path, keywords in self.code_index.items():
            if keyword in keywords:
                # Calculate relevance based on keyword frequency
                relevance = keywords.count(keyword) / len(keywords)
                matches.append({
                    'path': file_path,
                    'type': 'keyword_match',
                    'relevance': min(relevance * 10, 1.0),  # Normalize to 0-1
                    'keyword': keyword
                })

        # Sort by relevance
        matches.sort(key=lambda x: x['relevance'], reverse=True)
        return matches

    async def _search_docs_for_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search documentation files for a specific keyword."""
        matches = []

        for file_path, keywords in self.doc_index.items():
            if keyword in keywords:
                # Calculate relevance based on keyword frequency
                relevance = keywords.count(keyword) / len(keywords)
                matches.append({
                    'path': file_path,
                    'type': 'documentation',
                    'relevance': min(relevance * 10, 1.0),  # Normalize to 0-1
                    'keyword': keyword
                })

        # Sort by relevance
        matches.sort(key=lambda x: x['relevance'], reverse=True)
        return matches

    async def _get_category_documentation(self, category: str) -> List[Dict[str, Any]]:
        """Get documentation specific to an error category."""
        category_docs = []

        # Map categories to specific documentation files
        category_mappings = {
            'llm_communication': ['MCP_RESEARCH_SETUP_GUIDE.md', 'TROUBLESHOOTING.md'],
            'json_parsing': ['ValidationPRD.md', 'API_DOCUMENTATION.md'],
            'workflow_structure': ['NN_Builder.md', 'INTEGRATION_GUIDE.md'],
            'performance': ['TROUBLESHOOTING.md'],
            'system': ['GETTING_STARTED.md', 'SERVER_STARTUP_METHODS.md']
        }

        doc_files = category_mappings.get(category, [])
        for doc_file in doc_files:
            doc_path = self.docs_path / doc_file
            if doc_path.exists():
                category_docs.append({
                    'path': str(doc_path),
                    'type': 'category_specific',
                    'relevance': 0.9,
                    'category': category
                })

        return category_docs

    def _calculate_error_similarity(self, error1: ContextInfo, error2: ContextInfo) -> float:
        """Calculate similarity between two errors."""
        try:
            # Simple similarity based on category, keywords, and components
            similarity = 0.0

            # Category similarity
            if error1.error_category == error2.error_category:
                similarity += 0.4

            # Keyword similarity (simplified)
            keywords1 = set(self._extract_error_keywords(error1))
            keywords2 = set(self._extract_error_keywords(error2))

            if keywords1 and keywords2:
                intersection = len(keywords1.intersection(keywords2))
                union = len(keywords1.union(keywords2))
                keyword_similarity = intersection / union if union > 0 else 0
                similarity += keyword_similarity * 0.4

            # Component similarity
            components1 = set(error1.affected_components)
            components2 = set(error2.affected_components)

            if components1 and components2:
                intersection = len(components1.intersection(components2))
                union = len(components1.union(components2))
                component_similarity = intersection / union if union > 0 else 0
                similarity += component_similarity * 0.2

            return similarity

        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0

    def _build_dependency_chain(self, components: List[str]) -> List[str]:
        """Build a simplified dependency chain for components."""
        # This is a simplified version - could be enhanced with actual dependency analysis
        dependency_order = [
            'config.py',
            'logging_config.py',
            'error_handler.py',
            'validators.py',
            'performance_optimizer.py',
            'retry_manager.py',
            'enhanced_prompt_builder.py',
            'n8n_builder.py',
            'project_manager.py',
            'app.py'
        ]

        # Return components in dependency order
        ordered_components = []
        for component in dependency_order:
            if component in components:
                ordered_components.append(component)

        # Add any remaining components
        for component in components:
            if component not in ordered_components:
                ordered_components.append(component)

        return ordered_components

    def get_cached_context(self, error_id: str) -> Optional[Dict[str, Any]]:
        """Get cached context for an error."""
        context_info = self.context_cache.get(error_id)
        if context_info:
            return {
                'error_id': context_info.error_id,
                'timestamp': context_info.timestamp.isoformat(),
                'error_category': context_info.error_category,
                'error_severity': context_info.error_severity,
                'related_files': context_info.related_files,
                'relevant_docs': context_info.relevant_docs,
                'affected_components': context_info.affected_components
            }
        return None

    def clear_old_context(self, max_age_hours: int = 24):
        """Clear old context information from cache."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)

        old_context_ids = [
            context_id for context_id, context_info in self.context_cache.items()
            if context_info.timestamp < cutoff_time
        ]

        for context_id in old_context_ids:
            del self.context_cache[context_id]

        if old_context_ids:
            self.logger.info(f"Cleared {len(old_context_ids)} old context entries")
