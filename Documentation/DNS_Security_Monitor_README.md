# DNS Security Monitor

A comprehensive DNS security monitoring system built with N8N that analyzes your Windows DNS cache for potential security threats and generates detailed HTML reports.

## 🎯 Overview

The DNS Security Monitor automatically:
- Collects Windows DNS cache data every 60 minutes (synchronized with N8N)
- Maintains historical domain tracking with occurrence counts and timestamps
- Analyzes domains for security threats using pattern-based detection
- Generates professional HTML security reports with historical context
- Creates alerts for high-risk domains
- Provides a web dashboard for easy access to reports and domain history

## 📁 Project Structure

```
N8N_Builder/
├── data/dns_reports/                    # Main reports directory
│   ├── index.html                       # Web dashboard
│   ├── dns_security_report_*.html       # Generated security reports
│   ├── DNS_SECURITY_ALERT_*.txt        # High-risk domain alerts
│   └── setup/                          # Configuration & setup files
│       ├── README.md                   # Setup documentation
│       ├── dns_cache_output.txt        # Raw DNS cache data
│       ├── dns_cache_metadata.json     # Collection metadata
│       ├── dns_domain_history.csv      # Historical domain tracking (flat file)
│       ├── dns_domain_history_format.json # Format specification
│       └── dns_domain_history_schema.sql  # Optional SQL Server integration
├── Scripts/                            # Automation scripts
│   ├── setup_dns_monitoring.ps1       # Main setup script
│   ├── get_dns_cache.ps1              # DNS cache collector
│   ├── setup_dns_automation.ps1       # Task scheduler setup
│   └── dns_cache_loop.ps1             # Continuous collection loop
└── data/dns_reports/setup/dns_security_workflow_fixed.json # N8N workflow definition
```

## 🚀 Quick Start

### 1. Prerequisites
- Windows 10/11 with PowerShell
- N8N running in Docker (localhost:5678)
- Docker volume mount: `../data:/home/node/shared`

### 2. Setup (One Command)
```powershell
# Run from N8N_Builder root directory
.\data\dns_reports\setup\setup_dns_monitoring.ps1
```

Choose **Option 1** for automated Windows Task Scheduler setup.

### 3. Import N8N Workflow
1. Open N8N at http://localhost:5678
2. Import workflow: `data/dns_reports/setup/dns_security_workflow_fixed.json`
3. The workflow will run automatically every 60 minutes

### 4. Access Dashboard
Open `data/dns_reports/index.html` in your browser to view:
- Latest security reports
- Alert summaries
- Direct links to detailed reports

## 🔧 How It Works

### Data Collection
1. **PowerShell Script** runs `ipconfig /displaydns` every 60 minutes (5 minutes before N8N)
2. **Raw DNS data** saved to `data/dns_reports/setup/dns_cache_output.txt`
3. **Domain history** updated in `data/dns_reports/setup/dns_domain_history.csv`
4. **Metadata** (timestamp, file size) saved alongside

### N8N Processing
1. **Read DNS File** node loads the raw DNS cache data
2. **Parse DNS Domains** extracts unique domain names
3. **Update Domain History** tracks domain occurrences and timestamps
4. **Security Analysis** checks domains against threat patterns with historical context
5. **Report Generation** creates professional HTML reports with trend analysis
6. **Alert Creation** generates alert files for high-risk domains

### Security Detection
- **High-Risk Patterns**: malware, phish, hack, virus, spam, scam, fraud
- **Medium-Risk Patterns**: test, temp, demo, long domain names, excessive subdomains
- **Whitelist**: Known good domains (google.com, microsoft.com, etc.)
- **Scoring System**: Threat score based on multiple factors

## 📊 Reports & Alerts

### HTML Security Reports
- **Professional styling** with responsive design
- **Risk level summaries** (High/Medium/Low)
- **Detailed domain analysis** with threat descriptions
- **Security scores** and threat categorization
- **Timestamp and metadata** for audit trails

### Security Alerts
- **High-risk domain detection** triggers immediate alerts
- **Text file alerts** with detailed threat information
- **Windows notifications** (simulated in N8N logs)
- **Dashboard integration** for quick access

## ⚙️ Configuration Options

### Automation Methods

#### Windows Task Scheduler (Recommended)
```powershell
.\data\dns_reports\setup\setup_dns_automation.ps1
```
- Runs every 60 minutes automatically (synchronized with N8N)
- Starts with Windows boot
- Background operation
- No manual intervention required

#### Continuous Loop Script
```powershell
.\data\dns_reports\setup\dns_cache_loop.ps1
```
- Runs in PowerShell window
- Good for testing and monitoring
- Manual start/stop control

#### Manual Collection
```powershell
.\Scripts\get_dns_cache.ps1
```
- On-demand DNS cache collection and domain history update
- Full control over timing
- Good for troubleshooting

### Management Commands
```powershell
# Check automation status
.\data\dns_reports\setup\setup_dns_automation.ps1 -Status

# Remove automation
.\data\dns_reports\setup\setup_dns_automation.ps1 -Remove

# Setup directories and permissions
.\data\dns_reports\setup\create_dns_reports_directory.ps1

# Query domain history
.\data\dns_reports\setup\query_domain_history.ps1 -Query summary
.\data\dns_reports\setup\query_domain_history.ps1 -Query recent -Days 7
.\data\dns_reports\setup\query_domain_history.ps1 -Query highrisk
```

## 🛠️ Troubleshooting

### Common Issues

#### "DNS cache file not found"
- Run: `.\Scripts\get_dns_cache.ps1`
- Check: `data/dns_reports/setup/dns_cache_output.txt` exists
- Verify: PowerShell execution policy allows scripts

#### "N8N workflow fails"
- Verify: Docker volume mount working (`../data:/home/node/shared`)
- Check: File path in Read DNS File node
- Ensure: dns_reports/setup directory exists

#### "Permission denied errors"
- Run: `.\Scripts\fix_permissions.ps1`
- Check: Docker container can access shared directory
- Verify: File ownership (node:node in container)

### Debug Steps
1. **Test DNS collection**: `.\Scripts\get_dns_cache.ps1`
2. **Check file creation**: Verify files in `data/dns_reports/setup/`
3. **Test N8N workflow**: Run manually and check console logs
4. **Verify dashboard**: Open `data/dns_reports/index.html`

## 🎯 Features

### Security Monitoring
- **Real-time DNS analysis** of your browsing activity
- **Pattern-based threat detection** for malicious domains
- **Automated alerting** for high-risk domains
- **Historical reporting** with timestamp tracking

### Professional Reporting
- **HTML dashboard** with modern, responsive design
- **Detailed security reports** with risk categorization and historical trends
- **Alert management** with file-based notifications
- **Domain history tracking** with occurrence counts and timeline analysis
- **Easy access** via web browser

### Domain History Tracking
- **Flat file format** (CSV) for maximum portability and compatibility
- **Historical timeline** tracking first seen, last seen, and occurrence counts
- **Risk level evolution** monitoring how domain threat levels change over time
- **Query tools** for analyzing domain patterns and trends
- **Export capabilities** for integration with Excel, SQL Server, or data analysis tools
- **No database required** - works on any Windows system

### Automation & Integration
- **Windows Task Scheduler** integration
- **N8N workflow automation** every 60 minutes
- **Docker containerization** for N8N processing
- **PowerShell scripting** for Windows DNS access

## 📞 Support

For setup assistance or troubleshooting:
1. Review this README and setup documentation
2. Check `data/dns_reports/setup/README.md` for detailed setup steps
3. Verify PowerShell script execution and N8N workflow logs
4. Ensure Docker volume mounts and permissions are correct

## 🔄 Updates & Maintenance

The system is designed for minimal maintenance:
- **Automated data collection** every 60 minutes (synchronized)
- **Self-contained reporting** with no external dependencies
- **Error handling** with fallback to mock data if needed
- **Log rotation** prevents large file accumulation

Regular monitoring via the dashboard ensures ongoing security awareness of your DNS activity.
