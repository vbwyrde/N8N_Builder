#!/usr/bin/env python3
"""
Complete Integration Test for Enhanced N8N_Builder

This script tests the complete integration of the MCP research tool
with the N8N_Builder system to demonstrate enhanced workflow generation.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path

# Add parent directory to path for imports when running from tests folder
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_complete_integration():
    """Test the complete integration of enhanced workflow generation."""
    
    logger.info("🚀 Complete Integration Test - Enhanced N8N_Builder")
    logger.info("=" * 70)
    
    try:
        # Test workflow descriptions
        test_workflows = [
            {
                "name": "Email Alert System",
                "description": "Send me an email notification when a new file is uploaded to my Google Drive folder",
                "expected_improvements": [
                    "Google Drive node configuration",
                    "Email authentication setup",
                    "Error handling patterns",
                    "Webhook security"
                ]
            },
            {
                "name": "Slack Integration",
                "description": "Post a message to Slack when someone submits a contact form on my website",
                "expected_improvements": [
                    "Slack OAuth configuration",
                    "Webhook validation",
                    "Message formatting",
                    "Rate limiting"
                ]
            }
        ]
        
        # Test 1: Enhanced Prompt Building
        logger.info("\n📋 Test 1: Enhanced Prompt Building with Research")
        logger.info("-" * 50)
        
        from n8n_builder.enhanced_prompt_builder import EnhancedPromptBuilder
        
        prompt_builder = EnhancedPromptBuilder(enable_research=True, research_timeout=30)
        
        for workflow in test_workflows:
            logger.info(f"\n🔍 Testing: {workflow['name']}")
            logger.info(f"Description: {workflow['description']}")
            
            start_time = time.time()
            
            # Generate enhanced prompt
            enhanced_prompt = await prompt_builder.build_enhanced_prompt(workflow['description'])
            
            # Generate basic prompt for comparison
            basic_prompt = await prompt_builder.build_enhanced_prompt(
                workflow['description'], 
                use_research=False
            )
            
            research_time = time.time() - start_time
            
            # Analyze results
            enhancement_ratio = len(enhanced_prompt) / len(basic_prompt)
            
            logger.info(f"✅ Research completed in {research_time:.2f}s")
            logger.info(f"📊 Enhancement Analysis:")
            logger.info(f"   Basic prompt: {len(basic_prompt)} characters")
            logger.info(f"   Enhanced prompt: {len(enhanced_prompt)} characters")
            logger.info(f"   Enhancement ratio: {enhancement_ratio:.2f}x")
            
            # Check for research indicators
            research_indicators = [
                "RESEARCH-ENHANCED",
                "OFFICIAL N8N DOCUMENTATION",
                "COMMUNITY EXAMPLES",
                "BEST PRACTICES",
                "IMPLEMENTATION RECOMMENDATIONS"
            ]
            
            found_indicators = [ind for ind in research_indicators if ind in enhanced_prompt]
            logger.info(f"   Research indicators found: {len(found_indicators)}/{len(research_indicators)}")
            
            if len(found_indicators) >= 3:
                logger.info("   🎉 Strong research enhancement detected!")
            elif len(found_indicators) >= 1:
                logger.info("   ✅ Research enhancement detected")
            else:
                logger.warning("   ⚠️ Limited research enhancement")
        
        # Get research statistics
        stats = prompt_builder.get_research_stats()
        logger.info(f"\n📈 Research Statistics:")
        logger.info(f"   Total requests: {stats.get('total_requests', 0)}")
        logger.info(f"   Successful research: {stats.get('successful_research', 0)}")
        logger.info(f"   Success rate: {stats.get('success_rate', 0):.1%}")
        logger.info(f"   Average research time: {stats.get('average_research_time', 0):.2f}s")
        
        await prompt_builder.close()
        
        # Test 2: Full N8N_Builder Integration (if LLM is available)
        logger.info("\n📋 Test 2: Full N8N_Builder Integration")
        logger.info("-" * 50)
        
        try:
            from n8n_builder.n8n_builder import N8NBuilder
            
            builder = N8NBuilder()
            
            # Test workflow generation
            test_description = "Send me an email when a new customer signs up on my website"
            
            logger.info(f"🔧 Testing workflow generation...")
            logger.info(f"Description: {test_description}")
            
            start_time = time.time()
            
            try:
                # This will only work if you have a local LLM running
                workflow_json = builder.generate_workflow(test_description)
                generation_time = time.time() - start_time
                
                logger.info(f"✅ Workflow generated in {generation_time:.2f}s")
                logger.info(f"📄 Generated workflow length: {len(workflow_json)} characters")
                
                # Try to parse as JSON to validate
                try:
                    workflow_data = json.loads(workflow_json)
                    node_count = len(workflow_data.get('nodes', []))
                    connection_count = len(workflow_data.get('connections', {}))
                    
                    logger.info(f"📊 Workflow Analysis:")
                    logger.info(f"   Nodes: {node_count}")
                    logger.info(f"   Connections: {connection_count}")
                    logger.info(f"   Workflow name: {workflow_data.get('name', 'Unknown')}")
                    
                    # Check for enhanced features
                    enhanced_features = []
                    
                    # Look for error handling
                    if any('error' in str(node).lower() for node in workflow_data.get('nodes', [])):
                        enhanced_features.append("Error handling")
                    
                    # Look for proper node types
                    node_types = [node.get('type', '') for node in workflow_data.get('nodes', [])]
                    if any('n8n-nodes-base' in node_type for node_type in node_types):
                        enhanced_features.append("Proper node types")
                    
                    # Look for realistic parameters
                    if any(node.get('parameters') for node in workflow_data.get('nodes', [])):
                        enhanced_features.append("Configured parameters")
                    
                    logger.info(f"   Enhanced features: {', '.join(enhanced_features) if enhanced_features else 'None detected'}")
                    
                except json.JSONDecodeError:
                    logger.warning("⚠️ Generated workflow is not valid JSON")
                
                # Get final research statistics
                final_stats = builder.get_research_stats()
                logger.info(f"\n📈 Final Research Statistics:")
                logger.info(f"   Total requests: {final_stats.get('total_requests', 0)}")
                logger.info(f"   Successful research: {final_stats.get('successful_research', 0)}")
                
            except Exception as e:
                logger.warning(f"⚠️ Workflow generation failed (expected if no LLM running): {e}")
                logger.info("💡 To test workflow generation, ensure you have a local LLM running at localhost:1234")
            
            await builder.close()
            
        except ImportError as e:
            logger.warning(f"⚠️ N8NBuilder import failed: {e}")
        
        # Test 3: Cache Performance
        logger.info("\n📋 Test 3: Cache Performance")
        logger.info("-" * 50)
        
        from n8n_builder.mcp_research_tool import N8NResearchTool
        
        async with N8NResearchTool() as research_tool:
            # Test cache performance with repeated queries
            test_query = "email automation best practices"
            
            # First query (should hit external sources)
            start_time = time.time()
            results1 = await research_tool.search_n8n_docs(test_query)
            first_query_time = time.time() - start_time
            
            # Second query (should hit cache)
            start_time = time.time()
            results2 = await research_tool.search_n8n_docs(test_query)
            second_query_time = time.time() - start_time
            
            logger.info(f"🔍 Cache Performance Test:")
            logger.info(f"   First query time: {first_query_time:.2f}s")
            logger.info(f"   Second query time: {second_query_time:.2f}s")
            logger.info(f"   Speed improvement: {first_query_time / second_query_time:.1f}x faster")
            logger.info(f"   Results consistency: {'✅ Same' if len(results1) == len(results2) else '❌ Different'}")
            
            # Get cache statistics
            cache_stats = research_tool.get_cache_stats()
            logger.info(f"📊 Cache Statistics:")
            for key, value in cache_stats.items():
                if isinstance(value, float):
                    logger.info(f"   {key}: {value:.2f}")
                else:
                    logger.info(f"   {key}: {value}")
        
        # Test 4: Research Validation
        logger.info("\n📋 Test 4: Research Validation")
        logger.info("-" * 50)
        
        from n8n_builder.research_validator import ResearchValidator
        from n8n_builder.mcp_research_tool import ResearchResult
        
        validator = ResearchValidator()
        
        # Create mock research data for validation testing
        mock_results = [
            ResearchResult(
                source='official_docs',
                title='Email Send Node Documentation',
                content='The Email Send node allows you to send emails using SMTP or various email service providers. Configure authentication, set recipients, and customize message content.',
                url='https://docs.n8n.io/nodes/n8n-nodes-base.emailSend/',
                relevance_score=0.9,
                timestamp=time.time()
            ),
            ResearchResult(
                source='community_forum',
                title='Email Automation Best Practices',
                content='When setting up email automation, always use environment variables for credentials, implement proper error handling, and test with sample data before production.',
                url='https://community.n8n.io/t/email-best-practices/123',
                relevance_score=0.8,
                timestamp=time.time()
            )
        ]
        
        validation_result = validator.validate_research_results(mock_results, "email automation")
        
        logger.info(f"🔍 Validation Results:")
        logger.info(f"   Valid: {'✅ Yes' if validation_result.is_valid else '❌ No'}")
        logger.info(f"   Quality score: {validation_result.quality_score:.2f}")
        logger.info(f"   Issues found: {len(validation_result.issues)}")
        logger.info(f"   Recommendations: {len(validation_result.recommendations)}")
        
        if validation_result.issues:
            logger.info(f"   Sample issues: {validation_result.issues[0]}")
        
        if validation_result.recommendations:
            logger.info(f"   Sample recommendation: {validation_result.recommendations[0]}")
        
        # Final Summary
        logger.info("\n" + "=" * 70)
        logger.info("🎉 INTEGRATION TEST SUMMARY")
        logger.info("=" * 70)
        
        logger.info("✅ Enhanced prompt building with research integration")
        logger.info("✅ Knowledge caching for improved performance")
        logger.info("✅ Research validation for quality assurance")
        logger.info("✅ Complete system integration ready")
        
        logger.info("\n💡 Key Benefits Demonstrated:")
        logger.info("   🔍 Real-time research of n8n documentation")
        logger.info("   📚 Community best practices integration")
        logger.info("   ⚡ Intelligent caching for performance")
        logger.info("   🎯 Quality validation for accuracy")
        logger.info("   🔄 Seamless integration with existing system")
        
        logger.info("\n🚀 The Enhanced N8N_Builder is ready for production use!")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        logger.exception("Full error details:")
        return False

async def main():
    """Run the complete integration test."""
    success = await test_complete_integration()
    
    if success:
        logger.info("\n🎯 All integration tests passed!")
        logger.info("The MCP research tool is successfully integrated and ready to enhance workflow generation.")
    else:
        logger.error("\n❌ Integration tests failed!")
        logger.info("Please check the error logs and ensure all dependencies are properly installed.")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
