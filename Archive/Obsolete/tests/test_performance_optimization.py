#!/usr/bin/env python3
"""
Test Suite for Performance Optimization System
Verifies that performance optimizations work correctly for large workflows.

Task 1.1.5: Performance optimization for large workflows - Testing
"""

import unittest
import json
import time
import threading
from unittest.mock import patch, Mock
import logging
from pathlib import Path
import sys

# Add the n8n_builder module to path
sys.path.append(str(Path(__file__).parent.parent))

from n8n_builder.performance_optimizer import (
    PerformanceOptimizer, 
    WorkflowCache, 
    StreamingJSONProcessor,
    PerformanceMetrics,
    performance_optimizer
)
from n8n_builder.n8n_builder import N8NBuilder

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestPerformanceMetrics(unittest.TestCase):
    """Test performance metrics tracking."""
    
    def test_performance_metrics_creation(self):
        """Test creating and tracking performance metrics."""
        metrics = PerformanceMetrics("test_op_123", "test_operation")
        
        self.assertEqual(metrics.operation_id, "test_op_123")
        self.assertEqual(metrics.operation_type, "test_operation")
        self.assertGreater(metrics.start_time, 0)
        self.assertIsNone(metrics.end_time)
    
    def test_performance_metrics_completion(self):
        """Test completing performance metrics tracking."""
        metrics = PerformanceMetrics("test_op_123", "test_operation")
        
        # Simulate some processing time
        time.sleep(0.01)
        
        duration = metrics.finish()
        
        self.assertIsNotNone(metrics.end_time)
        self.assertGreater(duration, 0)
        self.assertGreater(metrics.duration, 0)
    
    def test_performance_metrics_cache_hit_rate(self):
        """Test cache hit rate calculation."""
        metrics = PerformanceMetrics("test_op_123", "test_operation")
        
        # No cache activity
        self.assertEqual(metrics.cache_hit_rate, 0.0)
        
        # Some cache hits
        metrics.cache_hits = 8
        metrics.cache_misses = 2
        self.assertEqual(metrics.cache_hit_rate, 80.0)
        
        # All cache hits
        metrics.cache_hits = 10
        metrics.cache_misses = 0
        self.assertEqual(metrics.cache_hit_rate, 100.0)
    
    def test_performance_metrics_to_dict(self):
        """Test converting metrics to dictionary."""
        metrics = PerformanceMetrics("test_op_123", "test_operation")
        metrics.node_count = 25
        metrics.cache_hits = 5
        metrics.optimizations_applied = ["cache_hit", "parallel_processing"]
        
        data = metrics.to_dict()
        
        self.assertEqual(data['operation_id'], "test_op_123")
        self.assertEqual(data['operation_type'], "test_operation")
        self.assertEqual(data['node_count'], 25)
        self.assertEqual(data['cache_hits'], 5)
        self.assertEqual(data['optimizations_applied'], ["cache_hit", "parallel_processing"])
        self.assertIn('duration', data)

class TestWorkflowCache(unittest.TestCase):
    """Test workflow caching system."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cache = WorkflowCache(max_size=10, max_memory_mb=1)
    
    def test_cache_set_and_get(self):
        """Test basic cache set and get operations."""
        workflow_json = '{"name": "test", "nodes": [{"id": "1", "type": "test"}]}'
        result = {"analysis": "test_result"}
        
        # Cache should be empty initially
        cached_result = self.cache.get(workflow_json, "analyze")
        self.assertIsNone(cached_result)
        
        # Set cache value
        self.cache.set(workflow_json, "analyze", result)
        
        # Should now return cached result
        cached_result = self.cache.get(workflow_json, "analyze")
        self.assertEqual(cached_result, result)
    
    def test_cache_key_generation(self):
        """Test cache key generation with different parameters."""
        workflow_json = '{"name": "test"}'
        
        # Different operations should have different keys  
        key1 = self.cache._generate_key(workflow_json, "analyze")
        key2 = self.cache._generate_key(workflow_json, "validate")
        self.assertNotEqual(key1, key2)
        
        # Same operation with different params should have different keys
        key3 = self.cache._generate_key(workflow_json, "analyze", {"param": "value"})
        self.assertNotEqual(key1, key3)
        
        # Same inputs should generate same key
        key4 = self.cache._generate_key(workflow_json, "analyze")
        self.assertEqual(key1, key4)
    
    def test_cache_size_limit_eviction(self):
        """Test LRU eviction when cache size limit is reached."""
        # Fill cache to capacity
        for i in range(self.cache.max_size):
            workflow_json = f'{{"name": "test_{i}"}}'
            result = f"result_{i}"
            self.cache.set(workflow_json, "test", result)
        
        # Verify cache is at capacity
        self.assertEqual(len(self.cache.cache), self.cache.max_size)
        
        # Add one more item to trigger eviction
        workflow_json = f'{{"name": "test_overflow"}}'
        self.cache.set(workflow_json, "test", "overflow_result")
        
        # Cache should still be at max size (evicted oldest)
        self.assertEqual(len(self.cache.cache), self.cache.max_size)
        
        # New item should be in cache
        cached_result = self.cache.get(workflow_json, "test")
        self.assertEqual(cached_result, "overflow_result")
    
    def test_cache_memory_estimation(self):
        """Test memory size estimation for cached items."""
        test_data = "small_string"
        size_mb = self.cache._estimate_size_mb(test_data)
        self.assertGreater(size_mb, 0)
        self.assertLess(size_mb, 1)  # Should be very small
        
        large_dict = {"data": "x" * 10000}  # Large data
        large_size_mb = self.cache._estimate_size_mb(large_dict)
        self.assertGreater(large_size_mb, size_mb)
    
    def test_cache_clear(self):
        """Test clearing all cached data."""
        # Add some data to cache
        self.cache.set('{"test": "data"}', "analyze", {"result": "test"})
        self.assertGreater(len(self.cache.cache), 0)
        
        # Clear cache
        self.cache.clear()
        
        # Cache should be empty
        self.assertEqual(len(self.cache.cache), 0)
        self.assertEqual(self.cache.total_memory_mb, 0.0)
    
    def test_cache_stats(self):
        """Test cache statistics."""
        # Add some data
        self.cache.set('{"test": "data"}', "analyze", {"result": "test"})
        
        stats = self.cache.get_stats()
        
        self.assertIn('total_items', stats)
        self.assertIn('total_memory_mb', stats)
        self.assertIn('memory_usage_percent', stats)
        self.assertEqual(stats['total_items'], 1)
        self.assertGreaterEqual(stats['total_memory_mb'], 0)

class TestStreamingJSONProcessor(unittest.TestCase):
    """Test streaming JSON processing for large workflows."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = StreamingJSONProcessor()
    
    def test_small_workflow_regular_parsing(self):
        """Test that small workflows use regular parsing."""
        small_workflow = {
            "name": "Small Workflow",
            "nodes": [
                {"id": "1", "name": "Node 1", "type": "test"},
                {"id": "2", "name": "Node 2", "type": "test"}
            ],
            "connections": {"1": {"main": [[{"node": "2"}]]}}
        }
        
        workflow_json = json.dumps(small_workflow)
        chunks = list(self.processor.parse_workflow_streaming(workflow_json))
        
        # Should return single chunk for small workflows
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], small_workflow)
    
    def test_large_workflow_streaming_parsing(self):
        """Test streaming parsing for large workflows."""
        # Create a large workflow (over 50KB to trigger streaming)
        large_workflow = {
            "name": "Large Workflow",
            "nodes": [],
            "connections": {}
        }
        
        # Add many nodes to make it large
        for i in range(1000):
            large_workflow["nodes"].append({
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": "n8n-nodes-base.function",
                "parameters": {"code": "a" * 100}  # Add bulk
            })
        
        workflow_json = json.dumps(large_workflow)
        
        # Should be large enough to trigger streaming
        self.assertGreater(len(workflow_json), 50000)
        
        chunks = list(self.processor.parse_workflow_streaming(workflow_json))
        
        # Should return multiple chunks for large workflows
        self.assertGreater(len(chunks), 1)
        
        # Verify chunk types
        chunk_types = [chunk.get('type') for chunk in chunks if 'type' in chunk]
        self.assertIn('metadata', chunk_types)
        self.assertIn('nodes', chunk_types)
        self.assertIn('connections', chunk_types)
    
    def test_parallel_node_analysis(self):
        """Test parallel node analysis for large node sets."""
        # Create many nodes to trigger parallel processing
        nodes = []
        for i in range(150):  # More than parallel threshold
            node_type = "n8n-nodes-base.manualTrigger" if i < 5 else "n8n-nodes-base.function"
            nodes.append({
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": node_type
            })
        
        result = self.processor._parallel_node_analysis(nodes)
        
        self.assertEqual(len(result["node_types"]), 150)
        self.assertEqual(len(result["triggers"]), 5)  # First 5 are triggers
        self.assertEqual(len(result["actions"]), 145)  # Rest are actions
    
    def test_sequential_node_analysis(self):
        """Test sequential node analysis for smaller node sets."""
        nodes = [
            {"id": "1", "name": "Trigger", "type": "n8n-nodes-base.manualTrigger"},
            {"id": "2", "name": "Action", "type": "n8n-nodes-base.function"}
        ]
        
        result = self.processor._sequential_node_analysis(nodes)
        
        self.assertEqual(len(result["node_types"]), 2)
        self.assertEqual(len(result["triggers"]), 1)
        self.assertEqual(len(result["actions"]), 1)
    
    def test_optimized_data_flow_analysis(self):
        """Test optimized data flow analysis."""
        # Test with reasonable connection count
        small_connections = {
            "node1": {"main": [[{"node": "node2"}]]},
            "node2": {"main": [[{"node": "node3"}]]}
        }
        
        result = self.processor._analyze_data_flow_optimized(small_connections)
        self.assertEqual(len(result), 2)
        
        # Test with large connection count (should sample)
        large_connections = {}
        for i in range(1500):  # More than 1000 threshold
            large_connections[f"node_{i}"] = {"main": [[{"node": f"node_{i+1}"}]]}
        
        result = self.processor._analyze_data_flow_optimized(large_connections)
        # Should have note about sampling and sample results
        self.assertGreater(len(result), 0)
        # Check if sampling note is included
        note_found = any("sample" in str(item).lower() for item in result if isinstance(item, dict))
        self.assertTrue(note_found)

class TestPerformanceOptimizer(unittest.TestCase):
    """Test the main performance optimizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = PerformanceOptimizer()
    
    def test_performance_tracking_lifecycle(self):
        """Test complete performance tracking lifecycle."""
        operation_id = "test_operation_123"
        operation_type = "test_modify_workflow"
        
        # Start tracking
        metrics = self.optimizer.start_performance_tracking(operation_id, operation_type)
        
        self.assertEqual(metrics.operation_id, operation_id)
        self.assertEqual(metrics.operation_type, operation_type)
        self.assertIn(operation_id, self.optimizer.performance_metrics)
        
        # Add a small delay to ensure measurable duration
        time.sleep(0.002)
        
        # Finish tracking
        final_metrics = self.optimizer.finish_performance_tracking(operation_id)
        
        self.assertIsNotNone(final_metrics)
        self.assertIsNotNone(final_metrics.end_time)
        self.assertGreaterEqual(final_metrics.duration, 0.001)  # Should be at least 1ms
    
    def test_workflow_processing_optimization_cache_hit(self):
        """Test workflow processing with cache hit."""
        workflow_json = '{"name": "Test", "nodes": [{"id": "1", "type": "test"}]}'
        
        # First call should miss cache
        result1, metrics1 = self.optimizer.optimize_workflow_processing(workflow_json, 'analyze')
        self.assertEqual(metrics1.cache_misses, 1)
        self.assertEqual(metrics1.cache_hits, 0)
        
        # Second call should hit cache
        result2, metrics2 = self.optimizer.optimize_workflow_processing(workflow_json, 'analyze')
        self.assertEqual(metrics2.cache_hits, 1)
        self.assertEqual(metrics2.cache_misses, 0)
        self.assertIn("cache_hit", metrics2.optimizations_applied)
    
    def test_large_workflow_optimization_strategy(self):
        """Test that large workflows trigger appropriate optimizations."""
        # Create large workflow JSON (over 1MB)
        large_workflow = {
            "name": "Very Large Workflow",
            "nodes": [],
            "connections": {}
        }
        
        # Add enough data to exceed large_json_bytes threshold
        for i in range(2000):
            large_workflow["nodes"].append({
                "id": f"huge_node_{i}",
                "name": f"Huge Node {i}",
                "type": "n8n-nodes-base.function",
                "parameters": {"code": "x" * 1000}  # 1KB per node
            })
        
        workflow_json = json.dumps(large_workflow)
        self.assertGreater(len(workflow_json.encode('utf-8')), 1024 * 1024)  # Over 1MB
        
        result, metrics = self.optimizer.optimize_workflow_processing(workflow_json, 'analyze')
        
        # Should trigger large workflow optimizations
        self.assertIn("streaming_processing", metrics.optimizations_applied)
        self.assertTrue(metrics.streaming_used)
        self.assertGreater(metrics.input_size_bytes, 1024 * 1024)
    
    def test_cache_result_decision(self):
        """Test cache result decision logic."""
        # Small workflow should be cached
        small_workflow = '{"name": "Small", "nodes": []}'
        self.assertTrue(self.optimizer._should_cache_result(small_workflow, {"result": "small"}))
        
        # Very large workflow should not be cached (exceed 2MB threshold = 2 * 1024 * 1024 bytes)
        # The optimizer threshold is large_json_bytes * 2 = 1MB * 2 = 2MB
        large_workflow_data = "x" * (3 * 1024 * 1024)  # 3MB string
        self.assertFalse(self.optimizer._should_cache_result(large_workflow_data, {"result": "large"}))
        
        # Large result should not be cached (exceed 1MB threshold)
        large_result = "y" * (2 * 1024 * 1024)  # 2MB result
        self.assertFalse(self.optimizer._should_cache_result(small_workflow, large_result))
    
    def test_performance_summary_generation(self):
        """Test performance summary generation."""
        # Perform some operations to generate metrics
        workflow_json = '{"name": "Test", "nodes": [{"id": "1", "type": "test"}]}'
        
        # Multiple operations
        for i in range(3):
            result, metrics = self.optimizer.optimize_workflow_processing(
                workflow_json, f'test_operation_{i}'
            )
        
        summary = self.optimizer.get_performance_summary()
        
        self.assertIn('total_operations', summary)
        self.assertIn('average_duration', summary)
        self.assertIn('total_cache_hits', summary)
        self.assertIn('average_cache_hit_rate', summary)
        self.assertIn('optimizations_used', summary)
        self.assertIn('cache_stats', summary)
        
        self.assertGreater(summary['total_operations'], 0)
    
    def test_cache_stats_integration(self):
        """Test cache statistics integration."""
        workflow_json = '{"name": "Test", "nodes": [{"id": "1", "type": "test"}]}'
        
        # Perform operation to populate cache
        self.optimizer.optimize_workflow_processing(workflow_json, 'analyze')
        
        cache_stats = self.optimizer.get_cache_stats()
        
        self.assertIn('total_items', cache_stats)
        self.assertIn('total_memory_mb', cache_stats)
        self.assertGreaterEqual(cache_stats['total_items'], 0)
    
    def test_cache_clear_functionality(self):
        """Test cache clearing functionality."""
        workflow_json = '{"name": "Test", "nodes": [{"id": "1", "type": "test"}]}'
        
        # Add something to cache
        self.optimizer.optimize_workflow_processing(workflow_json, 'analyze')
        
        # Verify cache has content
        cache_stats_before = self.optimizer.get_cache_stats()
        
        # Clear cache
        self.optimizer.clear_cache()
        
        # Verify cache is empty
        cache_stats_after = self.optimizer.get_cache_stats()
        self.assertEqual(cache_stats_after['total_items'], 0)
        self.assertEqual(cache_stats_after['total_memory_mb'], 0.0)

class TestN8NBuilderPerformanceIntegration(unittest.TestCase):
    """Test N8N Builder integration with performance optimization."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.builder = N8NBuilder()
    
    def test_builder_has_performance_optimizer(self):
        """Test that N8N Builder has performance optimizer initialized."""
        self.assertIsNotNone(self.builder.performance_optimizer)
        self.assertIsInstance(self.builder.performance_optimizer, PerformanceOptimizer)
    
    def test_workflow_analysis_performance_optimization(self):
        """Test that workflow analysis uses performance optimization."""
        # Create a workflow for analysis
        workflow = {
            "name": "Test Workflow",
            "nodes": [
                {"id": "1", "name": "Start", "type": "n8n-nodes-base.manualTrigger"},
                {"id": "2", "name": "Process", "type": "n8n-nodes-base.function"}
            ],
            "connections": {"1": {"main": [[{"node": "2"}]]}}
        }
        
        # Call analysis method
        result = self.builder._analyze_workflow(workflow)
        
        # Should return analysis results
        self.assertIn('node_count', result)
        self.assertIn('node_types', result)
        self.assertIn('analysis_type', result)
        self.assertEqual(result['node_count'], 2)
        self.assertEqual(len(result['node_types']), 2)
    
    def test_large_workflow_analysis_optimization(self):
        """Test analysis optimization for large workflows."""
        # Create large workflow to trigger optimizations
        large_workflow = {
            "name": "Large Workflow",
            "nodes": [],
            "connections": {}
        }
        
        # Add many nodes
        for i in range(150):  # Enough to trigger parallel processing
            large_workflow["nodes"].append({
                "id": f"node_{i}",
                "name": f"Node {i}",
                "type": "n8n-nodes-base.function"
            })
        
        # Analyze workflow
        result = self.builder._analyze_workflow(large_workflow)
        
        # Should handle large workflow efficiently
        self.assertEqual(result['node_count'], 150)
        self.assertEqual(len(result['node_types']), 150)
    
    def test_workflow_analysis_caching(self):
        """Test that workflow analysis results are cached."""
        workflow = {
            "name": "Cache Test Workflow",
            "nodes": [{"id": "1", "name": "Test", "type": "n8n-nodes-base.manualTrigger"}],
            "connections": {}
        }
        
        # First analysis
        result1 = self.builder._analyze_workflow(workflow)
        
        # Second analysis (should use cache)
        result2 = self.builder._analyze_workflow(workflow)
        
        # Results should be identical
        self.assertEqual(result1, result2)
    
    def test_performance_optimizer_memory_tracking(self):
        """Test memory usage tracking in performance optimizer."""
        workflow_json = '{"name": "Memory Test", "nodes": [{"id": "1", "type": "test"}]}'
        
        result, metrics = self.builder.performance_optimizer.optimize_workflow_processing(
            workflow_json, 'analyze'
        )
        
        # Memory metrics should be tracked
        self.assertGreaterEqual(metrics.memory_before_mb, 0)
        self.assertGreaterEqual(metrics.memory_after_mb, 0)

class TestPerformanceOptimizationThreadSafety(unittest.TestCase):
    """Test thread safety of performance optimization components."""
    
    def test_cache_thread_safety(self):
        """Test that cache operations are thread-safe."""
        cache = WorkflowCache(max_size=100, max_memory_mb=10)
        results = []
        errors = []
        
        def cache_operations(thread_id):
            try:
                for i in range(10):
                    workflow_json = f'{{"name": "test_{thread_id}_{i}"}}'
                    result = f"result_{thread_id}_{i}"
                    
                    # Set and get operations
                    cache.set(workflow_json, "test", result)
                    cached_result = cache.get(workflow_json, "test")
                    
                    if cached_result == result:
                        results.append(f"thread_{thread_id}_success_{i}")
                    else:
                        results.append(f"thread_{thread_id}_failure_{i}")
            except Exception as e:
                errors.append(f"thread_{thread_id}_error: {str(e)}")
        
        # Run multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=cache_operations, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Should have no errors and all successes
        self.assertEqual(len(errors), 0, f"Thread safety errors: {errors}")
        success_count = len([r for r in results if "success" in r])
        self.assertEqual(success_count, 50)  # 5 threads * 10 operations each

if __name__ == '__main__':
    # Run with increased verbosity to see detailed test output
    unittest.main(verbosity=2) 