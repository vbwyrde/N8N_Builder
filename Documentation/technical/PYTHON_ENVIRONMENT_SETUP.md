# 🐍 Python Environment Setup Guide

**🎯 Goal**: Understand and properly configure the Python runtime environment for N8N_Builder

## Overview

N8N_Builder requires a properly configured Python virtual environment to function correctly. This guide explains why, how to set it up, and how to troubleshoot common issues.

## Why Virtual Environment is Critical

### Technical Requirements
1. **Database Integration**: The MCP Database Tool requires `pyodbc` to be available in the Python environment
2. **Process Management**: Emergency shutdown logic depends on proper process isolation and PID detection
3. **Dependency Isolation**: Prevents conflicts between N8N_Builder dependencies and system Python packages
4. **IDE Compatibility**: Ensures proper import resolution in development environments like Augment Code

### Common Issues Without Virtual Environment
- Import errors for `pyodbc` and other dependencies
- Process detection failures causing emergency shutdown to kill itself
- Conflicts with system-wide Python packages
- IDE reporting missing imports even when packages are installed globally

## Detailed Setup Instructions

### 1. Create Virtual Environment
```bash
# Navigate to N8N_Builder directory
cd N8N_Builder

# Create virtual environment
python -m venv venv

# Alternative: Create with specific Python version
python3.11 -m venv venv
```

### 2. Activate Virtual Environment

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
# Ensure you're in the activated virtual environment
# Your prompt should show (venv) prefix

pip install -r requirements.txt
```

### 4. Verify Installation
```bash
# Check Python executable location
which python  # Linux/Mac
where python   # Windows
# Should show path inside venv directory

# Test critical imports
python -c "import pyodbc; print('✅ pyodbc available:', pyodbc.version)"
python -c "from n8n_builder.mcp_database_tool import get_mcp_database; print('✅ MCP Database tool ready')"
python -c "import psutil; print('✅ psutil available:', psutil.version_info)"
```

## Running N8N_Builder with Virtual Environment

### Method 1: Startup Scripts (Recommended)
The provided startup scripts automatically handle virtual environment activation:

```bash
# Windows PowerShell
.\Scripts\run_with_venv.ps1

# Windows Command Prompt
Scripts\run_with_venv.bat
```

These scripts:
- Check if virtual environment exists
- Verify dependencies are installed
- Use the correct Python executable
- Provide clear error messages if setup is incorrect

### Method 2: Manual Activation
```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# Run N8N_Builder
python run.py
```

### Method 3: Direct Virtual Environment Python
```bash
# Use venv Python directly (no activation needed)
.\venv\Scripts\python.exe run.py  # Windows
./venv/bin/python run.py          # Linux/Mac
```

## Technical Details

### Process Detection Issue Resolution
The virtual environment setup resolves a critical process detection issue where:

1. **Problem**: When running with system Python, the emergency shutdown could incorrectly identify processes
2. **Root Cause**: Windows process resolution differences between system Python and virtual environment Python
3. **Solution**: The `is_current_process_safe()` function uses multiple detection methods:
   - Direct PID comparison
   - Executable path + script path comparison
   - Handles both real processes and "ghost" processes

### Emergency Shutdown Logic
The emergency shutdown function now safely:
- Identifies N8N_Builder processes using specific patterns
- Preserves the current process using robust detection
- Kills only confirmed N8N_Builder processes
- Avoids system process interference

## Troubleshooting

### Virtual Environment Issues

**"Virtual environment not found"**
```bash
# Recreate virtual environment
python -m venv venv --clear
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**"pyodbc could not be resolved"**
```bash
# Check if you're in virtual environment
where python  # Should show venv path

# If not, activate and install
.\venv\Scripts\Activate.ps1
pip install pyodbc>=4.0.39
```

**"Process kills itself on startup"**
```bash
# Ensure using virtual environment Python
.\venv\Scripts\python.exe run.py

# Or use startup script
.\Scripts\run_with_venv.ps1
```

### Dependency Issues

**"Package not found errors"**
```bash
# Reinstall all dependencies in virtual environment
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt --force-reinstall
```

**"Invalid metadata warnings"**
```bash
# These warnings are usually harmless but can be fixed by:
pip install --upgrade setuptools pip
pip install -r requirements.txt --force-reinstall
```

### IDE Configuration

**"Imports not resolved in IDE"**
1. Ensure IDE is configured to use the virtual environment Python
2. Point IDE Python interpreter to: `./venv/Scripts/python.exe` (Windows)
3. Restart IDE language server if needed

## Environment Recovery

### Complete Environment Reset
```bash
# Remove existing virtual environment
Remove-Item -Recurse -Force venv  # PowerShell
# rm -rf venv                     # Linux/Mac

# Recreate from scratch
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Verify setup
python -c "import pyodbc; print('✅ Environment ready')"
```

### Backup and Restore
```bash
# Backup working environment
pip freeze > working_requirements.txt

# Restore to working state
pip install -r working_requirements.txt
```

## Best Practices

1. **Always use virtual environment**: Never install N8N_Builder dependencies globally
2. **Use startup scripts**: They handle environment verification automatically
3. **Verify before running**: Check imports work before starting the system
4. **Document changes**: If you modify dependencies, update requirements.txt
5. **Regular maintenance**: Periodically recreate virtual environment to ensure cleanliness

## Integration with Development Tools

### Augment Code IDE
- Configure Python interpreter to use `./venv/Scripts/python.exe`
- Ensure workspace Python path includes virtual environment
- Restart language server after environment changes

### Other IDEs
- **VS Code**: Select Python interpreter from venv
- **PyCharm**: Configure project interpreter to virtual environment
- **Vim/Neovim**: Ensure Python LSP uses venv Python

---

**📝 Note**: This environment setup is critical for N8N_Builder functionality. When in doubt, recreate the virtual environment from scratch rather than trying to fix a corrupted one.

**🔗 Related**: [Getting Started Guide](../../GETTING_STARTED.md) | [Troubleshooting Guide](../TROUBLESHOOTING.md)
