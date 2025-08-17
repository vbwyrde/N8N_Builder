"""
MCP Research Tool for N8N Workflow Generation

This module implements the Model Context Protocol (MCP) tool for researching
n8n documentation, community examples, and best practices in real-time.
"""

import asyncio
import json
import re
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
import logging

import httpx
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None
    logger = logging.getLogger(__name__)
    logger.warning("BeautifulSoup not available - web scraping features will be limited")

from .knowledge_cache import EnhancedKnowledgeCache

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class ResearchResult:
    """Container for research findings."""
    source: str
    title: str
    content: str
    url: str
    relevance_score: float
    timestamp: float
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class NodeDocumentation:
    """Container for n8n node documentation."""
    node_name: str
    node_type: str
    description: str
    parameters: Dict[str, Any]
    examples: List[Dict[str, Any]]
    best_practices: List[str]
    common_issues: List[str]

@dataclass
class WorkflowPattern:
    """Container for workflow patterns and examples."""
    pattern_name: str
    description: str
    use_cases: List[str]
    example_workflow: Dict[str, Any]
    complexity_level: str
    required_nodes: List[str]

class N8NResearchTool:
    """
    MCP tool for researching n8n documentation and best practices.
    
    This tool can search multiple sources to gather current information
    about n8n nodes, workflows, and integration patterns.
    """
    
    def __init__(self, cache_ttl: int = 3600, enable_enhanced_cache: bool = True, github_api_token: Optional[str] = None):
        """
        Initialize the research tool.

        Args:
            cache_ttl: Time-to-live for cached results in seconds
            enable_enhanced_cache: Whether to use enhanced knowledge cache
            github_api_token: GitHub API token for authenticated requests
        """
        self.cache_ttl = cache_ttl
        self.session = None
        self.github_api_token = github_api_token

        # Initialize enhanced knowledge cache
        self.use_enhanced_cache = enable_enhanced_cache
        if enable_enhanced_cache:
            try:
                self.enhanced_cache = EnhancedKnowledgeCache(
                    cache_dir="cache/research",
                    default_ttl=cache_ttl,
                    max_memory_size=50 * 1024 * 1024,  # 50MB
                    enable_persistence=True
                )
                logger.info("Enhanced knowledge cache initialized for research tool")
            except Exception as e:
                logger.warning(f"Failed to initialize enhanced cache, falling back to simple cache: {e}")
                self.use_enhanced_cache = False
                self.enhanced_cache = None

        # Fallback to simple cache
        if not self.use_enhanced_cache:
            self.simple_cache = {}
            logger.info("Using simple cache for research tool")
        
        # Research sources configuration - Updated with current API endpoints
        self.sources = {
            'official_docs': 'https://docs.n8n.io/',
            'community_forum': 'https://community.n8n.io/',
            'github_main': 'https://github.com/n8n-io/n8n',
            'github_docs_repo': 'https://github.com/n8n-io/n8n-docs',
            'github_api_docs': 'https://api.github.com/repos/n8n-io/n8n-docs/contents/docs',
            'github_api_nodes': 'https://api.github.com/repos/n8n-io/n8n/contents/packages/nodes-base/nodes',
            'github_workflows': 'https://github.com/n8n-io/n8n/tree/master/packages/nodes-base/nodes',
            'templates': 'https://n8n.io/workflows/',
            'workflow_examples': 'https://api.github.com/search/repositories?q=n8n+workflow+topic:n8n'
        }
        
        # Request headers to appear as a legitimate browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }

        # Add GitHub authentication if token is provided
        if self.github_api_token:
            self.github_headers = self.headers.copy()
            self.github_headers.update({
                'Authorization': f'token {self.github_api_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
            logger.info("GitHub API authentication configured")
        else:
            self.github_headers = self.headers.copy()
            logger.warning("No GitHub API token provided - using unauthenticated requests (rate limited)")
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = httpx.AsyncClient(
            headers=self.headers,
            timeout=30.0,
            follow_redirects=True
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.aclose()
    
    def _get_cache_key(self, method: str, *args) -> str:
        """Generate cache key for method and arguments."""
        return f"{method}:{':'.join(str(arg) for arg in args)}"
    
    def _get_cached_result(self, method: str, *args, **kwargs) -> Any:
        """Get cached result if valid."""
        if self.use_enhanced_cache and self.enhanced_cache:
            return self.enhanced_cache.get(method, *args, **kwargs)
        else:
            # Simple cache fallback
            cache_key = self._get_cache_key(method, *args, **kwargs)
            if cache_key in self.simple_cache:
                cached_data = self.simple_cache[cache_key]
                if (time.time() - cached_data['timestamp']) < self.cache_ttl:
                    return cached_data['result']
                else:
                    # Remove expired entry
                    del self.simple_cache[cache_key]
            return None

    def _cache_result(self, method: str, result: Any, source: str, *cache_args, **kwargs) -> None:
        """Cache a result with explicit source and cache key arguments."""
        if self.use_enhanced_cache and self.enhanced_cache:
            # Debug: print what we're trying to pass
            logger.debug(f"Caching: method={method}, source={source}, cache_args={cache_args}, kwargs={kwargs}")

            # Call put with proper parameter order - *args first, then keyword arguments
            try:
                self.enhanced_cache.put(method, result, *cache_args, source=source, **kwargs)
            except TypeError as e:
                logger.warning(f"Enhanced cache put failed: {e}, falling back to simple cache")
                # Fall back to simple cache
                cache_key = self._get_cache_key(method, *cache_args, **kwargs)
                if not hasattr(self, 'simple_cache'):
                    self.simple_cache = {}
                self.simple_cache[cache_key] = {
                    'result': result,
                    'timestamp': time.time()
                }
        else:
            # Simple cache fallback
            cache_key = self._get_cache_key(method, *cache_args, **kwargs)
            self.simple_cache[cache_key] = {
                'result': result,
                'timestamp': time.time()
            }
    
    async def search_n8n_docs(self, query: str, node_type: Optional[str] = None) -> List[ResearchResult]:
        """
        Search official n8n documentation using direct page access and content scraping.

        Args:
            query: Search query
            node_type: Optional specific node type to focus on

        Returns:
            List of research results from official documentation
        """
        cached = self._get_cached_result('search_docs', query, node_type or '')
        if cached:
            logger.info(f"Using cached docs search for: {query}")
            return cached

        logger.info(f"Searching n8n docs for: {query}")
        results = []

        try:
            # Ensure session is available
            if not self.session:
                logger.warning("Session not available for n8n docs search")
                return []

            # Since n8n docs doesn't have a public search API, we'll search specific sections
            # based on the query content and node type
            search_targets = self._get_documentation_targets(query, node_type)

            for target in search_targets:
                try:
                    result = None

                    # Handle different source types
                    if target['source'] == 'web':
                        # Original web scraping approach for official docs
                        doc_url = f"{self.sources['official_docs']}{target['path']}"
                        response = await self.session.get(doc_url)

                        if response.status_code == 200:
                            if BeautifulSoup is None:
                                # Fallback: use simple text extraction
                                content = response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                                title = target['title']
                                relevance = self._calculate_relevance(query, content)

                                result = ResearchResult(
                                    source='official_docs',
                                    title=title,
                                    content=content,
                                    url=doc_url,
                                    relevance_score=relevance,
                                    timestamp=time.time(),
                                    metadata={'section': target['section']}
                                )
                            else:
                                soup = BeautifulSoup(response.text, 'html.parser')

                                # Extract main content with improved targeting
                                main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
                                if main_content and hasattr(main_content, 'find_all'):
                                    title_elem = soup.find('h1')
                                    title = title_elem.get_text(strip=True) if title_elem else target['title']

                                    # Remove navigation and sidebar elements
                                    for nav in main_content.find_all(['nav', 'aside', 'header', 'footer']):
                                        nav.decompose()

                                    # Remove elements with navigation-related classes
                                    for elem in main_content.find_all(class_=['nav', 'navigation', 'sidebar', 'menu', 'breadcrumb']):
                                        elem.decompose()

                                    # Extract meaningful content paragraphs
                                    content_parts = []

                                    # Look for specific documentation sections first
                                    doc_sections = main_content.find_all(['section', 'div'], class_=['description', 'parameters', 'examples', 'usage'])
                                    if doc_sections:
                                        for section in doc_sections[:2]:  # First 2 sections
                                            text = section.get_text(strip=True)
                                            if text and len(text) > 50:
                                                content_parts.append(text)

                                    # If no specific sections, get paragraphs and list items
                                    if not content_parts:
                                        for elem in main_content.find_all(['p', 'li', 'dd'], limit=15):
                                            if hasattr(elem, 'get_text'):
                                                text = elem.get_text(strip=True)
                                                if text and len(text) > 30:  # Skip very short text
                                                    # Skip navigation-like text
                                                    if not any(nav_word in text.lower() for nav_word in ['menu', 'navigation', 'breadcrumb', 'skip to']):
                                                        content_parts.append(text)

                                    if content_parts:
                                        content = ' '.join(content_parts[:4])  # First 4 relevant parts
                                        if len(content) > 1500:
                                            content = content[:1500] + "..."

                                        relevance = self._calculate_relevance(query, title + ' ' + content)

                                        result = ResearchResult(
                                            source='official_docs',
                                            title=title,
                                            content=content,
                                            url=doc_url,
                                            relevance_score=relevance,
                                            timestamp=time.time(),
                                            metadata={'section': target['section']}
                                        )
                        else:
                            logger.debug(f"Failed to fetch documentation from {doc_url}: {response.status_code}")

                    elif target['source'] == 'github_api':
                        # Use GitHub API for documentation
                        result = await self._search_github_docs_api(target['path'], target['title'])

                    elif target['source'] == 'github_nodes':
                        # Use GitHub API for node definitions
                        result = await self._search_github_node_definitions(target['path'])

                    if result:
                        results.append(result)

                    # Add small delay to be respectful to the server
                    await asyncio.sleep(0.5)

                except Exception as e:
                    logger.warning(f"Error accessing documentation target {target['path']}: {str(e)}")
                    continue

            # If no results from targeted search, try direct node documentation
            if not results and node_type:
                node_results = await self._search_node_documentation(node_type)
                results.extend(node_results)

        except Exception as e:
            logger.error(f"Error searching n8n docs: {str(e)}")
            # Return empty results rather than failing
            results = []

        # Cache and return results
        self._cache_result('search_docs', results, 'official_docs', query, node_type or '')
        return results

    def _get_documentation_targets(self, query: str, node_type: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Get targeted documentation URLs based on query content and node type.
        Updated with current N8N documentation structure.

        Args:
            query: Search query
            node_type: Optional node type

        Returns:
            List of documentation targets with path, title, section, and source type
        """
        targets = []
        query_lower = query.lower()

        # Core concepts based on query keywords - Updated paths
        if any(keyword in query_lower for keyword in ['webhook', 'trigger', 'http']):
            targets.extend([
                {'path': 'integrations/builtin/core-nodes/n8n-nodes-base.webhook/', 'title': 'Webhook Node', 'section': 'core_nodes', 'source': 'web'},
                {'path': 'integrations/builtin/core-nodes/n8n-nodes-base.httprequest/', 'title': 'HTTP Request Node', 'section': 'core_nodes', 'source': 'web'},
                {'path': 'workflows/components/nodes.md', 'title': 'Understanding Nodes', 'section': 'concepts', 'source': 'github_api'},
                {'path': 'Webhook', 'title': 'Webhook Node Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        if any(keyword in query_lower for keyword in ['email', 'notification', 'send']):
            targets.extend([
                {'path': 'integrations/builtin/core-nodes/n8n-nodes-base.sendemail/', 'title': 'Send Email Node', 'section': 'core_nodes', 'source': 'web'},
                {'path': 'integrations/builtin/app-nodes/n8n-nodes-base.gmail/', 'title': 'Gmail Node', 'section': 'app_nodes', 'source': 'web'},
                {'path': 'Gmail', 'title': 'Gmail Node Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        if any(keyword in query_lower for keyword in ['database', 'sql', 'mysql', 'postgres']):
            targets.extend([
                {'path': 'integrations/builtin/app-nodes/n8n-nodes-base.mysql/', 'title': 'MySQL Node', 'section': 'app_nodes', 'source': 'web'},
                {'path': 'integrations/builtin/app-nodes/n8n-nodes-base.postgres/', 'title': 'PostgreSQL Node', 'section': 'app_nodes', 'source': 'web'},
                {'path': 'MySql', 'title': 'MySQL Node Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        if any(keyword in query_lower for keyword in ['schedule', 'cron', 'timer']):
            targets.extend([
                {'path': 'integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/', 'title': 'Schedule Trigger', 'section': 'core_nodes', 'source': 'web'},
                {'path': 'ScheduleTrigger', 'title': 'Schedule Trigger Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        if any(keyword in query_lower for keyword in ['code', 'javascript', 'function']):
            targets.extend([
                {'path': 'integrations/builtin/core-nodes/n8n-nodes-base.code/', 'title': 'Code Node', 'section': 'core_nodes', 'source': 'web'},
                {'path': 'Code', 'title': 'Code Node Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        # If specific node type is provided, add multiple sources
        if node_type:
            node_name_clean = node_type.replace(' ', '').replace('Request', '').replace('Node', '')
            targets.extend([
                {'path': f'integrations/builtin/core-nodes/n8n-nodes-base.{node_type.lower().replace(" ", "")}/', 'title': f'{node_type} Node', 'section': 'specific_node', 'source': 'web'},
                {'path': f'integrations/builtin/core-nodes/n8n-nodes-base.{node_type.lower().replace(" ", "")}.md', 'title': f'{node_type} Documentation', 'section': 'specific_node', 'source': 'github_api'},
                {'path': node_name_clean, 'title': f'{node_type} Node Definition', 'section': 'node_definition', 'source': 'github_nodes'}
            ])

        # Always include general workflow concepts from multiple sources
        targets.extend([
            {'path': 'workflows/', 'title': 'Understanding Workflows', 'section': 'concepts', 'source': 'web'},
            {'path': 'workflows/components/', 'title': 'Workflow Components', 'section': 'concepts', 'source': 'web'},
            {'path': 'workflows/index.md', 'title': 'Workflow Documentation', 'section': 'concepts', 'source': 'github_api'}
        ])

        # Remove duplicates while preserving order
        seen = set()
        unique_targets = []
        for target in targets:
            target_key = f"{target['path']}_{target['source']}"
            if target_key not in seen:
                seen.add(target_key)
                unique_targets.append(target)

        return unique_targets[:8]  # Increased limit for better coverage

    async def _search_github_docs_api(self, path: str, title: str) -> Optional[ResearchResult]:
        """
        Search GitHub documentation using the Contents API.

        Args:
            path: Path to the documentation file
            title: Title for the result

        Returns:
            ResearchResult if found, None otherwise
        """
        try:
            if not self.session:
                logger.warning("Session not available for GitHub API search")
                return None

            # Construct GitHub API URL
            api_url = f"{self.sources['github_api_docs']}/{path}"

            # Use GitHub-specific headers for authentication
            headers = self.github_headers if hasattr(self, 'github_headers') else self.headers

            response = await self.session.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                # GitHub API returns base64 encoded content
                if 'content' in data and data['type'] == 'file':
                    import base64
                    content_bytes = base64.b64decode(data['content'])
                    content_text = content_bytes.decode('utf-8')

                    # Extract meaningful content (skip frontmatter if present)
                    if content_text.startswith('---'):
                        parts = content_text.split('---', 2)
                        if len(parts) >= 3:
                            content_text = parts[2].strip()

                    # Limit content length
                    if len(content_text) > 2000:
                        content_text = content_text[:2000] + "..."

                    return ResearchResult(
                        source='github_docs_api',
                        title=title,
                        content=content_text,
                        url=data.get('html_url', api_url),
                        relevance_score=0.8,  # High relevance for direct API access
                        timestamp=time.time(),
                        metadata={'sha': data.get('sha'), 'size': data.get('size')}
                    )

            elif response.status_code == 404:
                logger.debug(f"GitHub documentation not found: {path}")
            else:
                logger.warning(f"GitHub API error {response.status_code} for {path}")

        except Exception as e:
            logger.error(f"Error searching GitHub docs API for {path}: {e}")

        return None

    async def _search_github_node_definitions(self, node_name: str) -> Optional[ResearchResult]:
        """
        Search GitHub for node definitions and implementations.

        Args:
            node_name: Name of the node to search for

        Returns:
            ResearchResult if found, None otherwise
        """
        try:
            if not self.session:
                logger.warning("Session not available for GitHub node search")
                return None

            # Search for node definition files
            search_url = f"https://api.github.com/search/code?q={node_name}+repo:n8n-io/n8n+filename:.node.json"

            headers = self.github_headers if hasattr(self, 'github_headers') else self.headers
            response = await self.session.get(search_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data.get('items') and len(data['items']) > 0:
                    # Get the first matching node definition
                    item = data['items'][0]

                    # Fetch the actual file content
                    content_response = await self.session.get(item['url'], headers=headers)
                    if content_response.status_code == 200:
                        content_data = content_response.json()

                        if 'content' in content_data:
                            import base64
                            content_bytes = base64.b64decode(content_data['content'])
                            content_text = content_bytes.decode('utf-8')

                            return ResearchResult(
                                source='github_node_definition',
                                title=f"{node_name} Node Definition",
                                content=content_text,
                                url=item['html_url'],
                                relevance_score=0.9,  # Very high relevance for node definitions
                                timestamp=time.time(),
                                metadata={'path': item['path'], 'repository': item['repository']['full_name']}
                            )

        except Exception as e:
            logger.error(f"Error searching GitHub node definitions for {node_name}: {e}")

        return None

    async def _search_node_documentation(self, node_type: str) -> List[ResearchResult]:
        """Search for specific node documentation."""
        results = []
        
        try:
            # Ensure session is available
            if not self.session:
                logger.warning("Session not available for node documentation search")
                return []

            # Try to find node-specific documentation
            node_url = f"{self.sources['official_docs']}integrations/builtin/core-nodes/n8n-nodes-base.{node_type}/"
            response = await self.session.get(node_url)
            
            if response.status_code == 200:
                if BeautifulSoup is None:
                    # Fallback: use simple text extraction
                    content_text = response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                    title_text = f"{node_type} Node"
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract node documentation content
                    content_div = soup.find('div', class_='content') or soup.find('main')
                    if content_div and hasattr(content_div, 'get_text'):
                        title = soup.find('h1')
                        title_text = title.get_text(strip=True) if title and hasattr(title, 'get_text') else f"{node_type} Node"
                        content_text = content_div.get_text(strip=True)[:1000]  # Limit content length
                    else:
                        # Fallback if content extraction fails
                        content_text = response.text[:1000] + "..." if len(response.text) > 1000 else response.text
                        title_text = f"{node_type} Node"
                    
                    results.append(ResearchResult(
                        source='official_docs',
                        title=title_text,
                        content=content_text,
                        url=node_url,
                        relevance_score=1.0,  # Direct match
                        timestamp=time.time(),
                        metadata={'node_type': node_type}
                    ))
        
        except Exception as e:
            logger.error(f"Error searching node documentation for {node_type}: {str(e)}")
        
        return results
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """
        Calculate relevance score between query and text.
        
        Args:
            query: Search query
            text: Text to score against
            
        Returns:
            Relevance score between 0.0 and 1.0
        """
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        
        if not query_words:
            return 0.0
        
        # Calculate word overlap
        overlap = len(query_words.intersection(text_words))
        return overlap / len(query_words)
    
    async def find_community_examples(self, workflow_type: str) -> List[ResearchResult]:
        """
        Find community workflow examples.

        Args:
            workflow_type: Type of workflow to search for

        Returns:
            List of community examples
        """
        cached = self._get_cached_result('community_examples', workflow_type)
        if cached:
            logger.info(f"Using cached community examples for: {workflow_type}")
            return cached
        
        logger.info(f"Searching community examples for: {workflow_type}")
        results = []
        
        try:
            # Ensure session is available
            if not self.session:
                logger.warning("Session not available for community search")
                return []

            # Search community forum with rate limiting awareness
            search_url = f"{self.sources['community_forum']}search?q={workflow_type}"
            response = await self.session.get(search_url)

            # Handle rate limiting
            if response.status_code == 429:
                logger.warning(f"Rate limited by community forum for query: {workflow_type}")
                # Return a placeholder result indicating rate limiting
                results.append(ResearchResult(
                    source='community_forum',
                    title=f"Community Search Rate Limited",
                    content=f"Search for '{workflow_type}' was rate limited. Please try again later or search manually at {search_url}",
                    url=search_url,
                    relevance_score=0.1,
                    timestamp=time.time(),
                    metadata={'rate_limited': True}
                ))
                return results
            
            if response.status_code == 200:
                if BeautifulSoup is None:
                    # Fallback: create a simple result from the response
                    results.append(ResearchResult(
                        source='community_forum',
                        title=f"Community Discussion: {workflow_type}",
                        content=response.text[:500] + "..." if len(response.text) > 500 else response.text,
                        url=search_url,
                        relevance_score=0.5,
                        timestamp=time.time()
                    ))
                else:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    # Extract forum posts (adapt to actual forum structure)
                    posts = soup.find_all('div', class_='topic-list-item')[:3]  # Limit to top 3
                
                for post in posts:
                    title_elem = post.find('a', class_='title')
                    excerpt_elem = post.find('div', class_='excerpt')
                    
                    if title_elem:
                        title = title_elem.get_text(strip=True)
                        content = excerpt_elem.get_text(strip=True) if excerpt_elem else ""
                        url = urljoin(self.sources['community_forum'], title_elem.get('href', ''))
                        
                        relevance = self._calculate_relevance(workflow_type, title + ' ' + content)
                        
                        results.append(ResearchResult(
                            source='community_forum',
                            title=title,
                            content=content,
                            url=url,
                            relevance_score=relevance,
                            timestamp=time.time()
                        ))
        
        except Exception as e:
            logger.error(f"Error searching community examples: {str(e)}")
            results = []
        
        self._cache_result('community_examples', results, 'community_forum', workflow_type)
        return results
    
    async def get_node_documentation(self, node_name: str) -> Optional[NodeDocumentation]:
        """
        Get detailed documentation for a specific n8n node.

        Args:
            node_name: Name of the n8n node

        Returns:
            NodeDocumentation object or None if not found
        """
        cached = self._get_cached_result('node_docs', node_name)
        if cached:
            logger.info(f"Using cached node documentation for: {node_name}")
            return cached
        
        logger.info(f"Getting node documentation for: {node_name}")
        
        try:
            # Search for node documentation
            search_results = await self.search_n8n_docs(f"{node_name} node", node_name)
            
            if search_results:
                # Use the most relevant result
                best_result = max(search_results, key=lambda x: x.relevance_score)
                
                # Extract structured information (this would need to be enhanced)
                node_doc = NodeDocumentation(
                    node_name=node_name,
                    node_type=f"n8n-nodes-base.{node_name.lower()}",
                    description=best_result.content[:500],
                    parameters={},  # Would need to parse from documentation
                    examples=[],    # Would need to extract examples
                    best_practices=[],  # Would need to extract best practices
                    common_issues=[]    # Would need to extract common issues
                )
                
                self._cache_result('node_docs', node_doc, 'node_documentation', node_name)
                return node_doc
        
        except Exception as e:
            logger.error(f"Error getting node documentation for {node_name}: {str(e)}")
        
        return None

    async def research_integration_patterns(self, services: List[str]) -> Dict[str, List[WorkflowPattern]]:
        """
        Research integration patterns for specific services.

        Args:
            services: List of service names to research

        Returns:
            Dictionary mapping service names to workflow patterns
        """
        cached = self._get_cached_result('integration_patterns', *services)
        if cached:
            logger.info(f"Using cached integration patterns for: {services}")
            return cached

        logger.info(f"Researching integration patterns for: {services}")
        patterns = {}

        for service in services:
            try:
                # Search for service-specific patterns
                search_results = await self.search_n8n_docs(f"{service} integration workflow")
                # Note: Community results could be added here if needed for pattern analysis

                service_patterns = []

                # Process search results into patterns
                for result in search_results[:2]:  # Top 2 results
                    pattern = WorkflowPattern(
                        pattern_name=f"{service} Integration",
                        description=result.content[:200],
                        use_cases=[f"{service} automation", f"{service} data sync"],
                        example_workflow={},  # Would need to extract actual workflow JSON
                        complexity_level="intermediate",
                        required_nodes=[f"{service.lower()}", "webhook"]
                    )
                    service_patterns.append(pattern)

                patterns[service] = service_patterns

            except Exception as e:
                logger.error(f"Error researching patterns for {service}: {str(e)}")
                patterns[service] = []

        self._cache_result('integration_patterns', patterns, 'integration_research', *services)
        return patterns

    async def search_github_examples(self, query: str) -> List[ResearchResult]:
        """
        Search GitHub for n8n workflow examples.

        Args:
            query: Search query

        Returns:
            List of GitHub examples
        """
        cached = self._get_cached_result('github_examples', query)
        if cached:
            logger.info(f"Using cached GitHub examples for: {query}")
            return cached

        logger.info(f"Searching GitHub for: {query}")
        results = []

        try:
            # Ensure session is available
            if not self.session:
                logger.warning("Session not available for GitHub search")
                return results

            # Search GitHub API with authentication if available
            search_url = f"https://api.github.com/search/code?q={query}+repo:n8n-io/n8n+extension:json"

            # Use GitHub-specific headers for authentication
            headers = self.github_headers if hasattr(self, 'github_headers') else self.headers
            response = await self.session.get(search_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                for item in data.get('items', [])[:3]:  # Top 3 results
                    title = item.get('name', 'Unknown')
                    url = item.get('html_url', '')

                    # Get file content
                    download_url = item.get('download_url')
                    if download_url:
                        content_response = await self.session.get(download_url)
                        if content_response.status_code == 200:
                            content = content_response.text[:1000]  # Limit content

                            relevance = self._calculate_relevance(query, title + ' ' + content)

                            results.append(ResearchResult(
                                source='github',
                                title=title,
                                content=content,
                                url=url,
                                relevance_score=relevance,
                                timestamp=time.time(),
                                metadata={'repository': 'n8n-io/n8n'}
                            ))

        except Exception as e:
            logger.error(f"Error searching GitHub: {str(e)}")
            results = []

        self._cache_result('github_examples', results, 'github', query)
        return results

    async def get_best_practices(self, workflow_type: str) -> List[str]:
        """
        Get best practices for a specific workflow type.

        Args:
            workflow_type: Type of workflow

        Returns:
            List of best practice recommendations
        """
        cached = self._get_cached_result('best_practices', workflow_type)
        if cached:
            return cached

        logger.info(f"Getting best practices for: {workflow_type}")
        best_practices = []

        try:
            # Search for best practices in documentation and community
            docs_results = await self.search_n8n_docs(f"{workflow_type} best practices")
            community_results = await self.find_community_examples(f"{workflow_type} best practices")

            # Extract best practices from results
            all_results = docs_results + community_results

            for result in all_results:
                # Look for common best practice patterns in content
                content = result.content.lower()

                if 'error handling' in content:
                    best_practices.append("Implement proper error handling with error trigger nodes")

                if 'rate limit' in content:
                    best_practices.append("Add rate limiting to prevent API throttling")

                if 'authentication' in content or 'auth' in content:
                    best_practices.append("Use secure authentication methods and store credentials safely")

                if 'webhook' in content:
                    best_practices.append("Configure webhook URLs properly for external integrations")

                if 'test' in content:
                    best_practices.append("Test workflows thoroughly before production deployment")

        except Exception as e:
            logger.error(f"Error getting best practices: {str(e)}")

        # Add default best practices
        if not best_practices:
            best_practices = [
                "Add descriptive names to all nodes",
                "Include error handling for external API calls",
                "Use environment variables for sensitive data",
                "Test workflows with sample data before activation"
            ]

        self._cache_result('best_practices', best_practices, 'best_practices_research', workflow_type)
        return best_practices

    async def comprehensive_research(self, description: str) -> Dict[str, Any]:
        """
        Perform comprehensive research for a workflow description.

        Args:
            description: Plain English workflow description

        Returns:
            Comprehensive research results
        """
        logger.info(f"Starting comprehensive research for: {description}")

        # Extract key concepts from description
        concepts = self._extract_concepts(description)

        # Perform parallel research
        tasks = []

        # Search official documentation
        tasks.append(self.search_n8n_docs(description))

        # Find community examples
        tasks.append(self.find_community_examples(description))

        # Search GitHub examples
        tasks.append(self.search_github_examples(description))

        # Get best practices
        tasks.append(self.get_best_practices(description))

        # Research integration patterns for detected services
        if concepts.get('services'):
            tasks.append(self.research_integration_patterns(concepts['services']))

        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            return {
                'official_docs': results[0] if not isinstance(results[0], Exception) else [],
                'community_examples': results[1] if not isinstance(results[1], Exception) else [],
                'github_examples': results[2] if not isinstance(results[2], Exception) else [],
                'best_practices': results[3] if not isinstance(results[3], Exception) else [],
                'integration_patterns': results[4] if len(results) > 4 and not isinstance(results[4], Exception) else {},
                'concepts': concepts,
                'research_timestamp': time.time()
            }

        except Exception as e:
            logger.error(f"Error in comprehensive research: {str(e)}")
            return {
                'official_docs': [],
                'community_examples': [],
                'github_examples': [],
                'best_practices': [],
                'integration_patterns': {},
                'concepts': concepts,
                'research_timestamp': time.time()
            }

    def _extract_concepts(self, description: str) -> Dict[str, List[str]]:
        """
        Extract key concepts from workflow description.

        Args:
            description: Workflow description

        Returns:
            Dictionary of extracted concepts
        """
        description_lower = description.lower()

        # Common service patterns
        services = []
        service_patterns = {
            'email': ['email', 'gmail', 'outlook', 'smtp'],
            'slack': ['slack'],
            'google': ['google', 'sheets', 'drive', 'calendar'],
            'github': ['github', 'git'],
            'webhook': ['webhook', 'http'],
            'database': ['database', 'mysql', 'postgres', 'mongodb'],
            'file': ['file', 'upload', 'download'],
            'twitter': ['twitter', 'tweet'],
            'discord': ['discord']
        }

        for service, patterns in service_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                services.append(service)

        # Common action patterns
        actions = []
        action_patterns = {
            'send': ['send', 'email', 'message', 'notification'],
            'create': ['create', 'add', 'new'],
            'update': ['update', 'modify', 'change'],
            'delete': ['delete', 'remove'],
            'monitor': ['monitor', 'watch', 'check'],
            'sync': ['sync', 'synchronize', 'backup']
        }

        for action, patterns in action_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                actions.append(action)

        # Common trigger patterns
        triggers = []
        trigger_patterns = {
            'webhook': ['webhook', 'http request'],
            'schedule': ['schedule', 'daily', 'hourly', 'cron'],
            'file': ['file upload', 'new file', 'file change'],
            'email': ['new email', 'email received'],
            'manual': ['manual', 'button', 'trigger']
        }

        for trigger, patterns in trigger_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                triggers.append(trigger)

        return {
            'services': services,
            'actions': actions,
            'triggers': triggers,
            'keywords': description.split()
        }

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache performance statistics."""
        if self.use_enhanced_cache and self.enhanced_cache:
            return self.enhanced_cache.get_stats()
        else:
            # Simple cache stats
            return {
                'cache_type': 'simple',
                'entries': len(self.simple_cache),
                'memory_size_bytes': sum(len(str(v)) for v in self.simple_cache.values())
            }

    def clear_cache(self):
        """Clear all cached data."""
        if self.use_enhanced_cache and self.enhanced_cache:
            self.enhanced_cache.clear()
        else:
            self.simple_cache.clear()
        logger.info("Research cache cleared")
