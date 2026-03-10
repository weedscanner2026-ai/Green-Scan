# Green Scan - Online Deployment Guide

## Overview
This guide will help you deploy the Green Scan backend server online so users can access it from anywhere. The Android app will connect to your online server instead of localhost.

---

## Deployment Options

### Option 1: PythonAnywhere (Recommended for Students - FREE)
**Best for:** College projects, testing, small-scale deployment
**Cost:** Free tier available
**Pros:** Easy setup, no credit card required, Python-friendly
**Cons:** Limited resources on free tier

### Option 2: Heroku
**Best for:** Production-ready apps
**Cost:** Free tier discontinued, paid plans start at $5/month
**Pros:** Easy deployment, good documentation
**Cons:** Requires credit card

### Option 3: Railway.app
**Best for:** Modern deployment
**Cost:** Free $5 credit monthly, then pay-as-you-go
**Pros:** Easy setup, modern interface
**Cons:** Requires credit card after trial

### Option 4: Render
**Best for:** Free tier with good features
**Cost:** Free tier available
**Pros:** Easy deployment, good free tier
**Cons:** Free tier has limitations

### Option 5: DigitalOcean / AWS / Google Cloud
**Best for:** Full control, scalability
**Cost:** Starting from $5-10/month
**Pros:** Full control, scalable
**Cons:** More complex setup, requires server management

---

## OPTION 1: PythonAnywhere Deployment (RECOMMENDED)

### Step 1: Prepare Your Project

1. **Create a requirements.txt file** (if not exists):
```bash
pip freeze > requirements.txt
```

2. **Update unified_admin_server.py** for production:
   - Change debug mode to False
   - Add proper host configuration

### Step 2: Sign Up for PythonAnywhere

1. Go to https://www.pythonanywhere.com
2. Click "Start running Python online in less than a minute!"
3. Create a free account (Beginner account)
4. Verify your email

### Step 3: Upload Your Files

1. Go to **Files** tab
2. Create a new directory: `greenscan`
3. Upload these files:
   - `unified_admin_server.py`
   - `requirements.txt`
   - `weed_info.json`
   - `model_version.json`
   - All folders: `admin_templates/`, `static/`, `models/`
   - `users.db` (or create new)

### Step 4: Install Dependencies

1. Go to **Consoles** tab
2. Start a **Bash console**
3. Run these commands:
```bash
cd greenscan
pip3.10 install --user flask flask-cors pillow tensorflow
```

### Step 5: Create Web App

1. Go to **Web** tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select "Python 3.10"
5. Click through the setup

### Step 6: Configure WSGI File

1. In the **Web** tab, find "Code" section
2. Click on the WSGI configuration file link
3. Replace contents with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/greenscan'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['FLASK_APP'] = 'unified_admin_server.py'

# Import Flask app
from unified_admin_server import app as application
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

### Step 7: Configure Static Files

In the **Web** tab, under "Static files":
- URL: `/static/`
- Directory: `/home/YOUR_USERNAME/greenscan/static/`

### Step 8: Reload Web App

1. Scroll to top of **Web** tab
2. Click the green "Reload" button
3. Your app will be available at: `https://YOUR_USERNAME.pythonanywhere.com`

### Step 9: Update Android App

Update `ApiConfig.java`:
```java
public class ApiConfig {
    // Change this to your PythonAnywhere URL
    public static final String BASE_URL = "https://YOUR_USERNAME.pythonanywhere.com";
}
```

Rebuild and install the APK.

---

## OPTION 2: Railway.app Deployment

### Step 1: Prepare Project

1. **Create `railway.json`**:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python unified_admin_server.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

2. **Update `unified_admin_server.py`**:
```python
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
```

### Step 2: Deploy to Railway

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Connect your GitHub account
6. Push your code to GitHub
7. Select the repository
8. Railway will auto-detect Python and deploy

### Step 3: Get Your URL

1. Go to your project settings
2. Click "Generate Domain"
3. Copy the URL (e.g., `https://your-app.railway.app`)

### Step 4: Update Android App

Update `ApiConfig.java` with your Railway URL.

---

## OPTION 3: Render Deployment

### Step 1: Prepare Files

1. **Create `render.yaml`**:
```yaml
services:
  - type: web
    name: greenscan
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python unified_admin_server.py
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

2. **Update server to use PORT environment variable**

### Step 2: Deploy

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your repository
5. Configure:
   - Name: greenscan
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python unified_admin_server.py`
6. Click "Create Web Service"

---

## Production-Ready Server Configuration

Update `unified_admin_server.py` for production:

```python
import os

# ... existing code ...

if __name__ == '__main__':
    # Get port from environment variable (for cloud platforms)
    port = int(os.environ.get('PORT', 5000))
    
    # Get host from environment variable
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Disable debug in production
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
```

---

## Security Considerations for Production

### 1. Environment Variables
Create `.env` file for sensitive data:
```
SECRET_KEY=your-secret-key-here
ADMIN_PASSWORD=your-admin-password
DATABASE_URL=your-database-url
```

### 2. HTTPS/SSL
- Most platforms provide free SSL certificates
- Ensure all API calls use HTTPS

### 3. Database
- Use PostgreSQL or MySQL instead of SQLite for production
- Enable database backups

### 4. CORS Configuration
Update CORS settings:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://yourdomain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### 5. Rate Limiting
Add rate limiting to prevent abuse:
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

---

## Android App Configuration

### Update ApiConfig.java

```java
package com.example.weeddetector;

public class ApiConfig {
    // PRODUCTION URL - Update this after deployment
    public static final String BASE_URL = "https://your-domain.com";
    
    // API Endpoints
    public static final String REGISTER_URL = BASE_URL + "/register";
    public static final String LOGIN_URL = BASE_URL + "/login";
    public static final String MODEL_VERSION_URL = BASE_URL + "/model/version";
    public static final String MODEL_DOWNLOAD_URL = BASE_URL + "/model/download/model";
    public static final String LABELS_DOWNLOAD_URL = BASE_URL + "/model/download/labels";
    public static final String INFO_DOWNLOAD_URL = BASE_URL + "/model/download/info";
}
```

### Rebuild APK

1. Open Android Studio
2. Build → Clean Project
3. Build → Rebuild Project
4. Build → Build Bundle(s) / APK(s) → Build APK(s)
5. Distribute the new APK to users

---

## Testing Your Deployment

### 1. Test Admin Panel
- Visit: `https://your-domain.com/admin`
- Login with admin credentials
- Check all features work

### 2. Test API Endpoints
```bash
# Test registration
curl -X POST https://your-domain.com/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test123","fullName":"Test User","userType":"Farmer"}'

# Test model version
curl https://your-domain.com/model/version
```

### 3. Test Android App
- Install new APK
- Register new user
- Login
- Test weed detection
- Check model updates

---

## Monitoring & Maintenance

### 1. Check Logs
- PythonAnywhere: Web tab → Log files
- Railway: Project → Deployments → Logs
- Render: Dashboard → Logs

### 2. Monitor Usage
- Check server resources
- Monitor API response times
- Track user registrations

### 3. Backup Database
```bash
# Backup users.db regularly
cp users.db users_backup_$(date +%Y%m%d).db
```

### 4. Update Model
1. Train new model locally
2. Upload to server
3. Update model_version.json
4. Users will auto-download update

---

## Cost Estimates

### Free Tier Options:
- **PythonAnywhere Free**: Good for 100-500 users/day
- **Render Free**: 750 hours/month, sleeps after inactivity
- **Railway Free**: $5 credit/month

### Paid Options (if needed):
- **PythonAnywhere Hacker**: $5/month
- **Railway Pro**: ~$5-20/month based on usage
- **Render Starter**: $7/month
- **DigitalOcean Droplet**: $6/month

---

## Troubleshooting

### Issue: App can't connect to server
**Solution:**
- Check if server is running
- Verify URL in ApiConfig.java
- Check firewall settings
- Ensure CORS is configured

### Issue: Model files too large
**Solution:**
- Use Git LFS for large files
- Upload models separately via FTP
- Use cloud storage (AWS S3, Google Cloud Storage)

### Issue: Server timeout
**Solution:**
- Increase timeout settings
- Optimize model loading
- Use caching for frequently accessed data

### Issue: Database locked
**Solution:**
- Switch from SQLite to PostgreSQL
- Enable WAL mode for SQLite
- Reduce concurrent writes

---

## Next Steps After Deployment

1. ✅ Test all features thoroughly
2. ✅ Share APK with test users
3. ✅ Monitor server logs
4. ✅ Collect user feedback
5. ✅ Plan for scaling if needed
6. ✅ Set up automated backups
7. ✅ Consider custom domain name
8. ✅ Add analytics (optional)

---

## Custom Domain (Optional)

If you want a custom domain like `greenscan.com`:

1. Buy domain from Namecheap, GoDaddy, etc. (~$10-15/year)
2. Configure DNS settings:
   - Add CNAME record pointing to your hosting platform
3. Update SSL certificate
4. Update ApiConfig.java with new domain

---

## Support & Resources

- PythonAnywhere Help: https://help.pythonanywhere.com
- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- Flask Deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/

---

## Conclusion

For your college project, I recommend starting with **PythonAnywhere** (free tier) because:
- ✅ No credit card required
- ✅ Easy setup
- ✅ Python-friendly
- ✅ Good for demonstrations
- ✅ Can upgrade later if needed

Once deployed, your app will be accessible from anywhere, making it perfect for your panel presentation!

Good luck with your deployment! 🚀
