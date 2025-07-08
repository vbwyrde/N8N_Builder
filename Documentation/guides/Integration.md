# 🔗 Integration Setup Guide

**🎯 Goal**: Connect N8N_Builder workflows with external services (15 minutes)

## What You'll Learn

- Connect workflows to Gmail, Google Drive, Slack, Twitter, and more
- Setup webhook endpoints for external triggers
- Configure credentials securely
- Test integrations end-to-end

## Prerequisites

- ✅ N8N_Builder and n8n-docker running
- ✅ Completed [Getting Started Guide](../../GETTING_STARTED.md)
- ✅ External service accounts (Gmail, Slack, etc.)

## Common Integrations

### 📧 Email Integration (Gmail)

#### Generate Email Workflow
In N8N_Builder, describe:
```
Create a workflow that sends an email notification to john@example.com 
when a webhook is triggered. Include the webhook data in the email body.
```

#### Configure Gmail in n8n
1. **Open n8n**: http://localhost:5678
2. **Import** the generated workflow
3. **Click Gmail node** → Configure credentials
4. **Add Gmail OAuth2**:
   - Client ID: From Google Cloud Console
   - Client Secret: From Google Cloud Console
   - Authorize with your Gmail account

#### Test the Integration
1. **Activate** the workflow
2. **Find webhook URL** in the Webhook node
3. **Test with curl**:
   ```bash
   curl -X POST "your-webhook-url" \
     -H "Content-Type: application/json" \
     -d '{"message": "Test notification", "priority": "high"}'
   ```
4. **Check email** - Should receive notification

### 💬 Slack Integration

#### Generate Slack Workflow
```
Create a workflow that posts a message to #general channel in Slack 
when a file is uploaded to a monitored folder. Include the filename 
and upload timestamp.
```

#### Configure Slack in n8n
1. **Import workflow** from N8N_Builder
2. **Click Slack node** → Configure credentials
3. **Create Slack App**:
   - Go to https://api.slack.com/apps
   - Create new app for your workspace
   - Get Bot User OAuth Token
4. **Add token** to n8n Slack credentials

#### Test File Upload Trigger
1. **Create test folder**: `mkdir data/uploads`
2. **Activate workflow**
3. **Add test file**: `echo "test" > data/uploads/test.txt`
4. **Check Slack** - Should see message in #general

### 🌐 Webhook Integrations

#### Setup nGrok for External Access
```bash
# Install nGrok (if not already installed)
# Download from https://ngrok.com/download

# Start tunnel to n8n
ngrok http 5678
```

#### Get Public Webhook URL
1. **Open nGrok dashboard**: http://127.0.0.1:4040
2. **Copy HTTPS URL** (e.g., https://abc123.ngrok.io)
3. **Your webhook endpoints** will be:
   - `https://abc123.ngrok.io/webhook/your-webhook-path`

#### Configure External Services
Update webhook URLs in external services:
- **GitHub**: Repository → Settings → Webhooks
- **Stripe**: Dashboard → Webhooks
- **Zapier**: Use nGrok URL as webhook destination

## Advanced Integration Patterns

### Multi-Service Workflow
Generate complex integrations:
```
Create a workflow that:
1. Monitors Google Drive for new files
2. When a PDF is added, extract text content
3. Send the text to OpenAI for summarization
4. Post the summary to Slack
5. Save the summary to a database
```

### Conditional Logic
Add smart routing:
```
Create a workflow that processes incoming webhooks differently:
- If priority is "high", send SMS and email
- If priority is "medium", send email only
- If priority is "low", just log to database
```

### Data Transformation
Handle complex data:
```
Create a workflow that:
1. Receives CSV data via webhook
2. Converts CSV to JSON format
3. Validates required fields
4. Sends valid records to CRM
5. Sends invalid records to error queue
```

## Security Best Practices

### Credential Management
- **Never hardcode** API keys in workflows
- **Use n8n credentials** system for secure storage
- **Rotate keys** regularly
- **Use environment variables** for sensitive data

### Webhook Security
- **Use HTTPS** endpoints (nGrok provides this)
- **Validate webhook signatures** when possible
- **Implement rate limiting** for public endpoints
- **Monitor webhook logs** for suspicious activity

### Network Security
- **Use nGrok paid plan** for production (custom domains, auth)
- **Implement IP whitelisting** where supported
- **Use VPN** for internal service connections
- **Monitor access logs** regularly

## Troubleshooting Integrations

### Common Issues

**"Credentials not working"**
- Verify API keys are correct and active
- Check service-specific permission scopes
- Ensure OAuth tokens haven't expired
- Test credentials outside of n8n first

**"Webhooks not triggering"**
- Verify nGrok tunnel is active
- Check webhook URL format
- Confirm external service is sending requests
- Review n8n execution logs

**"Data not flowing between nodes"**
- Check node connections (lines between nodes)
- Verify data mapping expressions
- Use manual execution to debug data flow
- Check for required field mismatches

### Debug Tools

**Test Webhook Endpoints**
```bash
# Test your webhook
curl -X POST "https://your-ngrok-url.ngrok.io/webhook/test" \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

**Check n8n Logs**
```bash
# View n8n container logs
docker logs n8n-dev -f

# Check specific execution
# Go to n8n → Executions tab → Click failed execution
```

**Monitor nGrok Traffic**
- Open: http://127.0.0.1:4040
- View all incoming requests and responses
- Debug webhook payload issues

## Next Steps

### More Complex Integrations
- **[Technical Specifications](../technical/Specifications.md)** - Detailed system specifications
- **[Architecture Overview](../Architecture.md)** - System design and components

### Service-Specific Guides
- **Google Workspace**: Drive, Sheets, Calendar integration
- **Microsoft 365**: Outlook, Teams, SharePoint
- **CRM Systems**: Salesforce, HubSpot, Pipedrive
- **E-commerce**: Shopify, WooCommerce, Stripe

---

**🎉 Congratulations!** You can now connect N8N_Builder workflows to external services. Your automations can now interact with the real world!

**Next**: Review [Technical Specifications](../technical/Specifications.md) for detailed system requirements and configuration options.
