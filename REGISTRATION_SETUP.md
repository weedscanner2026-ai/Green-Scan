# User Registration System Setup Guide

## Overview
The Green Scan app now requires users to register before using the app. Admins can view all registered users and their details through a web dashboard.

---

## Backend Server Setup

### 1. Install Dependencies

```bash
pip install flask flask-cors
```

### 2. Start the Registration Server

```bash
python registration_server.py
```

The server will start on `http://localhost:5000`

### 3. Admin Dashboard Access

- URL: `http://localhost:5000/admin/login`
- Default Username: `admin`
- Default Password: `admin123`

---

## Admin Dashboard Features

### User Statistics
- Total registered users
- Number of students
- Number of agriculturists  
- Number of other users

### User Management Table
View all registered users with:
- ID
- Username
- Full Name
- Email
- User Type (Student/Agriculturist/Other)
- Institution
- Phone Number
- Registration Date
- Last Login Date
- Account Status (Active/Inactive)
- Activate/Deactivate button

---

## Android App Integration

### Required Files Created:
1. `activity_login.xml` - Login screen layout
2. `activity_register.xml` - Registration screen layout

### Next Steps (To be implemented in Android Studio):

1. **Create LoginActivity.java**
   - Handle user login
   - Connect to API: `POST http://YOUR_SERVER_IP:5000/api/login`
   - Save user session
   - Redirect to MainActivity on success

2. **Create RegisterActivity.java**
   - Handle user registration
   - Connect to API: `POST http://YOUR_SERVER_IP:5000/api/register`
   - Validate input fields
   - Redirect to LoginActivity on success

3. **Update AndroidManifest.xml**
   ```xml
   <activity android:name=".LoginActivity"
       android:exported="true">
       <intent-filter>
           <action android:name="android.intent.action.MAIN" />
           <category android:name="android.intent.category.LAUNCHER" />
       </intent-filter>
   </activity>
   <activity android:name=".RegisterActivity" />
   <activity android:name=".MainActivity" />
   ```

4. **Add Internet Permission**
   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   ```

5. **Add HTTP Library** (in app/build.gradle)
   ```gradle
   dependencies {
       implementation 'com.squareup.okhttp3:okhttp:4.10.0'
       implementation 'com.google.code.gson:gson:2.10'
   }
   ```

---

## API Endpoints

### Register User
```
POST /api/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "user_type": "Student",
    "institution": "University of Example",
    "phone": "+1234567890"
}

Response:
{
    "success": true,
    "message": "Registration successful",
    "username": "john_doe"
}
```

### Login User
```
POST /api/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "password123"
}

Response:
{
    "success": true,
    "message": "Login successful",
    "user": {
        "id": 1,
        "full_name": "John Doe",
        "user_type": "Student"
    }
}
```

---

## User Types

The system supports three user types:
1. **Student** - For students using the app for educational purposes
2. **Agriculturist** - For farmers and agricultural professionals
3. **Other** - For researchers, hobbyists, and other interested parties

---

## Database

The system uses SQLite database (`users.db`) with two tables:

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password_hash
- full_name
- user_type
- institution
- phone
- registered_date
- last_login
- is_active

### Admins Table
- id (Primary Key)
- username (Unique)
- password_hash

---

## Security Notes

1. Passwords are hashed using SHA256
2. Admin session is managed server-side
3. Users can be deactivated by admin (prevents login)
4. Change default admin password in production

---

## Testing the System

### 1. Start the server
```bash
python registration_server.py
```

### 2. Test Registration (using curl or Postman)
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "email": "test@example.com",
    "password": "test123",
    "full_name": "Test User",
    "user_type": "Student",
    "institution": "Test University"
  }'
```

### 3. Test Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_user",
    "password": "test123"
  }'
```

### 4. View Admin Dashboard
Open browser: `http://localhost:5000/admin/login`

---

## Deployment Notes

### For Production:
1. Change admin password
2. Use HTTPS
3. Use a production-grade database (PostgreSQL/MySQL)
4. Add rate limiting
5. Implement email verification
6. Add password reset functionality
7. Use environment variables for secrets

### Server IP Configuration:
- Update Android app to use your server's IP address
- Example: `http://192.168.1.100:5000/api/`
- For cloud deployment: `https://yourdomain.com/api/`

---

## Current Status

✓ Backend server created
✓ Admin dashboard created
✓ API endpoints implemented
✓ Android layouts created
⚠ Android Java activities need to be implemented
⚠ Server IP needs to be configured in Android app

---

## Next Steps

1. Implement LoginActivity.java and RegisterActivity.java
2. Configure server IP in Android app
3. Test registration and login flow
4. Deploy server to cloud (optional)
5. Update AndroidManifest.xml to make LoginActivity the launcher
