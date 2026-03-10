# Quick Start Guide - User Registration System

## Step 1: Find Your Computer's IP Address

### Windows:
1. Open Command Prompt (CMD)
2. Type: `ipconfig`
3. Look for "IPv4 Address" (e.g., 192.168.1.100)

### Mac/Linux:
1. Open Terminal
2. Type: `ifconfig` or `ip addr`
3. Look for your local IP address

## Step 2: Update Android App Configuration

1. Open `WeedDetectorApp/app/src/main/java/com/example/weeddetector/ApiConfig.java`
2. Change this line:
   ```java
   private static final String SERVER_IP = "192.168.1.100"; // CHANGE THIS!
   ```
   Replace `192.168.1.100` with YOUR computer's IP address

## Step 3: Start the Registration Server

```bash
# Install dependencies (first time only)
pip install flask flask-cors

# Start the server
python registration_server.py
```

You should see:
```
Green Scan REGISTRATION SERVER
Default Admin Credentials:
  Username: admin
  Password: admin123

Admin Dashboard: http://localhost:5000/admin/login
API Endpoint: http://localhost:5000/api/
```

## Step 4: Build and Run the Android App

1. Open Android Studio
2. Open the WeedDetectorApp project
3. Build > Rebuild Project
4. Run the app on your phone

**IMPORTANT:** Your phone and computer must be on the same WiFi network!

## Step 5: Test Registration

1. App will open to Login screen
2. Click "Don't have an account? Register"
3. Fill in the registration form:
   - Full Name: Your Name
   - Username: yourusername
   - Email: your@email.com
   - Password: (at least 6 characters)
   - User Type: Select (Student/Agriculturist/Other)
   - Institution: (optional)
   - Phone: (optional)
4. Click "Register"
5. You should see "Registration successful! Please login."

## Step 6: Test Login

1. Enter your username and password
2. Click "Login"
3. You should be redirected to the main weed scanner screen

## Step 7: View Users in Admin Dashboard

1. Open browser on your computer
2. Go to: `http://localhost:5000/admin/login`
3. Login with:
   - Username: `admin`
   - Password: `admin123`
4. You'll see all registered users with their details!

---

## Troubleshooting

### "Connection error" in app:
- Check if server is running
- Verify your phone and computer are on same WiFi
- Check if you updated the IP address in ApiConfig.java
- Try pinging your computer from phone

### "Cannot connect to server":
- Make sure firewall allows port 5000
- Windows: Allow Python through Windows Firewall
- Try accessing `http://YOUR_IP:5000` from phone browser

### App crashes on launch:
- Check Android Studio Logcat for errors
- Rebuild the project
- Make sure all files are saved

---

## Testing Flow

1. **Register a Student:**
   - Name: John Doe
   - Username: john_student
   - Type: Student
   - Institution: University of Example

2. **Register an Agriculturist:**
   - Name: Jane Farmer
   - Username: jane_farmer
   - Type: Agriculturist
   - Institution: Local Farm

3. **View in Admin Dashboard:**
   - See both users listed
   - Check their registration dates
   - View their user types

4. **Test Deactivation:**
   - Click "Deactivate" on a user
   - Try logging in with that user (should fail)
   - Click "Activate" to re-enable

---

## What's Next?

After successful registration and login:
- Users can scan weeds using the camera
- Model will identify weeds (including "not_weed" for non-weeds)
- Admin can track who is using the app
- Admin can see user statistics by type

---

## Files Created

✓ `registration_server.py` - Backend server
✓ `templates/admin_login.html` - Admin login page
✓ `templates/admin_dashboard.html` - User management dashboard
✓ `LoginActivity.java` - Android login screen
✓ `RegisterActivity.java` - Android registration screen
✓ `ApiConfig.java` - Server configuration
✓ `activity_login.xml` - Login layout
✓ `activity_register.xml` - Registration layout
✓ Updated `AndroidManifest.xml` - Added activities and permissions

---

## Default Credentials

**Admin Dashboard:**
- Username: `admin`
- Password: `admin123`

**IMPORTANT:** Change the admin password in production!

---

## Server Commands

```bash
# Start server
python registration_server.py

# Stop server
Ctrl + C

# View database
sqlite3 users.db
.tables
SELECT * FROM users;
.quit
```

---

## Success Indicators

✓ Server shows "Running on http://0.0.0.0:5000"
✓ Admin dashboard loads at localhost:5000
✓ App shows login screen on launch
✓ Registration creates new user
✓ Login redirects to scanner screen
✓ Admin can see registered users

---

## Need Help?

Check the detailed guide: `REGISTRATION_SETUP.md`
