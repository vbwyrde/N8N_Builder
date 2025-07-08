# 🤖 N8N_Builder Community Edition - AI-Powered Workflow Automation

**Transform plain English into powerful n8n workflows with local AI**

<!-- Testing enhanced automation with PR warning system -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-supported-blue.svg)](https://www.docker.com/)
[![Community Edition](https://img.shields.io/badge/edition-community-green.svg)](https://github.com/vbwyrde/N8N_Builder)

## 🎯 What is N8N_Builder?

N8N_Builder is an intelligent workflow automation system that converts natural language descriptions into fully functional n8n workflows. Simply describe what you want to automate in plain English, and N8N_Builder generates the complete JSON workflow ready for n8n.

**🌟 This is the Community Edition** - A powerful, free, and open-source version that provides core workflow generation capabilities with local AI processing.

### ✨ **Community Edition Features**

- **🧠 AI-Powered Generation**: Uses local LLM models (LM Studio) for complete privacy
- **📝 Natural Language Input**: Describe workflows in plain English
- **🔄 Complete Automation**: Generates full n8n-compatible JSON workflows
- **🏠 100% Local Processing**: All AI processing happens on your machine
- **🐳 Docker Ready**: Easy deployment with Docker containers
- **🔧 Developer Friendly**: REST API and extensible architecture
- **📚 Research Integration**: Accesses n8n documentation for accurate workflows
- **✅ Validation System**: Ensures generated workflows are valid and functional
- **🎨 Web Interface**: User-friendly web interface for workflow generation

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8 or higher
- [LM Studio](https://lmstudio.ai/) running locally
- [n8n](https://n8n.io/) (Docker or standalone)
- Git

### **⚡ Lightning Setup (2 minutes)**

1. **Clone the repository**
   ```bash
   git clone https://github.com/vbwyrde/N8N_Builder.git
   cd N8N_Builder
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start LM Studio**
   - Download and install [LM Studio](https://lmstudio.ai/)
   - Load a model (recommended: mimo-vl-7b-rl@q8_k_xl)
   - Start the local server (default: localhost:1234)

4. **Run N8N_Builder**
   ```bash
   python run.py
   ```

5. **Access the interface**
   - **Web Interface**: http://localhost:8002
   - **API Documentation**: http://localhost:8002/docs
   - Start creating workflows with natural language!

## 🎮 How to Use

### **Web Interface Method**

1. **Open your browser** to http://localhost:8002
2. **Describe your workflow** in the text area:
   ```
   "Create a workflow that monitors my Gmail for new emails, 
   extracts important information, and saves it to a Google Sheet"
   ```
3. **Click Generate** and watch N8N_Builder create your workflow
4. **Download the JSON** and import it into n8n
5. **Configure credentials** in n8n and start automating!

### **API Usage**

```python
import requests

# Generate a workflow
response = requests.post('http://localhost:8002/generate', json={
    'description': 'Send a Slack message when a new file is added to Dropbox',
    'complexity': 'medium'
})

workflow = response.json()
print(f"Generated workflow: {workflow['name']}")
```

### **Command Line Usage**

```bash
# Generate a workflow from command line
python -m n8n_builder.cli generate "Monitor RSS feed and post to Twitter"

# Validate an existing workflow
python -m n8n_builder.cli validate workflow.json
```

## 🏗️ Architecture

### **Core Components**
- **🧠 AI Engine**: Local LLM integration via LM Studio
- **🔄 Workflow Generator**: Converts descriptions to n8n JSON
- **🌐 REST API**: FastAPI-based web interface with OpenAPI docs
- **🔍 Validation System**: Ensures workflow quality and n8n compatibility
- **📚 Research Integration**: Real-time access to n8n documentation
- **🎨 Web Interface**: Clean, responsive interface for workflow generation

### **Supported Integrations**
- **📧 Email**: Gmail, Outlook, IMAP, SMTP
- **☁️ Cloud Storage**: Google Drive, Dropbox, OneDrive, AWS S3
- **💬 Communication**: Slack, Discord, Microsoft Teams, Telegram
- **🗄️ Databases**: MySQL, PostgreSQL, MongoDB, SQLite
- **🌐 APIs**: REST, GraphQL, Webhooks, HTTP requests
- **📊 Productivity**: Google Sheets, Airtable, Notion, Trello
- **🔧 Development**: GitHub, GitLab, Jenkins, Docker
- **And 200+ more n8n integrations...**

## 📚 Documentation

### 🎯 **User Guides**
- **📖 [Complete Documentation](Documentation/README.md)** - Master guide
- **🔧 [Troubleshooting](Documentation/TROUBLESHOOTING.md)** - Fix common issues
- **⚡ [API Quick Reference](Documentation/api/API_QUICK_REFERENCE.md)** - Common examples

### 🔧 **For Developers**
- **📚 [API Documentation](Documentation/api/API_DOCUMENTATION.md)** - Complete reference
- **🏗️ [Technical Architecture](Documentation/technical/DOCUMENTATION.md)** - System design

## 🛠️ Advanced Usage

### **Custom AI Models**
```yaml
# config.yaml
ai:
  endpoint: "http://localhost:1234/v1"
  model: "your-preferred-model"
  max_tokens: 2000
  temperature: 0.7
```

### **Docker Deployment**
```bash
# Build and run with Docker
docker build -t n8n-builder .
docker run -p 8002:8002 n8n-builder
```

### **Development Scripts**
```bash
# Analyze project structure
python Scripts/analyze_project_files.py

# Generate process flow documentation
python Scripts/generate_process_flow.py

# Setup log rotation
.\Scripts\Setup-LogRotation.ps1 -Setup
```

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `python -m pytest tests/`
5. **Submit a pull request**

### **Development Setup**
```bash
# Clone your fork
git clone https://github.com/yourusername/N8N_Builder.git
cd N8N_Builder

# Install development dependencies
pip install -r requirements.txt
pip install -e .

# Run tests
python -m pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **🐛 [GitHub Issues](https://github.com/vbwyrde/N8N_Builder/issues)** - Report bugs or request features
- **💬 [Discussions](https://github.com/vbwyrde/N8N_Builder/discussions)** - Ask questions and share ideas
- **📖 [Documentation](Documentation/README.md)** - Comprehensive guides and tutorials

## 🙏 Acknowledgments

- **[n8n](https://n8n.io/)** - The amazing workflow automation platform
- **[LM Studio](https://lmstudio.ai/)** - Local AI model hosting
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern web framework for APIs
- **The open-source community** - For inspiration and contributions

---

**🎉 Ready to start automating?** Follow the [Quick Start](#quick-start) guide and create your first AI-generated workflow in minutes!

This is a Quick Commit Test - Test Version 5.