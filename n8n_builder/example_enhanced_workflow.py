#!/usr/bin/env python3
"""
Example: Enhanced Workflow Generation with MCP Research

This script demonstrates how the enhanced N8N_Builder with MCP research
generates more accurate and sophisticated workflows by researching
n8n documentation and best practices in real-time.
"""

import asyncio
import json
import logging
import time
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def demonstrate_enhanced_generation():
    """Demonstrate enhanced workflow generation with research."""
    
    logger.info("🚀 Enhanced N8N Workflow Generation Demo")
    logger.info("=" * 50)
    
    try:
        # Import the enhanced components
        from n8n_builder.enhanced_prompt_builder import EnhancedPromptBuilder
        from n8n_builder.mcp_research_tool import N8NResearchTool
        from n8n_builder.research_formatter import ResearchFormatter
        
        # Example workflow descriptions
        examples = [
            {
                "name": "Email Notification System",
                "description": "Send me an email notification when a new file is uploaded to my Google Drive folder",
                "expected_improvements": [
                    "Proper Google Drive node configuration",
                    "Email authentication best practices",
                    "Error handling for failed uploads",
                    "Webhook security considerations"
                ]
            },
            {
                "name": "Slack Integration",
                "description": "Post a message to Slack when someone submits a form on my website",
                "expected_improvements": [
                    "Slack OAuth setup guidance",
                    "Webhook validation",
                    "Message formatting best practices",
                    "Rate limiting considerations"
                ]
            },
            {
                "name": "Database Automation",
                "description": "Automatically backup my database to Google Drive every day at midnight",
                "expected_improvements": [
                    "Cron schedule configuration",
                    "Database connection security",
                    "File compression options",
                    "Backup verification steps"
                ]
            }
        ]
        
        # Initialize enhanced prompt builder
        prompt_builder = EnhancedPromptBuilder(
            enable_research=True,
            research_timeout=30
        )
        
        logger.info(f"Testing {len(examples)} workflow examples...\n")
        
        for i, example in enumerate(examples, 1):
            logger.info(f"📋 Example {i}: {example['name']}")
            logger.info(f"Description: {example['description']}")
            logger.info(f"Expected improvements: {', '.join(example['expected_improvements'])}")
            
            start_time = time.time()
            
            try:
                # Generate enhanced prompt with research
                logger.info("🔍 Researching n8n documentation and best practices...")
                enhanced_prompt = await prompt_builder.build_enhanced_prompt(example['description'])
                
                research_time = time.time() - start_time
                logger.info(f"✅ Research completed in {research_time:.2f} seconds")
                
                # Show prompt comparison
                basic_prompt = await prompt_builder.build_enhanced_prompt(
                    example['description'], 
                    use_research=False
                )
                
                logger.info(f"📊 Prompt Analysis:")
                logger.info(f"   Basic prompt length: {len(basic_prompt)} characters")
                logger.info(f"   Enhanced prompt length: {len(enhanced_prompt)} characters")
                logger.info(f"   Enhancement ratio: {len(enhanced_prompt) / len(basic_prompt):.2f}x")
                
                # Extract research insights
                if "RESEARCH-ENHANCED" in enhanced_prompt:
                    logger.info("🧠 Research insights found in enhanced prompt:")
                    
                    # Look for specific improvements
                    insights = []
                    if "OFFICIAL N8N DOCUMENTATION" in enhanced_prompt:
                        insights.append("✓ Official documentation referenced")
                    if "COMMUNITY EXAMPLES" in enhanced_prompt:
                        insights.append("✓ Community examples included")
                    if "BEST PRACTICES" in enhanced_prompt:
                        insights.append("✓ Best practices incorporated")
                    if "INTEGRATION PATTERNS" in enhanced_prompt:
                        insights.append("✓ Integration patterns identified")
                    
                    for insight in insights:
                        logger.info(f"   {insight}")
                else:
                    logger.warning("⚠️ No research enhancement detected (may have fallen back to basic prompt)")
                
            except Exception as e:
                logger.error(f"❌ Failed to generate enhanced prompt: {e}")
            
            logger.info("-" * 50)
        
        # Show research statistics
        stats = prompt_builder.get_research_stats()
        logger.info("\n📈 Research Performance Statistics:")
        logger.info(f"   Total requests: {stats.get('total_requests', 0)}")
        logger.info(f"   Successful research: {stats.get('successful_research', 0)}")
        logger.info(f"   Success rate: {stats.get('success_rate', 0):.1%}")
        logger.info(f"   Average research time: {stats.get('average_research_time', 0):.2f}s")
        
        # Clean up
        await prompt_builder.close()
        
        logger.info("\n🎉 Demo completed successfully!")
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.info("💡 Make sure to install dependencies: pip install beautifulsoup4 lxml")
    except Exception as e:
        logger.error(f"❌ Demo failed: {e}")
        logger.exception("Full error details:")

async def demonstrate_research_tool():
    """Demonstrate the research tool capabilities directly."""
    
    logger.info("\n🔬 MCP Research Tool Direct Demo")
    logger.info("=" * 50)
    
    try:
        from n8n_builder.mcp_research_tool import N8NResearchTool
        
        async with N8NResearchTool() as research_tool:
            # Test different research capabilities
            test_queries = [
                ("email automation", "Email workflow research"),
                ("webhook security", "Webhook best practices"),
                ("slack integration", "Slack node documentation"),
                ("database backup", "Database automation patterns")
            ]
            
            for query, description in test_queries:
                logger.info(f"\n🔍 {description}")
                logger.info(f"Query: '{query}'")
                
                try:
                    # Perform comprehensive research
                    results = await research_tool.comprehensive_research(query)
                    
                    # Show results summary
                    logger.info("📊 Research Results:")
                    logger.info(f"   Official docs: {len(results.get('official_docs', []))} results")
                    logger.info(f"   Community examples: {len(results.get('community_examples', []))} results")
                    logger.info(f"   Best practices: {len(results.get('best_practices', []))} items")
                    logger.info(f"   Detected services: {', '.join(results.get('concepts', {}).get('services', []))}")
                    logger.info(f"   Detected actions: {', '.join(results.get('concepts', {}).get('actions', []))}")
                    
                except Exception as e:
                    logger.warning(f"⚠️ Research failed for '{query}': {e}")
        
        logger.info("\n✅ Research tool demo completed!")
        
    except Exception as e:
        logger.error(f"❌ Research tool demo failed: {e}")

def demonstrate_offline_features():
    """Demonstrate features that work without internet access."""
    
    logger.info("\n💻 Offline Features Demo")
    logger.info("=" * 50)
    
    try:
        from n8n_builder.research_formatter import ResearchFormatter
        from n8n_builder.mcp_research_tool import ResearchResult
        
        # Create mock research data
        mock_results = [
            ResearchResult(
                source='official_docs',
                title='Email Send Node',
                content='The Email Send node allows you to send emails using SMTP or email service providers like Gmail, Outlook, etc.',
                url='https://docs.n8n.io/nodes/n8n-nodes-base.emailSend/',
                relevance_score=0.95,
                timestamp=time.time()
            ),
            ResearchResult(
                source='community_forum',
                title='Email Automation Best Practices',
                content='Always use environment variables for credentials, implement error handling, and test with sample data.',
                url='https://community.n8n.io/t/email-best-practices/123',
                relevance_score=0.85,
                timestamp=time.time()
            )
        ]
        
        mock_research_data = {
            'official_docs': mock_results,
            'community_examples': mock_results,
            'best_practices': [
                'Use environment variables for sensitive credentials',
                'Implement proper error handling with error trigger nodes',
                'Test workflows with sample data before production',
                'Add descriptive names to all workflow nodes',
                'Use rate limiting for external API calls'
            ],
            'concepts': {
                'services': ['email', 'gmail', 'smtp'],
                'actions': ['send', 'notify', 'alert'],
                'triggers': ['webhook', 'schedule', 'manual']
            }
        }
        
        # Test research formatter
        formatter = ResearchFormatter()
        
        logger.info("📝 Testing research formatting...")
        formatted = formatter.format_comprehensive_research(mock_research_data)
        logger.info(f"✅ Formatted {len(formatted)} characters of research data")
        
        # Test prompt generation
        prompt = formatter.format_for_llm_prompt(
            "Send email notification when webhook received",
            mock_research_data
        )
        logger.info(f"✅ Generated {len(prompt)} character enhanced prompt")
        
        # Show sample of formatted content
        logger.info("\n📋 Sample formatted research:")
        sample = formatted[:300] + "..." if len(formatted) > 300 else formatted
        logger.info(sample)
        
        logger.info("\n✅ Offline features demo completed!")
        
    except Exception as e:
        logger.error(f"❌ Offline demo failed: {e}")

async def main():
    """Run all demonstrations."""
    
    logger.info("🎯 N8N_Builder Enhanced Workflow Generation Demo")
    logger.info("This demo shows how MCP research improves workflow generation")
    logger.info("=" * 60)
    
    # Run offline demo first (always works)
    demonstrate_offline_features()
    
    # Run online demos (require internet)
    await demonstrate_research_tool()
    await demonstrate_enhanced_generation()
    
    logger.info("\n" + "=" * 60)
    logger.info("🏁 All demonstrations completed!")
    logger.info("\n💡 Key Benefits of Enhanced Workflow Generation:")
    logger.info("   • Real-time research of n8n documentation")
    logger.info("   • Community best practices integration")
    logger.info("   • Accurate node parameters and configurations")
    logger.info("   • Security and error handling recommendations")
    logger.info("   • Up-to-date integration patterns")
    logger.info("\n🚀 Ready to generate better workflows with AI + Research!")

if __name__ == "__main__":
    asyncio.run(main())
