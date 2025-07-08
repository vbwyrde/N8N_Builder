# Legacy Tunneling Solutions

## 📁 What's in this folder?

This folder contains the **legacy tunneling solutions** that were used before the **Stable URL Proxy** was implemented.

### Files Moved Here:
- `Start-N8N-NgRok.ps1` - Old ngrok startup script
- `Stop-N8N-NgRok.ps1` - Old ngrok stop script  
- `Start-N8N-Zrok*.ps1` - Zrok startup scripts
- `Stop-N8N-Zrok.ps1` - Zrok stop script
- `Setup-Zrok*.ps1` - Zrok setup scripts
- `docker-compose.zrok*.yml` - Zrok Docker configurations
- `ZROK_SETUP_GUIDE.md` - Zrok setup documentation

## 🎯 Why were these replaced?

### Problems with ngrok/zrok:
- ❌ **URL changes every restart** - Required updating OAuth apps constantly
- ❌ **Manual credential management** - Had to update webhook URLs manually
- ❌ **External dependencies** - Relied on third-party services
- ❌ **Complex setup** - Multiple configuration steps required

### New Stable URL Solution:
- ✅ **URL never changes** - http://localhost:8080 is permanent
- ✅ **Zero maintenance** - Set once, works forever
- ✅ **No external dependencies** - Pure Docker/nginx solution
- ✅ **Simple setup** - Just run `.\start-n8n.bat`

## 🔄 Migration Complete

The main n8n-docker system now uses:
- **Primary startup**: `.\start-n8n.bat` → `Start-N8N-Stable.ps1`
- **Primary stop**: `.\stop-n8n.bat` → `Stop-N8N-Stable-Fixed.ps1`
- **Stable webhook URL**: http://localhost:8080 (never changes!)

## 📚 When to use legacy files?

These files are kept for:
- **Reference purposes** - Understanding the old approach
- **Fallback scenarios** - If stable URL doesn't work in specific environments
- **Learning** - Comparing different tunneling approaches

## ⚠️ Important Notes

- These legacy scripts are **not maintained** and may not work with current configurations
- The `.env` file has been updated for stable URL - legacy scripts may need manual configuration
- **Recommended**: Use the new stable URL solution unless you have specific requirements

---
*Legacy files preserved for reference. Use the new stable URL solution for production.*
