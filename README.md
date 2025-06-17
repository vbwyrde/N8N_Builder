# N8N Workflow Builder

🤖 **Transform plain English into powerful N8N workflows using AI**

N8N Workflow Builder is an intelligent automation tool that converts natural language descriptions into executable N8N workflows. Simply describe what you want to automate in plain English, and get production-ready workflow JSON that you can import directly into N8N.

## 🎯 What This Does

**For Business Users:**
- Create complex automation workflows without coding
- Describe processes in plain English: *"Send me an email when a new file is uploaded"*
- Get instant, working N8N workflows ready to deploy

**For Developers:**
- Rapid prototyping of automation workflows
- AI-powered workflow generation with validation
- REST API for integration into larger systems
- Extensible architecture for custom patterns

## ✨ Key Features

- **Natural Language to Workflow** - AI-powered conversion using local LLM
- **Real-time Validation** - Ensures workflows meet N8N standards
- **Web Interface & CLI** - Multiple ways to interact with the system
- **Workflow Modification** - Update existing workflows with new requirements
- **Agent Architecture** - Extensible system for custom processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Local LLM server (Mimo VL 7B recommended) or LLM API access
- N8N instance for testing workflows

### Installation

1. **Clone and Setup**
   ```bash
   git clone https://github.com/vbwyrde/N8N_Builder.git
   cd N8N_Builder
   pip install -r requirements.txt
   ```

2. **Configure Your LLM** (create `.env` file)
   ```bash
   # For local LLM (recommended)
   MIMO_ENDPOINT=http://localhost:1234/v1/chat/completions
   MIMO_MODEL=mimo-vl-7b
   MIMO_IS_LOCAL=true

   # For external LLM services
   # MIMO_IS_LOCAL=false
   # MIMO_API_KEY=your_api_key_here
   ```

3. **Start the Application**
   ```bash
   python -m n8n_builder.cli serve
   ```

4. **Create Your First Workflow**
   - Open `http://localhost:8000` in your browser
   - Type: *"Send me an email when a new file is uploaded to my folder"*
   - Click "Generate Workflow"
   - Copy the JSON to your N8N instance

## 💡 Example Use Cases

- **File Monitoring**: *"Alert me when files are added to a specific folder"*
- **Data Processing**: *"Convert CSV files to JSON and send to a webhook"*
- **E-commerce**: *"Send customer welcome emails after purchase"*
- **Social Media**: *"Post to Twitter when I publish a new blog article"*
- **System Monitoring**: *"Check website status every 5 minutes and alert if down"*

## 🛠️ Usage Options

### Web Interface (Recommended)
```bash
python -m n8n_builder.cli serve
# Open http://localhost:8000
```

### Command Line
```bash
# Generate workflow
python -m n8n_builder.cli generate "Send email when file uploaded" -o workflow.json

# Modify existing workflow
python -m n8n_builder.cli modify workflow.json "Add SMS notification" -o updated.json
```

### REST API
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"description": "Your workflow description here"}'
```

## 🚀 Recent Updates (June 2025)

**Major Bug Fixes & Improvements:**
- ✅ **Fixed Critical Validation Bugs** - Workflow modifications now apply successfully
- ✅ **Enhanced LLM Response Parsing** - Robust handling of reasoning models
- ✅ **Intelligent Node Validation** - Allows acceptable isolated nodes
- ✅ **Comprehensive Error Handling** - Enhanced retry logic and fallback strategies

**Result:** Email nodes, database connections, and workflow modifications now work reliably!

## 📚 Documentation

For comprehensive documentation, see **[Documentation/DOCUMENTATION.MD](Documentation/DOCUMENTATION.MD)**:

- **🏗️ Technical Architecture** - System design and component details
- **🔧 Advanced Configuration** - Environment variables and custom settings
- **🛠️ Development Guide** - Adding features, custom agents, and patterns
- **📊 Monitoring & Analytics** - Performance metrics and health monitoring
- **🔄 Complete API Reference** - All endpoints with examples
- **🧪 Testing & Debugging** - Comprehensive testing and troubleshooting guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Development Guidelines:**
- Follow the agent-based architecture patterns
- Add comprehensive tests for new features
- Update documentation for API changes
- Use the logging system for debugging information

## 🔧 Quick Troubleshooting

**LLM Connection Issues:**
- Ensure your local LLM server is running
- Verify `MIMO_ENDPOINT` in your `.env` file
- Check logs in `logs/n8n_builder.llm.log`

**Validation Failures:**
- Check `logs/n8n_builder.validation.log` for details
- Ensure workflow has proper node connections
- Recent fixes resolved most validation issues

For detailed troubleshooting, see the [full documentation](Documentation/DOCUMENTATION.MD).

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- **n8n team** for the workflow automation platform
- **Mimo VL 7B team** for the local LLM capabilities
- **FastAPI** for the excellent web framework
- **Open-source community** for inspiration and contributions

---

**Ready to automate your workflows with AI?** [Get started now](#-quick-start) or explore the [complete documentation](Documentation/DOCUMENTATION.MD)!