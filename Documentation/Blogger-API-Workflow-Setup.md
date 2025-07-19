# Blogger API Workflow Setup Guide

## Overview

This guide explains how to set up the improved ElthosRPG Blog to Twitter workflow that uses the Blogger API instead of web scraping for more reliable blog post retrieval.

## Benefits of Using Blogger API

- **Reliability**: No dependency on HTML structure changes
- **Structured Data**: Get post metadata, titles, dates, etc.
- **Better Performance**: Direct API calls are faster than scraping
- **Error Handling**: Clear API error responses
- **Rate Limiting**: Built-in API rate limiting protection

## Prerequisites

1. **N8N Docker Environment**: Running with LocalTunnel or nGrok
2. **Google Cloud Console Access**: For OAuth2 credentials
3. **Blogger Blog**: Your existing Elthos RPG blog
4. **Local AI Model**: LM Studio with mimo-vl-7b-rl model

## Step 1: Set Up Blogger API Credentials

### 1.1 Run the Setup Script
```powershell
.\n8n-docker\scripts\setup-blogger-credentials.ps1
```

### 1.2 Manual Setup (if needed)
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable the Blogger API v3
4. Create OAuth2 credentials
5. Add your N8N callback URL: `https://your-tunnel-url.com/rest/oauth2-credential/callback`

### 1.3 Configure N8N Credentials
1. Open N8N interface
2. Go to Settings → Credentials
3. Add new credential: "Google OAuth2 API"
4. Enter Client ID and Client Secret
5. Add scopes:
   - `https://www.googleapis.com/auth/blogger`
   - `https://www.googleapis.com/auth/blogger.readonly`
6. Complete OAuth authorization

## Step 2: Find Your Blog ID

### 2.1 Run the Helper Script
```powershell
.\Scripts\get-blogger-blog-id.ps1
```

### 2.2 Using Blogger API (Recommended)
1. Create test workflow in N8N
2. Add HTTP Request node:
   - Method: GET
   - URL: `https://www.googleapis.com/blogger/v3/users/self/blogs`
   - Authentication: Your Google OAuth2 credential
3. Execute and find your blog's `id` field

### 2.3 From Blogger Dashboard
1. Go to [Blogger.com](https://www.blogger.com/)
2. Select your Elthos RPG blog
3. Look at URL: `https://www.blogger.com/blogger.g?blogID=YOUR_BLOG_ID`
4. Copy the long numeric ID

## Step 3: Configure the Workflow

### 3.1 Import the New Workflow
The updated workflow is located at:
```
projects/elthosdb1/ElthosRPG_Blog_Twitter_BloggerAPI.json
```

### 3.2 Update Configuration
1. **Set Blog ID Node**: Replace `YOUR_BLOG_ID_HERE` with your actual Blog ID
2. **Get Blog Posts via API Node**: Update the credential ID to match your OAuth2 credential
3. **Test the API Connection**: Execute the "Get Blog Posts via API" node

### 3.3 Workflow Structure
```
Manual Trigger → Set Blog ID → Get Blog Posts via API → Extract Post URLs from API → Random Selection → Fetch Post → Edit Field - blogURL → ScrapeNinja → Code - Get Paragraph 1 → Basic LLM Chain → Code - Clean for Tweet → Create Tweet
```

## Step 4: Key Workflow Changes

### 4.1 Replaced Nodes
- **Old**: `Fetch Blog Page` + `Scrape Blog Page` + `Extract Post URLs`
- **New**: `Get Blog Posts via API` + `Extract Post URLs from API`

### 4.2 New API Parameters
```json
{
  "url": "https://www.googleapis.com/blogger/v3/blogs/{{ $json.blogId }}/posts",
  "queryParameters": {
    "maxResults": "50",
    "status": "LIVE",
    "orderBy": "published"
  }
}
```

### 4.3 Enhanced Error Handling
The new workflow includes better error handling for:
- Empty API responses
- Invalid Blog IDs
- Authentication failures
- Network timeouts

## Step 5: Testing the Workflow

### 5.1 Test Individual Nodes
1. **Set Blog ID**: Verify your Blog ID is set correctly
2. **Get Blog Posts via API**: Should return JSON with posts array
3. **Extract Post URLs from API**: Should extract URLs from API response
4. **Random Selection**: Should select a random post URL

### 5.2 Full Workflow Test
1. Execute the complete workflow
2. Monitor console logs for debugging information
3. Verify the final tweet is posted to Twitter

### 5.3 Expected API Response Structure
```json
{
  "kind": "blogger#postList",
  "items": [
    {
      "kind": "blogger#post",
      "id": "post-id",
      "blog": { "id": "blog-id" },
      "published": "2025-01-01T00:00:00.000Z",
      "updated": "2025-01-01T00:00:00.000Z",
      "url": "https://elthosrpg.blogspot.com/2025/01/post-title.html",
      "title": "Post Title",
      "content": "Post content..."
    }
  ]
}
```

## Step 6: Troubleshooting

### 6.1 Common Issues
- **401 Unauthorized**: Check OAuth2 credentials and scopes
- **403 Forbidden**: Verify Blogger API is enabled in Google Cloud Console
- **404 Not Found**: Check Blog ID is correct
- **Empty Response**: Blog might have no published posts

### 6.2 Debug Tips
- Check N8N execution logs
- Test API endpoints in OAuth2 Playground
- Verify Blog ID using the helper script
- Ensure LocalTunnel/nGrok is running for OAuth callbacks

### 6.3 Fallback Options
If API fails, the workflow can fall back to:
- Hardcoded post URLs for testing
- Previous scraping method (temporarily)
- Manual post selection

## Step 7: Advanced Configuration

### 7.1 API Parameters
Customize the API request:
- `maxResults`: Number of posts to retrieve (1-500)
- `status`: `LIVE`, `DRAFT`, or `SCHEDULED`
- `orderBy`: `published`, `updated`
- `startDate`/`endDate`: Filter by date range

### 7.2 Post Filtering
Add custom filtering in the "Extract Post URLs from API" node:
- Filter by date range
- Exclude certain post types
- Prioritize recent posts

### 7.3 Metadata Usage
The API provides rich metadata you can use:
- Post titles for better tweet content
- Publication dates for context
- Post labels/tags for hashtag generation
- Author information

## Conclusion

The new Blogger API workflow provides a more reliable and maintainable solution for automatically selecting blog posts for Twitter promotion. The structured API data enables better content processing and reduces the risk of failures due to website changes.

For support or questions, refer to the troubleshooting section or check the N8N execution logs for detailed error information.
