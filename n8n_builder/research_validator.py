"""
Research Validation System for MCP Research Tool

This module validates the quality and accuracy of research results
to ensure they provide useful information for workflow generation.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse

from .mcp_research_tool import ResearchResult, NodeDocumentation, WorkflowPattern

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of research validation."""
    is_valid: bool
    quality_score: float
    issues: List[str]
    recommendations: List[str]
    metadata: Dict[str, Any]

class ResearchValidator:
    """
    Validates research results for quality and usefulness.
    """
    
    def __init__(self, min_quality_score: float = 0.6):
        """
        Initialize the research validator.
        
        Args:
            min_quality_score: Minimum quality score for valid research
        """
        self.min_quality_score = min_quality_score
        
        # Quality criteria weights
        self.weights = {
            'relevance': 0.3,
            'completeness': 0.25,
            'freshness': 0.2,
            'source_credibility': 0.15,
            'content_quality': 0.1
        }
    
    def validate_research_results(self, results: List[ResearchResult], query: str) -> ValidationResult:
        """
        Validate a list of research results.
        
        Args:
            results: List of research results to validate
            query: Original search query
            
        Returns:
            ValidationResult with quality assessment
        """
        if not results:
            return ValidationResult(
                is_valid=False,
                quality_score=0.0,
                issues=["No research results found"],
                recommendations=["Try broader search terms", "Check internet connectivity"],
                metadata={'result_count': 0}
            )
        
        issues = []
        recommendations = []
        scores = []
        
        for result in results:
            result_validation = self._validate_single_result(result, query)
            scores.append(result_validation.quality_score)
            issues.extend(result_validation.issues)
            recommendations.extend(result_validation.recommendations)
        
        # Calculate overall quality score
        overall_score = sum(scores) / len(scores) if scores else 0.0
        
        # Check for common issues
        self._check_common_issues(results, issues, recommendations)
        
        # Remove duplicate recommendations
        recommendations = list(set(recommendations))
        
        return ValidationResult(
            is_valid=overall_score >= self.min_quality_score,
            quality_score=overall_score,
            issues=issues,
            recommendations=recommendations,
            metadata={
                'result_count': len(results),
                'average_relevance': sum(r.relevance_score for r in results) / len(results),
                'source_diversity': len(set(r.source for r in results)),
                'validation_timestamp': time.time()
            }
        )
    
    def _validate_single_result(self, result: ResearchResult, query: str) -> ValidationResult:
        """Validate a single research result."""
        issues = []
        recommendations = []
        
        # Calculate component scores
        relevance_score = self._score_relevance(result, query)
        completeness_score = self._score_completeness(result)
        freshness_score = self._score_freshness(result)
        source_score = self._score_source_credibility(result)
        content_score = self._score_content_quality(result)
        
        # Calculate weighted overall score
        overall_score = (
            relevance_score * self.weights['relevance'] +
            completeness_score * self.weights['completeness'] +
            freshness_score * self.weights['freshness'] +
            source_score * self.weights['source_credibility'] +
            content_score * self.weights['content_quality']
        )
        
        # Identify issues
        if relevance_score < 0.5:
            issues.append(f"Low relevance score ({relevance_score:.2f}) for result: {result.title}")
            recommendations.append("Refine search terms for better relevance")
        
        if completeness_score < 0.4:
            issues.append(f"Incomplete content in result: {result.title}")
            recommendations.append("Look for more detailed documentation sources")
        
        if freshness_score < 0.3:
            issues.append(f"Potentially outdated content: {result.title}")
            recommendations.append("Verify information with recent sources")
        
        if source_score < 0.6:
            issues.append(f"Low credibility source: {result.source}")
            recommendations.append("Prioritize official documentation sources")
        
        return ValidationResult(
            is_valid=overall_score >= self.min_quality_score,
            quality_score=overall_score,
            issues=issues,
            recommendations=recommendations,
            metadata={
                'relevance_score': relevance_score,
                'completeness_score': completeness_score,
                'freshness_score': freshness_score,
                'source_score': source_score,
                'content_score': content_score
            }
        )
    
    def _score_relevance(self, result: ResearchResult, query: str) -> float:
        """Score the relevance of a result to the query."""
        # Use the existing relevance score from the result
        base_score = result.relevance_score
        
        # Boost score for exact matches in title
        query_words = set(query.lower().split())
        title_words = set(result.title.lower().split())
        title_match_ratio = len(query_words.intersection(title_words)) / len(query_words) if query_words else 0
        
        # Boost score for n8n-specific content
        n8n_indicators = ['n8n', 'workflow', 'node', 'automation']
        content_lower = result.content.lower()
        n8n_score = sum(1 for indicator in n8n_indicators if indicator in content_lower) / len(n8n_indicators)
        
        # Combine scores
        final_score = (base_score * 0.6) + (title_match_ratio * 0.3) + (n8n_score * 0.1)
        return min(final_score, 1.0)
    
    def _score_completeness(self, result: ResearchResult) -> float:
        """Score the completeness of the result content."""
        content_length = len(result.content)
        
        # Score based on content length (more content generally better)
        if content_length < 50:
            length_score = 0.2
        elif content_length < 200:
            length_score = 0.5
        elif content_length < 500:
            length_score = 0.8
        else:
            length_score = 1.0
        
        # Check for key information indicators
        content_lower = result.content.lower()
        info_indicators = [
            'parameter', 'configuration', 'example', 'usage',
            'setup', 'install', 'connect', 'authenticate'
        ]
        info_score = sum(1 for indicator in info_indicators if indicator in content_lower) / len(info_indicators)
        
        return (length_score * 0.7) + (info_score * 0.3)
    
    def _score_freshness(self, result: ResearchResult) -> float:
        """Score the freshness of the result."""
        current_time = time.time()
        age_hours = (current_time - result.timestamp) / 3600
        
        # Score based on age (fresher is better)
        if age_hours < 1:
            return 1.0
        elif age_hours < 24:
            return 0.9
        elif age_hours < 168:  # 1 week
            return 0.7
        elif age_hours < 720:  # 1 month
            return 0.5
        else:
            return 0.3
    
    def _score_source_credibility(self, result: ResearchResult) -> float:
        """Score the credibility of the source."""
        source_scores = {
            'official_docs': 1.0,
            'github': 0.9,
            'community_forum': 0.8,
            'templates': 0.7,
            'unknown': 0.3
        }
        
        base_score = source_scores.get(result.source, 0.3)
        
        # Boost score for official n8n domains
        if result.url:
            parsed_url = urlparse(result.url)
            domain = parsed_url.netloc.lower()
            
            if 'n8n.io' in domain:
                base_score = min(base_score + 0.2, 1.0)
            elif 'github.com/n8n-io' in result.url.lower():
                base_score = min(base_score + 0.1, 1.0)
        
        return base_score
    
    def _score_content_quality(self, result: ResearchResult) -> float:
        """Score the quality of the content."""
        content = result.content.lower()
        
        # Check for quality indicators
        quality_indicators = [
            'example', 'tutorial', 'guide', 'documentation',
            'step', 'instruction', 'configuration', 'setup'
        ]
        quality_score = sum(1 for indicator in quality_indicators if indicator in content) / len(quality_indicators)
        
        # Penalize for poor quality indicators
        poor_quality_indicators = [
            'error', 'broken', 'deprecated', 'outdated',
            'not working', 'issue', 'problem'
        ]
        penalty = sum(1 for indicator in poor_quality_indicators if indicator in content) * 0.1
        
        final_score = max(quality_score - penalty, 0.0)
        return min(final_score, 1.0)
    
    def _check_common_issues(self, results: List[ResearchResult], issues: List[str], recommendations: List[str]):
        """Check for common issues across all results."""
        
        # Check source diversity
        sources = set(r.source for r in results)
        if len(sources) < 2:
            issues.append("Limited source diversity - all results from same source")
            recommendations.append("Expand search to include multiple sources")
        
        # Check for very low relevance scores
        avg_relevance = sum(r.relevance_score for r in results) / len(results)
        if avg_relevance < 0.4:
            issues.append(f"Overall low relevance scores (avg: {avg_relevance:.2f})")
            recommendations.append("Refine search query for better results")
        
        # Check for very short content
        avg_content_length = sum(len(r.content) for r in results) / len(results)
        if avg_content_length < 100:
            issues.append(f"Very short content on average ({avg_content_length:.0f} chars)")
            recommendations.append("Look for more detailed documentation")
        
        # Check for missing URLs
        missing_urls = sum(1 for r in results if not r.url)
        if missing_urls > len(results) * 0.3:
            issues.append(f"{missing_urls} results missing source URLs")
            recommendations.append("Ensure proper URL tracking for source verification")
    
    def validate_comprehensive_research(self, research_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate comprehensive research results.
        
        Args:
            research_data: Complete research results from comprehensive_research()
            
        Returns:
            ValidationResult for the entire research set
        """
        issues = []
        recommendations = []
        component_scores = []
        
        # Validate each component
        components = ['official_docs', 'community_examples', 'github_examples']
        
        for component in components:
            results = research_data.get(component, [])
            if results:
                validation = self.validate_research_results(results, "comprehensive")
                component_scores.append(validation.quality_score)
                issues.extend([f"{component}: {issue}" for issue in validation.issues])
                recommendations.extend(validation.recommendations)
            else:
                issues.append(f"No results found for {component}")
                recommendations.append(f"Improve {component} search capabilities")
        
        # Validate best practices
        best_practices = research_data.get('best_practices', [])
        if not best_practices:
            issues.append("No best practices found")
            recommendations.append("Implement fallback best practices")
        elif len(best_practices) < 3:
            issues.append("Limited best practices found")
            recommendations.append("Expand best practices research")
        
        # Validate concepts
        concepts = research_data.get('concepts', {})
        if not concepts.get('services'):
            issues.append("No services detected in concepts")
            recommendations.append("Improve concept extraction for services")
        
        # Calculate overall score
        overall_score = sum(component_scores) / len(component_scores) if component_scores else 0.0
        
        # Boost score for having multiple components
        component_bonus = len([c for c in components if research_data.get(c)]) * 0.1
        overall_score = min(overall_score + component_bonus, 1.0)
        
        return ValidationResult(
            is_valid=overall_score >= self.min_quality_score and len(component_scores) >= 2,
            quality_score=overall_score,
            issues=list(set(issues)),
            recommendations=list(set(recommendations)),
            metadata={
                'components_found': len(component_scores),
                'best_practices_count': len(best_practices),
                'services_detected': len(concepts.get('services', [])),
                'validation_timestamp': time.time()
            }
        )
