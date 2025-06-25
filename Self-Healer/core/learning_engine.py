"""
Learning Engine - Learns from healing results to improve future performance.

This module implements machine learning and pattern recognition capabilities
to continuously improve the self-healing system's effectiveness.
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from collections import defaultdict, Counter
import pickle

# Import existing N8N Builder components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from n8n_builder.error_handler import ErrorDetail
from n8n_builder.logging_config import get_logger


@dataclass
class LearningRecord:
    """Record of a healing attempt for learning purposes."""
    record_id: str
    timestamp: datetime
    
    # Error information
    error_category: str
    error_severity: str
    error_keywords: List[str] = field(default_factory=list)
    
    # Solution information
    solution_type: str
    solution_confidence: float
    solution_steps: List[str] = field(default_factory=list)
    
    # Context information
    affected_components: List[str] = field(default_factory=list)
    system_state: Dict[str, Any] = field(default_factory=dict)
    
    # Outcome information
    success: bool = False
    implementation_time: float = 0.0
    verification_results: Dict[str, Any] = field(default_factory=dict)
    
    # Learning metadata
    pattern_matches: List[str] = field(default_factory=list)
    effectiveness_score: float = 0.0


@dataclass
class Pattern:
    """Learned pattern for error-solution mapping."""
    pattern_id: str
    pattern_type: str  # 'error_pattern', 'solution_pattern', 'context_pattern'
    
    # Pattern definition
    conditions: Dict[str, Any] = field(default_factory=dict)
    triggers: List[str] = field(default_factory=list)
    
    # Pattern statistics
    occurrence_count: int = 0
    success_count: int = 0
    failure_count: int = 0
    average_effectiveness: float = 0.0
    
    # Pattern metadata
    first_seen: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    confidence: float = 0.0


@dataclass
class LearningInsight:
    """Insight derived from learning analysis."""
    insight_id: str
    insight_type: str  # 'improvement', 'warning', 'recommendation'
    title: str
    description: str
    
    # Supporting data
    evidence: List[str] = field(default_factory=list)
    confidence: float = 0.0
    impact_level: str = 'medium'  # 'low', 'medium', 'high'
    
    # Actionable recommendations
    recommendations: List[str] = field(default_factory=list)
    priority: int = 5  # 1-10 scale


class LearningEngine:
    """
    Learns from healing results to improve future performance.
    
    Features:
    - Pattern recognition for error-solution mappings
    - Success/failure analysis and learning
    - Predictive insights for proactive healing
    - Continuous improvement of solution effectiveness
    - Knowledge base evolution
    """
    
    def __init__(self):
        """Initialize the Learning Engine."""
        self.logger = get_logger('self_healer.learning_engine')
        
        # Data storage
        self.project_root = Path(__file__).parent.parent.parent
        self.learning_data_dir = self.project_root / "Self-Healer" / "learning_data"
        self.learning_data_dir.mkdir(parents=True, exist_ok=True)
        
        # Learning records and patterns
        self.learning_records: List[LearningRecord] = []
        self.patterns: Dict[str, Pattern] = {}
        self.insights: List[LearningInsight] = []
        
        # Learning configuration
        self.learning_config = {
            'min_pattern_occurrences': 3,
            'min_confidence_threshold': 0.6,
            'max_records_in_memory': 1000,
            'pattern_analysis_interval': 3600,  # 1 hour
            'insight_generation_interval': 86400,  # 24 hours
        }
        
        # State
        self.is_running = False
        self.analysis_task: Optional[asyncio.Task] = None
        
        # Load existing data
        self._load_learning_data()
        
        self.logger.info("Learning Engine initialized")
    
    async def start(self):
        """Start the learning engine."""
        if self.is_running:
            self.logger.warning("Learning Engine is already running")
            return
        
        self.is_running = True
        
        # Start periodic analysis
        self.analysis_task = asyncio.create_task(self._periodic_analysis())
        
        self.logger.info("Learning Engine started successfully")
    
    async def stop(self):
        """Stop the learning engine."""
        if not self.is_running:
            return
        
        self.is_running = False
        
        # Stop analysis task
        if self.analysis_task:
            self.analysis_task.cancel()
            try:
                await self.analysis_task
            except asyncio.CancelledError:
                pass
        
        # Save learning data
        self._save_learning_data()
        
        self.logger.info("Learning Engine stopped")
    
    async def record_healing_result(self, error_detail: ErrorDetail, context: Dict[str, Any], 
                                  solution: Dict[str, Any], implementation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Record the result of a healing attempt for learning.
        
        Args:
            error_detail: The original error
            context: Context information
            solution: The solution that was applied
            implementation_result: Result of the implementation
            
        Returns:
            Learning feedback dictionary
        """
        try:
            record_id = f"learn_{int(datetime.now().timestamp() * 1000)}"
            
            # Extract error keywords
            error_keywords = self._extract_keywords_from_error(error_detail)
            
            # Create learning record
            record = LearningRecord(
                record_id=record_id,
                timestamp=datetime.now(),
                error_category=context.get('error_category', 'unknown'),
                error_severity=context.get('error_severity', 'unknown'),
                error_keywords=error_keywords,
                solution_type=solution.get('type', 'unknown'),
                solution_confidence=solution.get('confidence', 0.0),
                solution_steps=[step.get('action', '') for step in solution.get('steps', [])],
                affected_components=context.get('affected_components', []),
                system_state=context.get('system_state', {}),
                success=implementation_result.get('success', False),
                implementation_time=implementation_result.get('duration_seconds', 0.0),
                verification_results=implementation_result.get('verification_results', {})
            )
            
            # Calculate effectiveness score
            record.effectiveness_score = self._calculate_effectiveness_score(record)
            
            # Identify pattern matches
            record.pattern_matches = self._identify_pattern_matches(record)
            
            # Add to records
            self.learning_records.append(record)
            
            # Trigger immediate pattern analysis if significant result
            if record.success or record.effectiveness_score > 0.8:
                await self._analyze_patterns()
            
            # Manage memory usage
            if len(self.learning_records) > self.learning_config['max_records_in_memory']:
                self._archive_old_records()
            
            self.logger.info(f"Recorded healing result: {record_id} - Success: {record.success}")
            
            # Return learning feedback
            feedback = {
                'record_id': record_id,
                'effectiveness_score': record.effectiveness_score,
                'pattern_matches': record.pattern_matches,
                'learning_insights': self._get_relevant_insights(record),
                'recommendations': self._generate_immediate_recommendations(record)
            }
            
            return feedback
            
        except Exception as e:
            self.logger.error(f"Error recording healing result: {e}")
            return {
                'record_id': 'error',
                'error': str(e),
                'effectiveness_score': 0.0
            }
    
    def _extract_keywords_from_error(self, error_detail: ErrorDetail) -> List[str]:
        """Extract relevant keywords from error information."""
        keywords = set()
        
        # Extract from error message and technical details
        text_sources = [
            error_detail.message,
            error_detail.technical_details or "",
            error_detail.title
        ]
        
        for text in text_sources:
            if text:
                # Simple keyword extraction
                words = text.lower().split()
                # Filter for meaningful words (length > 3, not common words)
                meaningful_words = [
                    word for word in words 
                    if len(word) > 3 and word not in ['this', 'that', 'with', 'from', 'they', 'have', 'been']
                ]
                keywords.update(meaningful_words[:10])  # Limit to 10 keywords per source
        
        return list(keywords)[:20]  # Total limit of 20 keywords
    
    def _calculate_effectiveness_score(self, record: LearningRecord) -> float:
        """Calculate effectiveness score for a healing attempt."""
        score = 0.0
        
        # Base score from success
        if record.success:
            score += 0.5
        
        # Bonus for high solution confidence
        score += record.solution_confidence * 0.2
        
        # Bonus for fast implementation
        if record.implementation_time > 0:
            if record.implementation_time <= 60:  # 1 minute
                score += 0.2
            elif record.implementation_time <= 300:  # 5 minutes
                score += 0.1
        
        # Bonus for verification success
        verification_success_rate = sum(
            1 for result in record.verification_results.values() 
            if result is True
        ) / max(1, len(record.verification_results))
        score += verification_success_rate * 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _identify_pattern_matches(self, record: LearningRecord) -> List[str]:
        """Identify which existing patterns match this record."""
        matches = []
        
        for pattern_id, pattern in self.patterns.items():
            if self._record_matches_pattern(record, pattern):
                matches.append(pattern_id)
        
        return matches
    
    def _record_matches_pattern(self, record: LearningRecord, pattern: Pattern) -> bool:
        """Check if a record matches a pattern."""
        try:
            conditions = pattern.conditions
            
            # Check error category match
            if 'error_category' in conditions:
                if record.error_category != conditions['error_category']:
                    return False
            
            # Check solution type match
            if 'solution_type' in conditions:
                if record.solution_type != conditions['solution_type']:
                    return False
            
            # Check keyword overlap
            if 'keywords' in conditions:
                pattern_keywords = set(conditions['keywords'])
                record_keywords = set(record.error_keywords)
                overlap = len(pattern_keywords.intersection(record_keywords))
                required_overlap = conditions.get('min_keyword_overlap', 1)
                if overlap < required_overlap:
                    return False
            
            # Check component overlap
            if 'components' in conditions:
                pattern_components = set(conditions['components'])
                record_components = set(record.affected_components)
                if not pattern_components.intersection(record_components):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error matching pattern: {e}")
            return False
    
    async def _periodic_analysis(self):
        """Periodic analysis of learning data."""
        while self.is_running:
            try:
                # Pattern analysis
                await self._analyze_patterns()
                await asyncio.sleep(self.learning_config['pattern_analysis_interval'])
                
                # Insight generation (less frequent)
                await self._generate_insights()
                await asyncio.sleep(self.learning_config['insight_generation_interval'])
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Error in periodic analysis: {e}")
                await asyncio.sleep(60)  # Wait before retrying
    
    async def _analyze_patterns(self):
        """Analyze learning records to identify and update patterns."""
        try:
            # Group records by error category and solution type
            category_solution_groups = defaultdict(list)
            
            for record in self.learning_records:
                key = (record.error_category, record.solution_type)
                category_solution_groups[key].append(record)
            
            # Analyze each group for patterns
            for (error_category, solution_type), records in category_solution_groups.items():
                if len(records) >= self.learning_config['min_pattern_occurrences']:
                    await self._analyze_group_patterns(error_category, solution_type, records)
            
            self.logger.debug(f"Pattern analysis completed. Total patterns: {len(self.patterns)}")
            
        except Exception as e:
            self.logger.error(f"Error analyzing patterns: {e}")
    
    async def _analyze_group_patterns(self, error_category: str, solution_type: str, records: List[LearningRecord]):
        """Analyze a group of records for patterns."""
        try:
            # Calculate success rate
            success_count = sum(1 for record in records if record.success)
            success_rate = success_count / len(records)
            
            # Find common keywords
            all_keywords = []
            for record in records:
                all_keywords.extend(record.error_keywords)
            
            keyword_counts = Counter(all_keywords)
            common_keywords = [kw for kw, count in keyword_counts.most_common(5) if count >= 2]
            
            # Find common components
            all_components = []
            for record in records:
                all_components.extend(record.affected_components)
            
            component_counts = Counter(all_components)
            common_components = [comp for comp, count in component_counts.most_common(3) if count >= 2]
            
            # Create or update pattern
            pattern_id = f"pattern_{error_category}_{solution_type}"
            
            if pattern_id in self.patterns:
                # Update existing pattern
                pattern = self.patterns[pattern_id]
                pattern.occurrence_count = len(records)
                pattern.success_count = success_count
                pattern.failure_count = len(records) - success_count
                pattern.average_effectiveness = sum(r.effectiveness_score for r in records) / len(records)
                pattern.last_seen = max(r.timestamp for r in records)
                pattern.confidence = success_rate
            else:
                # Create new pattern
                pattern = Pattern(
                    pattern_id=pattern_id,
                    pattern_type='error_solution_pattern',
                    conditions={
                        'error_category': error_category,
                        'solution_type': solution_type,
                        'keywords': common_keywords,
                        'components': common_components,
                        'min_keyword_overlap': max(1, len(common_keywords) // 2)
                    },
                    occurrence_count=len(records),
                    success_count=success_count,
                    failure_count=len(records) - success_count,
                    average_effectiveness=sum(r.effectiveness_score for r in records) / len(records),
                    first_seen=min(r.timestamp for r in records),
                    last_seen=max(r.timestamp for r in records),
                    confidence=success_rate
                )
                
                self.patterns[pattern_id] = pattern
            
        except Exception as e:
            self.logger.error(f"Error analyzing group patterns: {e}")
    
    async def _generate_insights(self):
        """Generate learning insights from patterns and records."""
        try:
            new_insights = []
            
            # Analyze high-performing patterns
            high_performing_patterns = [
                p for p in self.patterns.values() 
                if p.confidence >= 0.8 and p.occurrence_count >= 5
            ]
            
            if high_performing_patterns:
                insight = LearningInsight(
                    insight_id=f"insight_high_performance_{int(datetime.now().timestamp())}",
                    insight_type='improvement',
                    title='High-Performing Solution Patterns Identified',
                    description=f'Found {len(high_performing_patterns)} solution patterns with >80% success rate',
                    evidence=[f"Pattern {p.pattern_id}: {p.confidence:.2%} success rate" for p in high_performing_patterns[:5]],
                    confidence=0.9,
                    impact_level='high',
                    recommendations=[
                        'Prioritize these solution patterns for similar errors',
                        'Consider automating these high-confidence solutions',
                        'Use these patterns as templates for new solutions'
                    ],
                    priority=8
                )
                new_insights.append(insight)
            
            # Analyze low-performing patterns
            low_performing_patterns = [
                p for p in self.patterns.values() 
                if p.confidence <= 0.3 and p.occurrence_count >= 3
            ]
            
            if low_performing_patterns:
                insight = LearningInsight(
                    insight_id=f"insight_low_performance_{int(datetime.now().timestamp())}",
                    insight_type='warning',
                    title='Low-Performing Solution Patterns Detected',
                    description=f'Found {len(low_performing_patterns)} solution patterns with <30% success rate',
                    evidence=[f"Pattern {p.pattern_id}: {p.confidence:.2%} success rate" for p in low_performing_patterns[:5]],
                    confidence=0.8,
                    impact_level='medium',
                    recommendations=[
                        'Review and improve these solution approaches',
                        'Consider alternative solutions for these error types',
                        'Add additional validation for these patterns'
                    ],
                    priority=6
                )
                new_insights.append(insight)
            
            # Add new insights
            self.insights.extend(new_insights)
            
            # Keep only recent insights (last 30 days)
            cutoff_date = datetime.now() - timedelta(days=30)
            self.insights = [
                insight for insight in self.insights 
                if hasattr(insight, 'timestamp') and insight.timestamp > cutoff_date
            ]
            
            if new_insights:
                self.logger.info(f"Generated {len(new_insights)} new learning insights")
            
        except Exception as e:
            self.logger.error(f"Error generating insights: {e}")
    
    def _get_relevant_insights(self, record: LearningRecord) -> List[Dict[str, Any]]:
        """Get insights relevant to a specific record."""
        relevant_insights = []
        
        for insight in self.insights:
            # Simple relevance check based on keywords and categories
            if (record.error_category in insight.description or 
                record.solution_type in insight.description or
                any(keyword in insight.description for keyword in record.error_keywords[:5])):
                
                relevant_insights.append({
                    'insight_id': insight.insight_id,
                    'type': insight.insight_type,
                    'title': insight.title,
                    'impact_level': insight.impact_level,
                    'priority': insight.priority
                })
        
        return relevant_insights[:3]  # Return top 3 relevant insights
    
    def _generate_immediate_recommendations(self, record: LearningRecord) -> List[str]:
        """Generate immediate recommendations based on a record."""
        recommendations = []
        
        # Recommendations based on success/failure
        if record.success:
            recommendations.append('Consider this solution approach for similar errors')
            if record.effectiveness_score > 0.8:
                recommendations.append('High effectiveness - candidate for automation')
        else:
            recommendations.append('Review solution approach for potential improvements')
            if record.solution_confidence < 0.5:
                recommendations.append('Low confidence solution - consider alternative approaches')
        
        # Recommendations based on implementation time
        if record.implementation_time > 300:  # 5 minutes
            recommendations.append('Consider optimizing implementation steps for faster resolution')
        
        return recommendations
    
    def _archive_old_records(self):
        """Archive old learning records to manage memory usage."""
        try:
            # Keep most recent records in memory
            max_records = self.learning_config['max_records_in_memory']
            if len(self.learning_records) > max_records:
                # Sort by timestamp and keep most recent
                self.learning_records.sort(key=lambda r: r.timestamp, reverse=True)
                
                # Archive older records
                records_to_archive = self.learning_records[max_records:]
                self.learning_records = self.learning_records[:max_records]
                
                # Save archived records to disk
                archive_file = self.learning_data_dir / f"archived_records_{int(datetime.now().timestamp())}.pkl"
                with open(archive_file, 'wb') as f:
                    pickle.dump(records_to_archive, f)
                
                self.logger.info(f"Archived {len(records_to_archive)} old learning records")
        
        except Exception as e:
            self.logger.error(f"Error archiving records: {e}")
    
    def _load_learning_data(self):
        """Load existing learning data from disk."""
        try:
            # Load patterns
            patterns_file = self.learning_data_dir / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file, 'r') as f:
                    patterns_data = json.load(f)
                    # Convert back to Pattern objects (simplified)
                    for pattern_id, pattern_dict in patterns_data.items():
                        # This would need proper deserialization
                        pass
            
            # Load recent records
            records_file = self.learning_data_dir / "recent_records.pkl"
            if records_file.exists():
                with open(records_file, 'rb') as f:
                    self.learning_records = pickle.load(f)
            
            self.logger.info(f"Loaded learning data: {len(self.patterns)} patterns, {len(self.learning_records)} records")
            
        except Exception as e:
            self.logger.error(f"Error loading learning data: {e}")
    
    def _save_learning_data(self):
        """Save learning data to disk."""
        try:
            # Save patterns (simplified)
            patterns_file = self.learning_data_dir / "patterns.json"
            # This would need proper serialization
            
            # Save recent records
            records_file = self.learning_data_dir / "recent_records.pkl"
            with open(records_file, 'wb') as f:
                pickle.dump(self.learning_records, f)
            
            self.logger.info("Learning data saved successfully")
            
        except Exception as e:
            self.logger.error(f"Error saving learning data: {e}")
    
    def get_learning_statistics(self) -> Dict[str, Any]:
        """Get learning system statistics."""
        try:
            total_records = len(self.learning_records)
            successful_records = sum(1 for r in self.learning_records if r.success)
            success_rate = successful_records / total_records if total_records > 0 else 0
            
            avg_effectiveness = (
                sum(r.effectiveness_score for r in self.learning_records) / total_records
                if total_records > 0 else 0
            )
            
            return {
                'total_learning_records': total_records,
                'successful_healings': successful_records,
                'overall_success_rate': success_rate,
                'average_effectiveness_score': avg_effectiveness,
                'total_patterns': len(self.patterns),
                'high_confidence_patterns': len([p for p in self.patterns.values() if p.confidence >= 0.8]),
                'total_insights': len(self.insights),
                'recent_insights': len([i for i in self.insights if hasattr(i, 'timestamp')]),
            }
            
        except Exception as e:
            self.logger.error(f"Error getting learning statistics: {e}")
            return {'error': str(e)}
