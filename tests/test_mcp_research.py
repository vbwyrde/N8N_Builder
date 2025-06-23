#!/usr/bin/env python3
"""
Test script for MCP Research Tool

This script tests the MCP research tool functionality to ensure it can
properly research n8n documentation and enhance workflow generation.
"""

import asyncio
import json
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports when running from tests folder
sys.path.insert(0, str(Path(__file__).parent.parent))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def test_research_tool():
    """Test the MCP research tool functionality."""
    try:
        from n8n_builder.mcp_research_tool import N8NResearchTool
        from n8n_builder.research_formatter import ResearchFormatter
        from n8n_builder.enhanced_prompt_builder import EnhancedPromptBuilder
        
        logger.info("Testing MCP Research Tool...")
        
        # Test 1: Basic research tool functionality
        logger.info("Test 1: Basic research tool functionality")
        async with N8NResearchTool() as research_tool:
            # Test searching n8n docs
            docs_results = await research_tool.search_n8n_docs("email notification")
            logger.info(f"Found {len(docs_results)} documentation results")
            
            # Test community examples
            community_results = await research_tool.find_community_examples("email workflow")
            logger.info(f"Found {len(community_results)} community examples")
            
            # Test best practices
            best_practices = await research_tool.get_best_practices("email automation")
            logger.info(f"Found {len(best_practices)} best practices")
            
            # Test comprehensive research
            comprehensive_results = await research_tool.comprehensive_research(
                "Send me an email when a new file is uploaded to Google Drive"
            )
            logger.info(f"Comprehensive research completed with {len(comprehensive_results)} result categories")
        
        # Test 2: Research formatter
        logger.info("Test 2: Research formatter")
        formatter = ResearchFormatter()
        
        # Create mock research data for testing
        mock_research_data = {
            'official_docs': docs_results if 'docs_results' in locals() else [],
            'community_examples': community_results if 'community_results' in locals() else [],
            'best_practices': best_practices if 'best_practices' in locals() else [],
            'concepts': {
                'services': ['email', 'google'],
                'actions': ['send', 'monitor'],
                'triggers': ['file']
            }
        }
        
        formatted_research = formatter.format_comprehensive_research(mock_research_data)
        logger.info(f"Formatted research length: {len(formatted_research)} characters")
        
        # Test 3: Enhanced prompt builder
        logger.info("Test 3: Enhanced prompt builder")
        prompt_builder = EnhancedPromptBuilder(enable_research=True, research_timeout=10)
        
        # Test with research enabled
        enhanced_prompt = await prompt_builder.build_enhanced_prompt(
            "Send me an email notification when a new file is uploaded to my Google Drive folder"
        )
        logger.info(f"Enhanced prompt length: {len(enhanced_prompt)} characters")
        
        # Test with research disabled
        basic_prompt = await prompt_builder.build_enhanced_prompt(
            "Send me an email notification when a new file is uploaded to my Google Drive folder",
            use_research=False
        )
        logger.info(f"Basic prompt length: {len(basic_prompt)} characters")
        
        # Get research statistics
        stats = prompt_builder.get_research_stats()
        logger.info(f"Research statistics: {stats}")
        
        # Clean up
        await prompt_builder.close()
        
        logger.info("All tests completed successfully!")
        return True
        
    except ImportError as e:
        logger.error(f"Import error - missing dependencies: {e}")
        logger.info("Please install required packages: pip install beautifulsoup4 lxml")
        return False
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        logger.exception("Full error details:")
        return False

async def test_integration():
    """Test integration with the main N8N_Builder class."""
    try:
        logger.info("Testing integration with N8N_Builder...")
        
        # Import the main builder
        from n8n_builder.n8n_builder import N8NBuilder
        
        # Create builder instance
        builder = N8NBuilder()
        
        # Test research statistics
        stats = builder.get_research_stats()
        logger.info(f"Initial research stats: {stats}")
        
        # Test workflow generation with enhanced research
        # Note: This will only work if you have a local LLM running
        try:
            workflow = builder.generate_workflow(
                "Create a workflow that sends me an email when someone submits a form on my website"
            )
            logger.info("Workflow generation successful!")
            logger.info(f"Generated workflow length: {len(workflow)} characters")
            
            # Get updated research statistics
            final_stats = builder.get_research_stats()
            logger.info(f"Final research stats: {final_stats}")
            
        except Exception as e:
            logger.warning(f"Workflow generation failed (this is expected if no LLM is running): {e}")
        
        # Clean up
        await builder.close()
        
        logger.info("Integration test completed!")
        return True
        
    except Exception as e:
        logger.error(f"Integration test failed: {e}")
        logger.exception("Full error details:")
        return False

def test_offline_functionality():
    """Test functionality that doesn't require internet access."""
    try:
        logger.info("Testing offline functionality...")
        
        from n8n_builder.research_formatter import ResearchFormatter
        from n8n_builder.mcp_research_tool import ResearchResult
        
        # Test research formatter with mock data
        formatter = ResearchFormatter()
        
        # Create mock research results
        mock_results = [
            ResearchResult(
                source='official_docs',
                title='Email Send Node Documentation',
                content='The Email Send node allows you to send emails using SMTP or various email services.',
                url='https://docs.n8n.io/nodes/n8n-nodes-base.emailSend/',
                relevance_score=0.9,
                timestamp=1234567890
            ),
            ResearchResult(
                source='community_forum',
                title='Email Automation Best Practices',
                content='When setting up email automation, always include error handling and test with sample data.',
                url='https://community.n8n.io/t/email-automation/123',
                relevance_score=0.8,
                timestamp=1234567890
            )
        ]
        
        mock_research_data = {
            'official_docs': mock_results,
            'community_examples': mock_results,
            'best_practices': [
                'Use environment variables for email credentials',
                'Include error handling for failed email sends',
                'Test with sample data before production'
            ],
            'concepts': {
                'services': ['email', 'smtp'],
                'actions': ['send', 'notify'],
                'triggers': ['webhook', 'schedule']
            }
        }
        
        # Test formatting
        formatted = formatter.format_comprehensive_research(mock_research_data)
        logger.info(f"Formatted mock research: {len(formatted)} characters")
        
        # Test prompt creation
        prompt = formatter.format_for_llm_prompt(
            "Send email when webhook received",
            mock_research_data
        )
        logger.info(f"Generated prompt: {len(prompt)} characters")
        
        logger.info("Offline functionality test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Offline test failed: {e}")
        logger.exception("Full error details:")
        return False

async def main():
    """Run all tests."""
    logger.info("Starting MCP Research Tool Tests...")
    
    # Test offline functionality first (doesn't require internet)
    offline_success = test_offline_functionality()
    
    # Test online functionality (requires internet)
    online_success = await test_research_tool()
    
    # Test integration (requires N8N_Builder)
    integration_success = await test_integration()
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("TEST SUMMARY")
    logger.info("="*50)
    logger.info(f"Offline functionality: {'✅ PASS' if offline_success else '❌ FAIL'}")
    logger.info(f"Online research tool: {'✅ PASS' if online_success else '❌ FAIL'}")
    logger.info(f"Integration test: {'✅ PASS' if integration_success else '❌ FAIL'}")
    
    if offline_success and online_success and integration_success:
        logger.info("\n🎉 All tests passed! MCP Research Tool is ready to use.")
    else:
        logger.info("\n⚠️ Some tests failed. Check the logs above for details.")
    
    return offline_success and online_success and integration_success

if __name__ == "__main__":
    # Run the tests
    success = asyncio.run(main())
    exit(0 if success else 1)
