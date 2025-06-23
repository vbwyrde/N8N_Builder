# 🧪 N8N_Builder Test Suite

## 📋 Overview

This directory contains the complete test suite for the N8N_Builder system, including comprehensive tests for the MCP Research Tool integration and core functionality.

## 🗂️ Test Structure

### **MCP Research Tool Tests**
- **`test_mcp_research.py`** - Core MCP research functionality tests
- **`test_complete_integration.py`** - Full system integration tests
- **`test_research_quality.py`** - Research quality and performance tests

### **Core System Tests**
- **`test_n8n_builder.py`** - Main N8N_Builder functionality
- **`test_workflow_validation.py`** - Workflow validation and parsing
- **`test_api_endpoints.py`** - API endpoint testing

## 🚀 Running Tests

### **Quick Test Run**
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python tests/test_mcp_research.py

# Run with verbose output
python -m pytest tests/ -v
```

### **Individual Test Files**
```bash
# MCP Research Tool tests
python tests/test_mcp_research.py

# Complete integration tests
python tests/test_complete_integration.py

# Research quality tests
python tests/test_research_quality.py
```

## 📊 Test Coverage

### **MCP Research Tool Tests**
- ✅ **Offline functionality** - Mock data processing and formatting
- ✅ **Online research tool** - Real-time web scraping and API calls
- ✅ **Integration test** - Full N8N_Builder system integration
- ✅ **Cache performance** - Enhanced caching with fallback mechanisms
- ✅ **Error handling** - Graceful degradation and recovery

### **Expected Test Results**
```
📊 TEST SUMMARY
==================================================
Offline functionality: ✅ PASS
Online research tool: ✅ PASS  
Integration test: ✅ PASS
🎉 All tests passed! MCP Research Tool is ready to use.
```

## 🔧 Test Configuration

### **Environment Setup**
Tests automatically configure the necessary environment:
- **Import paths** - Configured to work from tests directory
- **Mock data** - Included for offline testing
- **Cache handling** - Temporary cache for test isolation
- **Error simulation** - Network failure and timeout testing

### **Dependencies**
All test dependencies are included in the main `requirements.txt`:
- `beautifulsoup4>=4.12.2` - HTML parsing
- `lxml>=4.9.3` - XML/HTML processing
- `pytest` - Test framework (optional, tests can run standalone)

## 🐛 Troubleshooting

### **Common Issues**

#### **Import Errors**
```
ModuleNotFoundError: No module named 'n8n_builder'
```
**Solution**: Tests automatically add parent directory to path. If issues persist, run from project root:
```bash
cd /path/to/N8N_Builder
python tests/test_mcp_research.py
```

#### **Network Timeouts**
```
HTTP Request timeout
```
**Solution**: Tests include retry logic and graceful degradation. Network failures are expected and handled.

#### **Cache Conflicts**
```
Enhanced cache put failed
```
**Solution**: Tests automatically fall back to simple cache. This is expected behavior.

## 📈 Performance Benchmarks

### **Typical Test Performance**
- **test_mcp_research.py**: ~30-60 seconds (includes network calls)
- **test_complete_integration.py**: ~45-90 seconds (full system test)
- **test_research_quality.py**: ~60-120 seconds (comprehensive quality tests)

### **Network-Dependent Tests**
Some tests make real HTTP requests to:
- n8n official documentation
- n8n community forum
- GitHub repositories (rate limited)

These tests may occasionally fail due to:
- Network connectivity issues
- Rate limiting (HTTP 429)
- Service availability (HTTP 404, 503)

This is expected and does not indicate system failure.

## 🔍 Test Details

### **test_mcp_research.py**
- **Purpose**: Core MCP research tool functionality
- **Coverage**: Offline processing, online research, caching
- **Duration**: ~30-60 seconds
- **Network**: Yes (with fallback)

### **test_complete_integration.py**
- **Purpose**: Full system integration testing
- **Coverage**: End-to-end workflow generation with research
- **Duration**: ~45-90 seconds
- **Network**: Yes (with fallback)

### **test_research_quality.py**
- **Purpose**: Research quality and performance optimization
- **Coverage**: Multiple workflow types, accuracy metrics
- **Duration**: ~60-120 seconds
- **Network**: Yes (extensive)

## 📝 Adding New Tests

### **Test File Template**
```python
#!/usr/bin/env python3
"""
Test Description

Brief description of what this test covers.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports when running from tests folder
sys.path.insert(0, str(Path(__file__).parent.parent))

# Your test imports and code here
```

### **Best Practices**
1. **Include import path setup** for standalone execution
2. **Use descriptive test names** and docstrings
3. **Handle network failures gracefully** with try/except
4. **Include both positive and negative test cases**
5. **Document expected behavior** in comments

## 🎯 Test Goals

The test suite ensures:
- ✅ **Reliability** - System works consistently
- ✅ **Performance** - Acceptable response times
- ✅ **Error Handling** - Graceful failure modes
- ✅ **Integration** - Components work together
- ✅ **Quality** - Research results meet standards

## 📚 Related Documentation

- **[MCP Research Setup Guide](../Documentation/MCP_RESEARCH_SETUP_GUIDE.md)** - Integration details
- **[API Documentation](../Documentation/API_DOCUMENTATION.md)** - API testing reference
- **[Technical Architecture](../Documentation/DOCUMENTATION.MD)** - System design

---

**🧪 Ready to test?** Run `python tests/test_mcp_research.py` to get started!
