#!/usr/bin/env python3
"""
Self-Healer System Example Usage

This script demonstrates how to use the Self-Healer system for automatic
error detection, analysis, and resolution in the N8N Builder environment.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from Self_Healer.core.healer_manager import SelfHealerManager
from n8n_builder.error_handler import ErrorDetail, ErrorCategory, ErrorSeverity


async def main():
    """Main example function demonstrating Self-Healer usage."""
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger('self_healer_example')
    logger.info("Starting Self-Healer System Example")
    
    # Initialize the Self-Healer Manager
    healer = SelfHealerManager()
    
    try:
        # Start the self-healing system
        logger.info("Starting Self-Healer system...")
        await healer.start()
        
        # Wait a moment for initialization
        await asyncio.sleep(2)
        
        # Example 1: Check system status
        logger.info("=== Example 1: System Status ===")
        status = await healer.get_status()
        print(f"System Status: {status['status']}")
        print(f"Is Running: {status['is_running']}")
        print(f"Active Sessions: {status['active_sessions']}")
        print(f"Total Errors Detected: {status['metrics']['total_errors_detected']}")
        print(f"Success Rate: {status['metrics']['success_rate']:.1f}%")
        print()
        
        # Example 2: Simulate an error for demonstration
        logger.info("=== Example 2: Simulated Error Healing ===")
        
        # Create a mock error detail
        mock_error = ErrorDetail(
            category=ErrorCategory.LLM_COMMUNICATION,
            severity=ErrorSeverity.ERROR,
            title="LLM Connection Failed",
            message="Unable to connect to the AI service for workflow generation",
            user_guidance="The AI service is temporarily unavailable.",
            technical_details="Connection refused: localhost:1234",
            fix_suggestions=[
                "Check if LM Studio is running",
                "Verify the server URL configuration",
                "Try again in a few moments"
            ],
            context={
                'error_id': 'demo_error_001',
                'operation_id': 'demo_operation',
                'endpoint': 'localhost:1234'
            }
        )
        
        # Manually trigger context analysis
        logger.info("Analyzing error context...")
        context = await healer.context_analyzer.analyze_error(mock_error)
        print(f"Context Analysis Complete:")
        print(f"  - Error Category: {context['error_category']}")
        print(f"  - Related Files: {len(context['related_files'])}")
        print(f"  - Relevant Docs: {len(context['relevant_docs'])}")
        print(f"  - Affected Components: {context['affected_components']}")
        print()
        
        # Generate solutions
        logger.info("Generating solutions...")
        solutions = await healer.solution_generator.generate_solutions(mock_error, context)
        print(f"Generated {len(solutions)} solutions:")
        
        for i, solution in enumerate(solutions[:3], 1):  # Show top 3 solutions
            print(f"  Solution {i}:")
            print(f"    - Title: {solution['title']}")
            print(f"    - Type: {solution['type']}")
            print(f"    - Confidence: {solution['confidence']:.2f}")
            print(f"    - Risk Level: {solution['risk_level']}")
            print(f"    - Can be Automated: {solution['can_be_automated']}")
            print(f"    - Steps: {len(solution['steps'])}")
        print()
        
        # Validate the best solution
        if solutions:
            best_solution = solutions[0]
            logger.info("Validating best solution...")
            validation = await healer.solution_validator.validate_solution(best_solution, context)
            
            print(f"Validation Results:")
            print(f"  - Result: {validation['validation_result']}")
            print(f"  - Confidence: {validation['confidence']:.2f}")
            print(f"  - Can Proceed: {validation['can_proceed']}")
            print(f"  - Is Safe: {validation['is_safe']}")
            print(f"  - Risk Factors: {len(validation['risk_factors'])}")
            
            if validation['risk_factors']:
                print(f"  - Risk Factors:")
                for risk in validation['risk_factors'][:3]:
                    print(f"    * {risk}")
            print()
            
            # Note: We won't actually implement the solution in this demo
            # to avoid making changes to the system
            logger.info("Note: Solution implementation skipped in demo mode")
        
        # Example 3: Learning System Statistics
        logger.info("=== Example 3: Learning System Statistics ===")
        learning_stats = healer.learning_engine.get_learning_statistics()
        print(f"Learning System Statistics:")
        print(f"  - Total Learning Records: {learning_stats['total_learning_records']}")
        print(f"  - Successful Healings: {learning_stats['successful_healings']}")
        print(f"  - Overall Success Rate: {learning_stats['overall_success_rate']:.1%}")
        print(f"  - Average Effectiveness: {learning_stats['average_effectiveness_score']:.2f}")
        print(f"  - Total Patterns: {learning_stats['total_patterns']}")
        print(f"  - High Confidence Patterns: {learning_stats['high_confidence_patterns']}")
        print()
        
        # Example 4: Monitor for a short period
        logger.info("=== Example 4: Monitoring Mode ===")
        logger.info("Monitoring for errors for 30 seconds...")
        
        # Monitor for 30 seconds
        for i in range(6):
            await asyncio.sleep(5)
            
            # Check for new errors
            new_errors = await healer.error_monitor.get_new_errors()
            if new_errors:
                logger.info(f"Detected {len(new_errors)} new errors")
                for error in new_errors:
                    print(f"  - {error.title}: {error.message}")
            else:
                logger.info(f"No new errors detected (check {i+1}/6)")
        
        print()
        logger.info("Monitoring period complete")
        
        # Example 5: Final Status Check
        logger.info("=== Example 5: Final Status ===")
        final_status = await healer.get_status()
        print(f"Final System Status:")
        print(f"  - Uptime: {final_status['metrics']['uptime_seconds']:.0f} seconds")
        print(f"  - Total Sessions: {len(final_status['recent_sessions'])}")
        print(f"  - System Health: {'Good' if final_status['is_running'] else 'Issues Detected'}")
        
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Error during example execution: {e}")
    finally:
        # Always stop the healer system
        logger.info("Stopping Self-Healer system...")
        await healer.stop()
        logger.info("Self-Healer system stopped")


async def demonstrate_manual_healing():
    """Demonstrate manual healing workflow."""
    logger = logging.getLogger('manual_healing_demo')
    
    logger.info("=== Manual Healing Demonstration ===")
    
    # This would be used when you want to manually trigger healing
    # for a specific error rather than relying on automatic detection
    
    healer = SelfHealerManager()
    
    try:
        await healer.start()
        
        # Create a specific error scenario
        error = ErrorDetail(
            category=ErrorCategory.JSON_PARSING,
            severity=ErrorSeverity.ERROR,
            title="Workflow JSON Format Error",
            message="Invalid JSON structure in workflow definition",
            user_guidance="Please check your workflow JSON for syntax errors",
            technical_details="JSONDecodeError: Expecting ',' delimiter: line 15, column 8",
            context={'error_id': 'manual_demo_001'}
        )
        
        # Manual healing workflow
        logger.info("1. Analyzing error context...")
        context = await healer.context_analyzer.analyze_error(error)
        
        logger.info("2. Generating solutions...")
        solutions = await healer.solution_generator.generate_solutions(error, context)
        
        logger.info("3. Validating solutions...")
        validated_solutions = []
        for solution in solutions:
            validation = await healer.solution_validator.validate_solution(solution, context)
            if validation['can_proceed']:
                validated_solutions.append((solution, validation))
        
        logger.info(f"Found {len(validated_solutions)} safe solutions")
        
        # In a real scenario, you would implement the best solution here
        # For demo purposes, we'll just show what would happen
        if validated_solutions:
            best_solution, best_validation = validated_solutions[0]
            logger.info(f"Best solution: {best_solution['title']}")
            logger.info(f"Confidence: {best_validation['confidence']:.2f}")
            logger.info("Would implement solution here...")
        
    finally:
        await healer.stop()


if __name__ == "__main__":
    print("Self-Healer System Example")
    print("=" * 50)
    print()
    
    # Run the main example
    asyncio.run(main())
    
    print()
    print("=" * 50)
    print("Example completed successfully!")
    print()
    print("To run manual healing demo:")
    print("python -c \"import asyncio; from example_usage import demonstrate_manual_healing; asyncio.run(demonstrate_manual_healing())\"")
