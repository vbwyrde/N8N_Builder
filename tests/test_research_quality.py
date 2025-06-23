#!/usr/bin/env python3
"""
Research Quality Testing and Optimization

This script tests the MCP research tool with various workflow types
and optimizes for accuracy and relevance.
"""

import asyncio
import json
import logging
import sys
import time
from typing import Dict, List, Any
from pathlib import Path

# Add parent directory to path for imports when running from tests folder
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test cases for different workflow types
TEST_WORKFLOWS = [
    {
        "name": "Email Notification",
        "description": "Send me an email when a new file is uploaded to Google Drive",
        "expected_services": ["email", "google"],
        "expected_actions": ["send", "monitor"],
        "expected_triggers": ["file"],
        "complexity": "simple"
    },
    {
        "name": "Slack Integration",
        "description": "Post a message to Slack when someone submits a form on my website",
        "expected_services": ["slack", "webhook"],
        "expected_actions": ["send", "create"],
        "expected_triggers": ["webhook"],
        "complexity": "simple"
    },
    {
        "name": "Database Automation",
        "description": "Automatically backup my PostgreSQL database to Google Drive every day at midnight",
        "expected_services": ["database", "google"],
        "expected_actions": ["sync", "create"],
        "expected_triggers": ["schedule"],
        "complexity": "intermediate"
    },
    {
        "name": "Multi-Service Workflow",
        "description": "When a new customer signs up, create a Slack notification, add them to Google Sheets, and send a welcome email",
        "expected_services": ["slack", "google", "email"],
        "expected_actions": ["create", "send"],
        "expected_triggers": ["webhook"],
        "complexity": "complex"
    },
    {
        "name": "Social Media Automation",
        "description": "Monitor Twitter mentions and automatically respond via Discord and update a tracking spreadsheet",
        "expected_services": ["twitter", "discord", "google"],
        "expected_actions": ["monitor", "send", "update"],
        "expected_triggers": ["schedule"],
        "complexity": "complex"
    },
    {
        "name": "E-commerce Integration",
        "description": "When an order is placed on Shopify, send order details to Slack, update inventory in Google Sheets, and trigger fulfillment",
        "expected_services": ["webhook", "slack", "google"],
        "expected_actions": ["send", "update", "create"],
        "expected_triggers": ["webhook"],
        "complexity": "complex"
    }
]

class ResearchQualityTester:
    """Test and optimize research quality for various workflow types."""
    
    def __init__(self):
        self.results = []
        self.performance_metrics = {
            'total_tests': 0,
            'successful_tests': 0,
            'average_research_time': 0.0,
            'average_quality_score': 0.0,
            'concept_detection_accuracy': 0.0
        }
    
    async def run_comprehensive_tests(self):
        """Run comprehensive tests on all workflow types."""
        logger.info("🧪 Starting Research Quality Testing")
        logger.info("=" * 60)
        
        try:
            from n8n_builder.enhanced_prompt_builder import EnhancedPromptBuilder
            from n8n_builder.research_validator import ResearchValidator
            
            # Initialize components
            prompt_builder = EnhancedPromptBuilder(enable_research=True, research_timeout=45)
            validator = ResearchValidator()
            
            total_start_time = time.time()
            
            for i, test_case in enumerate(TEST_WORKFLOWS, 1):
                logger.info(f"\n📋 Test {i}/{len(TEST_WORKFLOWS)}: {test_case['name']}")
                logger.info(f"Description: {test_case['description']}")
                logger.info(f"Complexity: {test_case['complexity']}")
                
                test_result = await self._test_single_workflow(
                    test_case, prompt_builder, validator
                )
                
                self.results.append(test_result)
                self._log_test_result(test_result)
            
            total_time = time.time() - total_start_time
            
            # Calculate performance metrics
            self._calculate_performance_metrics(total_time)
            
            # Generate optimization recommendations
            recommendations = self._generate_optimization_recommendations()
            
            # Display results
            self._display_comprehensive_results(recommendations)
            
            # Clean up
            await prompt_builder.close()
            
        except ImportError as e:
            logger.error(f"❌ Import error: {e}")
            logger.info("💡 Make sure all dependencies are installed")
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            logger.exception("Full error details:")
    
    async def _test_single_workflow(self, test_case: Dict[str, Any], prompt_builder, validator) -> Dict[str, Any]:
        """Test a single workflow type."""
        start_time = time.time()
        
        try:
            # Perform research
            research_data = await prompt_builder._perform_research(test_case['description'])
            research_time = time.time() - start_time
            
            if not research_data:
                return {
                    'test_case': test_case,
                    'success': False,
                    'error': 'No research data returned',
                    'research_time': research_time,
                    'quality_score': 0.0,
                    'concept_accuracy': 0.0
                }
            
            # Validate research quality
            validation_result = validator.validate_comprehensive_research(research_data)
            
            # Test concept detection accuracy
            concept_accuracy = self._test_concept_detection(test_case, research_data)
            
            # Test prompt enhancement
            enhanced_prompt = prompt_builder.formatter.format_for_llm_prompt(
                test_case['description'], research_data
            )
            
            return {
                'test_case': test_case,
                'success': True,
                'research_time': research_time,
                'quality_score': validation_result.quality_score,
                'concept_accuracy': concept_accuracy,
                'validation_result': validation_result,
                'research_data': research_data,
                'enhanced_prompt_length': len(enhanced_prompt),
                'components_found': validation_result.metadata.get('components_found', 0),
                'best_practices_count': validation_result.metadata.get('best_practices_count', 0)
            }
        
        except Exception as e:
            return {
                'test_case': test_case,
                'success': False,
                'error': str(e),
                'research_time': time.time() - start_time,
                'quality_score': 0.0,
                'concept_accuracy': 0.0
            }
    
    def _test_concept_detection(self, test_case: Dict[str, Any], research_data: Dict[str, Any]) -> float:
        """Test accuracy of concept detection."""
        concepts = research_data.get('concepts', {})
        detected_services = set(concepts.get('services', []))
        detected_actions = set(concepts.get('actions', []))
        detected_triggers = set(concepts.get('triggers', []))
        
        expected_services = set(test_case['expected_services'])
        expected_actions = set(test_case['expected_actions'])
        expected_triggers = set(test_case['expected_triggers'])
        
        # Calculate accuracy for each concept type
        service_accuracy = len(detected_services.intersection(expected_services)) / len(expected_services) if expected_services else 1.0
        action_accuracy = len(detected_actions.intersection(expected_actions)) / len(expected_actions) if expected_actions else 1.0
        trigger_accuracy = len(detected_triggers.intersection(expected_triggers)) / len(expected_triggers) if expected_triggers else 1.0
        
        # Overall accuracy (weighted average)
        overall_accuracy = (service_accuracy * 0.5) + (action_accuracy * 0.3) + (trigger_accuracy * 0.2)
        
        return overall_accuracy
    
    def _log_test_result(self, result: Dict[str, Any]):
        """Log the result of a single test."""
        if result['success']:
            logger.info(f"✅ Success - Quality: {result['quality_score']:.2f}, "
                       f"Concept Accuracy: {result['concept_accuracy']:.2f}, "
                       f"Time: {result['research_time']:.2f}s")
            
            if result['quality_score'] < 0.6:
                logger.warning(f"⚠️ Low quality score: {result['quality_score']:.2f}")
            
            if result['concept_accuracy'] < 0.7:
                logger.warning(f"⚠️ Low concept accuracy: {result['concept_accuracy']:.2f}")
        else:
            logger.error(f"❌ Failed - Error: {result['error']}")
    
    def _calculate_performance_metrics(self, total_time: float):
        """Calculate overall performance metrics."""
        successful_results = [r for r in self.results if r['success']]
        
        self.performance_metrics.update({
            'total_tests': len(self.results),
            'successful_tests': len(successful_results),
            'total_time': total_time,
            'success_rate': len(successful_results) / len(self.results) if self.results else 0,
            'average_research_time': sum(r['research_time'] for r in successful_results) / len(successful_results) if successful_results else 0,
            'average_quality_score': sum(r['quality_score'] for r in successful_results) / len(successful_results) if successful_results else 0,
            'concept_detection_accuracy': sum(r['concept_accuracy'] for r in successful_results) / len(successful_results) if successful_results else 0
        })
    
    def _generate_optimization_recommendations(self) -> List[str]:
        """Generate optimization recommendations based on test results."""
        recommendations = []
        metrics = self.performance_metrics
        
        # Performance recommendations
        if metrics['average_research_time'] > 30:
            recommendations.append("🚀 Consider reducing research timeout or optimizing cache usage")
        
        if metrics['success_rate'] < 0.8:
            recommendations.append("🔧 Improve error handling and fallback mechanisms")
        
        # Quality recommendations
        if metrics['average_quality_score'] < 0.7:
            recommendations.append("📚 Enhance research sources or improve content filtering")
        
        if metrics['concept_detection_accuracy'] < 0.8:
            recommendations.append("🎯 Improve concept extraction algorithms")
        
        # Analyze specific issues
        failed_tests = [r for r in self.results if not r['success']]
        if failed_tests:
            recommendations.append(f"🔍 Investigate {len(failed_tests)} failed test cases")
        
        # Complexity-based recommendations
        complex_tests = [r for r in self.results if r['success'] and r['test_case']['complexity'] == 'complex']
        if complex_tests:
            avg_complex_quality = sum(r['quality_score'] for r in complex_tests) / len(complex_tests)
            if avg_complex_quality < 0.6:
                recommendations.append("🧩 Improve handling of complex multi-service workflows")
        
        return recommendations
    
    def _display_comprehensive_results(self, recommendations: List[str]):
        """Display comprehensive test results."""
        logger.info("\n" + "=" * 60)
        logger.info("📊 RESEARCH QUALITY TEST RESULTS")
        logger.info("=" * 60)
        
        metrics = self.performance_metrics
        
        logger.info(f"📈 Overall Performance:")
        logger.info(f"   Total Tests: {metrics['total_tests']}")
        logger.info(f"   Successful Tests: {metrics['successful_tests']}")
        logger.info(f"   Success Rate: {metrics['success_rate']:.1%}")
        logger.info(f"   Total Time: {metrics['total_time']:.2f}s")
        
        logger.info(f"\n⏱️ Research Performance:")
        logger.info(f"   Average Research Time: {metrics['average_research_time']:.2f}s")
        logger.info(f"   Average Quality Score: {metrics['average_quality_score']:.2f}")
        logger.info(f"   Concept Detection Accuracy: {metrics['concept_detection_accuracy']:.1%}")
        
        # Results by complexity
        logger.info(f"\n📋 Results by Complexity:")
        for complexity in ['simple', 'intermediate', 'complex']:
            complexity_results = [r for r in self.results if r['success'] and r['test_case']['complexity'] == complexity]
            if complexity_results:
                avg_quality = sum(r['quality_score'] for r in complexity_results) / len(complexity_results)
                avg_accuracy = sum(r['concept_accuracy'] for r in complexity_results) / len(complexity_results)
                logger.info(f"   {complexity.title()}: {len(complexity_results)} tests, "
                           f"Quality: {avg_quality:.2f}, Accuracy: {avg_accuracy:.1%}")
        
        # Recommendations
        if recommendations:
            logger.info(f"\n💡 Optimization Recommendations:")
            for rec in recommendations:
                logger.info(f"   {rec}")
        
        # Quality assessment
        overall_grade = self._calculate_overall_grade()
        logger.info(f"\n🎯 Overall Grade: {overall_grade}")
        
        logger.info("\n" + "=" * 60)
    
    def _calculate_overall_grade(self) -> str:
        """Calculate overall grade based on performance metrics."""
        metrics = self.performance_metrics
        
        # Weighted score calculation
        score = (
            metrics['success_rate'] * 0.3 +
            metrics['average_quality_score'] * 0.4 +
            metrics['concept_detection_accuracy'] * 0.3
        )
        
        if score >= 0.9:
            return "A+ (Excellent)"
        elif score >= 0.8:
            return "A (Very Good)"
        elif score >= 0.7:
            return "B (Good)"
        elif score >= 0.6:
            return "C (Acceptable)"
        elif score >= 0.5:
            return "D (Needs Improvement)"
        else:
            return "F (Poor)"
    
    def save_results(self, filename: str = "research_quality_results.json"):
        """Save test results to file."""
        results_data = {
            'timestamp': time.time(),
            'performance_metrics': self.performance_metrics,
            'test_results': self.results,
            'recommendations': self._generate_optimization_recommendations()
        }
        
        with open(filename, 'w') as f:
            json.dump(results_data, f, indent=2, default=str)
        
        logger.info(f"📄 Results saved to {filename}")

async def main():
    """Run the research quality tests."""
    tester = ResearchQualityTester()
    
    try:
        await tester.run_comprehensive_tests()
        tester.save_results()
        
        logger.info("\n🎉 Research quality testing completed!")
        logger.info("💡 Use the results to optimize the MCP research tool for better accuracy and performance.")
        
    except Exception as e:
        logger.error(f"❌ Testing failed: {e}")
        logger.exception("Full error details:")

if __name__ == "__main__":
    asyncio.run(main())
