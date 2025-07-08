# 🔧 Developer Workflow Guide

**N8N_Builder Development Workflow - Community Edition Separation System**

This guide explains the development workflow for N8N_Builder, which maintains both private proprietary components and a public Community Edition using an automated separation system.

## 🎯 **Overview**

N8N_Builder uses a dual-repository approach:
- **N8N_Builder** (Main): Contains all code (private + community) - stays local
- **N8N_Builder_Community**: Contains only community-safe code - syncs to GitHub

This allows us to develop with full functionality while automatically maintaining a clean public repository.

## 🏗️ **Repository Architecture**

```
Local Development:
├── N8N_Builder/ (MAIN WORKSPACE)
│   ├── Enterprise_Module/ (Private - never synced)
│   ├── Enterprise_Database/ (Private - never synced)
│   ├── Community Code (synced to public)
│   ├── Scripts/commit-and-sync-simple.ps1 (automation)
│   └── .vscode/tasks.json (VS Code integration)
│
├── N8N_Builder_Community/ (OUTPUT)
│   ├── Community Code Only
│   └── Remote: https://github.com/vbwyrde/N8N_Builder.git
│
GitHub Public Repository:
└── https://github.com/vbwyrde/N8N_Builder (Community Edition Only)
```

## 🚀 **Daily Development Workflow**

### **Standard Workflow (Recommended)**

1. **Work in N8N_Builder** (main workspace in VS Code/Augment)
2. **Make changes** to any files (private or community)
3. **When ready to commit**:
   - Press `Ctrl+Shift+P` in VS Code
   - Type: "Tasks: Run Task"
   - Select: "Commit and Sync Community"
4. **Follow prompts**:
   - Enter commit message for main repository
   - Enter community message (or press Enter to skip GitHub sync)
5. **Continue working** (stay in same workspace)

### **Alternative: Direct Script Execution**

```powershell
# From N8N_Builder root directory
.\Scripts\commit-and-sync-simple.ps1
```

## 📋 **Workflow Options**

### **Option 1: Commit + Sync (Most Common)**
- **Use when**: You have changes ready for both local and public repositories
- **Result**: Commits locally + syncs to GitHub
- **Prompts**: Main commit message + community message

### **Option 2: Commit Only (Local Development)**
- **Use when**: Working on private features or incomplete changes
- **Result**: Commits only to main repository
- **How**: Provide main commit message, press Enter for community message

### **Option 3: Sync Only (Manual)**
- **Use when**: Main repository already committed, need to sync to community
- **Script**: `.\Scripts\sync-community-only.ps1`
- **Result**: Syncs existing changes to GitHub

## 🛡️ **Safety Features**

### **Automatic Private Component Protection**
- **Main repository**: No GitHub remote configured (prevents accidental pushes)
- **Separation system**: Automatically filters out private components
- **File sanitization**: Removes private references from community files
- **Validation**: Ensures only safe content reaches GitHub

### **What Gets Synced vs. What Stays Private**

#### **✅ Synced to Community Edition:**
- Core N8N_Builder functionality
- Web interface and API
- Documentation (sanitized)
- Configuration files (_community versions)
- Scripts and utilities (public-safe)

#### **❌ Stays Private (Never Synced):**
- Enterprise_Module/ folder and components
- Enterprise_Database/ folder and components
- Private configuration files
- Development notes with sensitive information
- Any file containing proprietary algorithms

## 🔧 **VS Code Integration**

### **Available Tasks**
Access via `Ctrl+Shift+P` → "Tasks: Run Task":

1. **"Run N8N Builder"**: Start the application
2. **"Commit and Sync Community"**: Main development workflow
3. **"Sync Community Only"**: Manual sync to GitHub

### **Task Configuration**
Tasks are defined in `.vscode/tasks.json` and can be customized as needed.

## 📝 **Commit Message Guidelines**

### **Main Repository Commits**
- **Purpose**: Internal development tracking
- **Style**: Detailed, technical, can reference private components
- **Examples**:
  - "Fix authentication bug in workflow generator and update Enterprise Module error handling"
  - "Add new Enterprise_Database integration for improved solution caching"
  - "Refactor optional integrations to support new Enterprise Module features"

### **Community Repository Commits**
- **Purpose**: Public changelog, user-facing
- **Style**: Clean, professional, no private component references
- **Examples**:
  - "Fix authentication bug in workflow generator"
  - "Improve error handling and retry mechanisms"
  - "Enhance optional integrations for better extensibility"

## 🔍 **Troubleshooting**

### **Common Issues**

#### **"No changes to commit"**
- **Cause**: No uncommitted changes in main repository
- **Solution**: Make changes first, or use "Sync Community Only" if needed

#### **"sync-public.ps1 not found"**
- **Cause**: Separation system not properly set up
- **Solution**: Ensure sync-public.ps1 exists in root directory

#### **"Failed to push to GitHub"**
- **Cause**: Network issues or authentication problems
- **Solution**: Check internet connection and GitHub credentials

#### **"Community sync failed"**
- **Cause**: Issues with separation process
- **Solution**: Check N8N_Builder_Community folder exists and has proper git configuration

### **Manual Recovery**

If automation fails, you can manually execute the workflow:

```powershell
# 1. Commit to main repository
git add .
git commit -m "Your commit message"

# 2. Sync to community
.\sync-public.ps1 -PublicRepoPath "..\N8N_Builder_Community" -Force

# 3. Push to GitHub
cd ..\N8N_Builder_Community
git add .
git commit -m "Community update message"
git push origin master
cd ..\N8N_Builder
```

## 📚 **Related Documentation**

- **[README.md](../README.md)**: Project overview and quick start
- **[Architecture.md](Architecture.md)**: Technical architecture details
- **[API_Reference.md](api/API_Reference.md)**: API reference
- **[Troubleshooting.md](guides/Troubleshooting.md)**: General troubleshooting guide

## 🤝 **Team Development**

### **For New Developers**

1. **Clone main repository**: `git clone <private-repo-url>` (when available)
2. **Set up environment**: Follow README.md setup instructions
3. **Install VS Code tasks**: Tasks are included in repository
4. **Test workflow**: Make a small change and run "Commit and Sync Community"

### **Best Practices**

- **Always work in main N8N_Builder workspace**
- **Use descriptive commit messages for both repositories**
- **Test changes before committing**
- **Sync to community regularly to keep public repo current**
- **Never manually edit N8N_Builder_Community** (it's auto-generated)

## 🔄 **Workflow Summary**

```
Developer Workflow:
1. Work in N8N_Builder (main workspace)
2. Ctrl+Shift+P → "Tasks: Run Task" → "Commit and Sync Community"
3. Enter main commit message (detailed, internal)
4. Enter community message (clean, public) or skip
5. Continue development

Result:
✅ Main repository: All changes committed locally
✅ Community repository: Safe changes synced to GitHub
✅ Private components: Protected and never exposed
```

---

**🎉 Ready to develop!** This workflow ensures your private components stay secure while maintaining a professional public repository for the community.
