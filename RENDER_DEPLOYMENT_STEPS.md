# Deploy Green Scan to Render - Step by Step Guide

## Prerequisites
- GitHub account
- Render account (free)
- Your project files ready

---

## STEP 1: Prepare Your GitHub Repository

### Option A: Create New Repository

1. Go to https://github.com
2. Click "New repository"
3. Name it: `green-scan-weed-detector`
4. Make it Public or Private
5. Don't initialize with README (we have files already)
6. Click "Create repository"

### Option B: Use Existing Repository

Skip to Step 2 if you already have a GitHub repo.

---

## STEP 2: Push Your Code to GitHub

Open Command Prompt in your project folder and run:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit for Render deployment"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/green-scan-weed-detector.git

# Push to GitHub
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` with your actual GitHub username.

If you get an error about 'master' vs 'main', use:
```bash
git branch -M main
git push -u origin main
```

---

## STEP 3: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with your GitHub account
4. Authorize Render to access your GitHub

---

## STEP 4: Create New Web Service

1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect" next to your `green-scan-weed-detector` repository
   - If you don't see it, click "Configure account" and grant access

---

## STEP 5: Configure Web Service

Fill in the following settings:

### Basic Settings:
- **Name:** `green-scan` (or any name you prefer)
- **Region:** Choose closest to Philippines (Singapore recommended)
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

### Build & Deploy Settings:
- **Build Command:** `./build.sh`
- **Start Command:** `python unified_admin_server.py`

### Instance Type:
- Select **Free** (this gives you 750 hours/month free)

### Advanced Settings (click "Advanced"):

#### Environment Variables:
Click "Add Environment Variable" and add:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.10.9` |
| `DEBUG` | `False` |

---

## STEP 6: Deploy

1. Click "Create Web Service" button at the bottom
2. Render will start building your app
3. Wait 5-10 minutes for first deployment
4. Watch the logs for any errors

### What Happens During Deployment:
- ✅ Render clones your GitHub repo
- ✅ Installs Python 3.10
- ✅ Runs `build.sh` (installs dependencies)
- ✅ Starts your Flask server
- ✅ Assigns you a URL

---

## STEP 7: Get Your URL

Once deployment succeeds:

1. You'll see "Live" status with a green dot
2. Your URL will be at the top: `https://green-scan-XXXX.onrender.com`
3. Copy this URL

---

## STEP 8: Test Your Deployment

### Test Admin Panel:
1. Visit: `https://your-app.onrender.com/admin/login`
2. Login with:
   - Username: `admin`
   - Password: `admin123`
3. Check if dashboard loads

### Test API Endpoints:

Open Command Prompt and test:

```bash
# Test model version endpoint
curl https://your-app.onrender.com/model/version

# Test registration endpoint
curl -X POST https://your-app.onrender.com/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"testuser\",\"password\":\"test123\",\"fullName\":\"Test User\",\"userType\":\"Farmer\"}"
```

---

## STEP 9: Update Android App

### Update ApiConfig.java:

```java
package com.example.weeddetector;

public class ApiConfig {
    // UPDATE THIS with your Render URL
    public static final String BASE_URL = "https://green-scan-XXXX.onrender.com";
    
    // API Endpoints
    public static final String REGISTER_URL = BASE_URL + "/register";
    public static final String LOGIN_URL = BASE_URL + "/login";
    public static final String MODEL_VERSION_URL = BASE_URL + "/model/version";
    public static final String MODEL_DOWNLOAD_URL = BASE_URL + "/model/download/model";
    public static final String LABELS_DOWNLOAD_URL = BASE_URL + "/model/download/labels";
    public static final String INFO_DOWNLOAD_URL = BASE_URL + "/model/download/info";
}
```

### Rebuild APK:

1. Open Android Studio
2. **Build → Clean Project**
3. **Build → Rebuild Project**
4. **Build → Build Bundle(s) / APK(s) → Build APK(s)**
5. Find APK in: `WeedDetectorApp/app/build/outputs/apk/debug/`
6. Install on your phone

---

## STEP 10: Test Complete System

1. **Install new APK** on your phone
2. **Register** a new user
3. **Login** with credentials
4. **Take a photo** of a weed
5. **Verify** detection works
6. **Check** if weed information displays

---

## Important Notes

### Free Tier Limitations:
- ⚠️ **Sleeps after 15 minutes of inactivity**
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for testing/demo)
- Shared CPU and 512MB RAM

### Keep Service Awake (Optional):
Use a service like UptimeRobot to ping your app every 14 minutes:
1. Sign up at https://uptimerobot.com (free)
2. Add monitor for your Render URL
3. Set interval to 5 minutes

### Upgrade to Paid (if needed):
- Starter Plan: $7/month
- No sleep, more resources
- Custom domain support

---

## Troubleshooting

### Issue: Build Failed
**Check logs for errors:**
- Missing dependencies in requirements.txt
- Python version mismatch
- File path issues

**Solution:**
- Update requirements.txt
- Check build.sh script
- Verify all files are in GitHub

### Issue: App Crashes on Start
**Check logs for:**
- Port binding errors
- Missing environment variables
- Database initialization errors

**Solution:**
- Ensure `PORT` environment variable is used
- Check unified_admin_server.py configuration
- Verify all required files are present

### Issue: Android App Can't Connect
**Verify:**
- ✅ Render service is "Live" (green dot)
- ✅ URL in ApiConfig.java is correct
- ✅ No typos in URL
- ✅ Using HTTPS (not HTTP)

**Solution:**
- Test URL in browser first
- Check Render logs for incoming requests
- Verify CORS is enabled

### Issue: Model Files Not Found
**Problem:** Model files might be too large for GitHub

**Solution:**
1. Use Git LFS (Large File Storage):
```bash
git lfs install
git lfs track "*.tflite"
git lfs track "*.h5"
git add .gitattributes
git commit -m "Add Git LFS"
git push
```

2. Or upload models directly to Render:
   - Use Render Disk for persistent storage
   - Upload via SSH or API

---

## Monitoring Your App

### View Logs:
1. Go to Render Dashboard
2. Click on your service
3. Click "Logs" tab
4. See real-time logs

### Check Metrics:
- CPU usage
- Memory usage
- Request count
- Response times

### Set Up Alerts:
- Email notifications for failures
- Slack integration
- Discord webhooks

---

## Updating Your App

When you make changes:

1. **Commit changes:**
```bash
git add .
git commit -m "Description of changes"
git push
```

2. **Render auto-deploys:**
   - Detects GitHub push
   - Rebuilds automatically
   - Deploys new version
   - Zero downtime

3. **Manual deploy:**
   - Go to Render Dashboard
   - Click "Manual Deploy"
   - Select branch
   - Click "Deploy"

---

## Database Persistence

### Important:
- Free tier has ephemeral storage
- Database resets on each deploy
- Users will be lost

### Solutions:

#### Option 1: Render Disk (Paid)
- Add persistent disk to your service
- $0.25/GB per month
- Database survives deploys

#### Option 2: External Database
- Use PostgreSQL on Render (free tier available)
- Update code to use PostgreSQL instead of SQLite
- More reliable for production

#### Option 3: Backup/Restore
- Download users.db before deploy
- Upload after deploy
- Manual process

---

## Custom Domain (Optional)

If you want `greenscan.com` instead of `green-scan-xxxx.onrender.com`:

1. **Buy domain** (~$10-15/year)
2. **In Render Dashboard:**
   - Go to Settings
   - Click "Custom Domain"
   - Add your domain
3. **Update DNS:**
   - Add CNAME record
   - Point to Render URL
4. **Update Android app** with new domain

---

## Security Best Practices

### 1. Change Default Admin Password:
After first login, change admin password in the database.

### 2. Use Environment Variables:
Store sensitive data in Render environment variables:
- Admin password
- Secret keys
- API keys

### 3. Enable HTTPS:
Render provides free SSL certificates automatically.

### 4. Rate Limiting:
Add rate limiting to prevent abuse (already in code).

### 5. Regular Backups:
Download users.db regularly for backup.

---

## Cost Estimate

### Free Tier:
- ✅ 750 hours/month
- ✅ Enough for demo/testing
- ✅ Good for college project
- ⚠️ Sleeps after inactivity

### If You Need More:
- **Starter:** $7/month
  - No sleep
  - Better performance
  - Custom domain
  
- **Standard:** $25/month
  - More resources
  - Better for production

---

## Success Checklist

- ✅ Code pushed to GitHub
- ✅ Render service created
- ✅ Build successful
- ✅ Service is "Live"
- ✅ Admin panel accessible
- ✅ API endpoints working
- ✅ Android app updated
- ✅ APK rebuilt and tested
- ✅ End-to-end test completed

---

## Next Steps

1. ✅ Share your Render URL with team
2. ✅ Test with multiple users
3. ✅ Monitor logs for errors
4. ✅ Prepare for panel presentation
5. ✅ Consider custom domain
6. ✅ Set up monitoring/alerts

---

## Support Resources

- Render Docs: https://render.com/docs
- Render Community: https://community.render.com
- Flask Deployment: https://flask.palletsprojects.com/en/2.3.x/deploying/

---

## Congratulations! 🎉

Your Green Scan app is now deployed online and accessible from anywhere!

Your panel presentation will be impressive with a live, working online system.

Good luck! 🚀
