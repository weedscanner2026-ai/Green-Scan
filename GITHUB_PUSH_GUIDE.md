# How to Push Your Project to GitHub - Step by Step

## What You Need:
- ✅ GitHub account (you have this)
- ✅ New repository created on GitHub (you have this)
- ✅ Git installed on your computer
- ✅ Your project folder (C:\Users\ASUS\Pictures\weeAdmin)

---

## Step 1: Install Git (if not installed)

Check if Git is installed:
```cmd
git --version
```

If you see a version number, Git is installed. Skip to Step 2.

If not installed:
1. Download from: https://git-scm.com/download/win
2. Run installer
3. Use default settings
4. Restart Command Prompt

---

## Step 2: Configure Git (First Time Only)

Open Command Prompt and run:

```cmd
git config --global user.name "Your Name"
git config --global user.email "your-email@example.com"
```

Replace with your actual name and the email you used for GitHub.

---

## Step 3: Get Your Repository URL

1. Go to your GitHub repository page
2. Click the green "Code" button
3. Copy the HTTPS URL (looks like: https://github.com/username/repo-name.git)

---

## Step 4: Push Your Code

Open Command Prompt in your project folder and run these commands ONE BY ONE:

### Initialize Git:
```cmd
git init
```

### Add all files:
```cmd
git add .
```

### Commit files:
```cmd
git commit -m "Initial commit - Green Scan Weed Detector"
```

### Connect to GitHub:
```cmd
git remote add origin YOUR_GITHUB_URL_HERE
```
Replace YOUR_GITHUB_URL_HERE with the URL you copied in Step 3.

### Push to GitHub:
```cmd
git branch -M main
git push -u origin main
```

You'll be asked for GitHub credentials:
- Username: your GitHub username
- Password: use Personal Access Token (not your password)

---

## Step 5: Create Personal Access Token (if needed)

If GitHub asks for password and rejects it:

1. Go to GitHub.com
2. Click your profile picture → Settings
3. Scroll down → Developer settings
4. Personal access tokens → Tokens (classic)
5. Generate new token (classic)
6. Give it a name: "Green Scan Deploy"
7. Select scopes: ✅ repo (all)
8. Click "Generate token"
9. COPY THE TOKEN (you won't see it again!)
10. Use this token as password when pushing

---

## Troubleshooting

### Error: "git is not recognized"
**Solution:** Install Git (see Step 1)

### Error: "fatal: not a git repository"
**Solution:** Make sure you're in the correct folder and ran `git init`

### Error: "failed to push"
**Solution:** 
- Check your internet connection
- Verify the repository URL is correct
- Make sure you have permission to push to the repo

### Error: "large files"
**Solution:** Some files might be too large. We'll handle this separately.

---

## What Gets Uploaded:

✅ All Python files (.py)
✅ HTML/CSS/JS files
✅ Configuration files
✅ Model files (if not too large)
✅ Documentation files

❌ Dataset folder (too large, excluded by .gitignore)
❌ Build folders
❌ Cache files

---

## After Successful Push:

1. Refresh your GitHub repository page
2. You should see all your files
3. Ready to deploy to Render!

---

## Next Step:

Once your code is on GitHub, you can proceed with Render deployment!
