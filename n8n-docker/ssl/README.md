# SSL Certificates Directory

Place your SSL certificates in this directory for HTTPS support.

## Required Files

For HTTPS to work, you need:
- `privkey.pem` - Private key file
- `fullchain.pem` - Full certificate chain

## Getting SSL Certificates

### Option 1: Let's Encrypt (Free)
```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d yourdomain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem ./ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem ./ssl/
```

### Option 2: Self-Signed (Development Only)
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout privkey.pem -out fullchain.pem -days 365 -nodes
```

## Configuration

After placing certificates, update your `.env` file:
```
N8N_PROTOCOL=https
N8N_SSL_KEY=/etc/ssl/certs/privkey.pem
N8N_SSL_CERT=/etc/ssl/certs/fullchain.pem
```

Then restart n8n:
```bash
docker-compose restart n8n
```

## Security Notes

- Never commit actual certificate files to git
- Use strong passwords for certificate generation
- Regularly renew certificates (Let's Encrypt expires every 90 days)
- Consider using a reverse proxy (nginx, traefik) for production
