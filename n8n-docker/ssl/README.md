# 🔐 SSL Certificates Directory

This directory is for SSL certificates to enable HTTPS support for your n8n instance.

**⚠️ IMPORTANT**: For development with nGrok, SSL certificates are NOT needed as nGrok provides HTTPS termination.

## 🎯 When You Need SSL Certificates

### ✅ Use SSL Certificates When:
- Running n8n in production without nGrok
- Exposing n8n directly to the internet
- Using a reverse proxy (nginx, traefik)
- Corporate environments requiring HTTPS

### ❌ Skip SSL Certificates When:
- Using nGrok for development (nGrok handles HTTPS)
- Running locally only (http://localhost:5678)
- Testing and development workflows

## 📁 Required Files

For HTTPS to work, place these files in this directory:
- **`privkey.pem`** - Private key file (⚠️ **NEVER commit to git**)
- **`fullchain.pem`** - Full certificate chain
- **`cert.pem`** - Certificate file (optional, usually included in fullchain)

## 🔑 Getting SSL Certificates

### 🆓 Option 1: Let's Encrypt (Free, Recommended)
```bash
# Install certbot (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install certbot

# Get certificate for your domain
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates to ssl directory
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/

# Set proper permissions
sudo chown $USER:$USER ./ssl/*.pem
chmod 600 ./ssl/privkey.pem
chmod 644 ./ssl/fullchain.pem
```

### 🧪 Option 2: Self-Signed (Development Only)
```bash
# Generate self-signed certificate (valid for 365 days)
openssl req -x509 -newkey rsa:4096 -keyout privkey.pem -out fullchain.pem -days 365 -nodes

# You'll be prompted for certificate details:
# Country Name: US
# State: Your State
# City: Your City
# Organization: Your Organization
# Organizational Unit: IT Department
# Common Name: yourdomain.com (IMPORTANT: must match your domain)
# Email: your-email@domain.com
```

### 💰 Option 3: Commercial Certificate
- Purchase from providers like DigiCert, Comodo, GoDaddy
- Follow provider's instructions for domain validation
- Download certificate files and place in ssl/ directory

## ⚙️ Configuration

### Step 1: Place Certificates
Ensure these files exist in the ssl/ directory:
```
ssl/
├── privkey.pem     # Private key (600 permissions)
├── fullchain.pem   # Certificate chain (644 permissions)
└── README.md       # This file
```

### Step 2: Update Environment Configuration
Edit your `.env` file:
```bash
# Change protocol to HTTPS
N8N_PROTOCOL=https

# Set certificate paths (these paths are inside the Docker container)
N8N_SSL_KEY=/etc/ssl/certs/privkey.pem
N8N_SSL_CERT=/etc/ssl/certs/fullchain.pem

# Optional: Set HTTPS port (default is 443, but n8n uses 5678)
N8N_PORT=5678
```

### Step 3: Restart n8n
```bash
# Restart to apply SSL configuration
docker-compose restart n8n

# Verify HTTPS is working
curl -k https://localhost:5678
```

## 🔒 Security Best Practices

### 🚫 Critical Security Rules
- **NEVER commit certificate files to git** (they're in .gitignore)
- **NEVER share private keys** via email, chat, or public channels
- **Use strong passwords** for certificate generation
- **Set proper file permissions**: 600 for private keys, 644 for certificates

### 🔄 Certificate Maintenance
- **Let's Encrypt**: Renew every 90 days (set up auto-renewal)
- **Commercial**: Renew before expiration (usually 1-2 years)
- **Self-signed**: Regenerate before expiration

### 🛡️ Additional Security
```bash
# Set up automatic Let's Encrypt renewal
sudo crontab -e
# Add this line for monthly renewal:
0 0 1 * * /usr/bin/certbot renew --quiet

# Monitor certificate expiration
openssl x509 -in ./ssl/fullchain.pem -text -noout | grep "Not After"
```

## 🔧 Troubleshooting

### Common Issues:

**Certificate not found:**
```bash
# Check file exists and permissions
ls -la ssl/
# Should show privkey.pem (600) and fullchain.pem (644)
```

**Permission denied:**
```bash
# Fix permissions
chmod 600 ssl/privkey.pem
chmod 644 ssl/fullchain.pem
```

**Browser security warnings:**
- Self-signed certificates will show warnings (normal)
- Click "Advanced" → "Proceed to localhost" for testing
- Use proper domain certificates for production

**n8n won't start with SSL:**
```bash
# Check n8n logs for SSL errors
docker logs n8n-dev --tail 20

# Common issues:
# - Wrong file paths in .env
# - Incorrect file permissions
# - Malformed certificate files
```

## 🌐 Integration with nGrok

**For development with nGrok:**
- Keep `N8N_PROTOCOL=http` in .env
- nGrok provides HTTPS termination automatically
- No SSL certificates needed in this directory
- nGrok URL will be https://your-tunnel.ngrok-free.app

**For production without nGrok:**
- Set `N8N_PROTOCOL=https` in .env
- Place SSL certificates in this directory
- Configure domain to point to your server
- Set up proper firewall rules

---

**📖 Related Documentation:**
- **[Security Guide](../Documentation/SECURITY.md)** - Complete security practices
- **[Main README](../Documentation/README.md)** - Full setup guide
- **[Credentials Setup](../Documentation/CREDENTIALS_SETUP.md)** - External service integration
