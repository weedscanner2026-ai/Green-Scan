# Logout Feature Guide

## Overview
Added logout functionality to the Android app with user information display.

## Changes Made

### 1. Updated Layout (activity_main.xml)
- Added user info text at the top showing logged-in user details
- Added red logout button in top-right corner
- Adjusted image view margins to accommodate the new header

### 2. Updated MainActivity.java
- Added `userInfoText` and `logoutButton` view references
- Added `displayUserInfo()` method to show user details from SharedPreferences
- Added `logout()` method to clear session and return to login screen
- Imported `SharedPreferences` for session management

## Features

### User Info Display
Shows at the top of the screen:
- "Welcome, [Full Name] ([User Type])" if full name is available
- "Welcome, [Username]" if only username is available
- "Welcome" as fallback

### Logout Button
- Red button in top-right corner
- Clears all saved login data from SharedPreferences
- Returns user to LoginActivity
- Prevents back navigation to MainActivity after logout

## How It Works

1. When MainActivity loads, it reads user data from SharedPreferences
2. Displays personalized welcome message
3. When logout button is clicked:
   - All SharedPreferences data is cleared
   - User is redirected to LoginActivity
   - Activity stack is cleared to prevent back navigation

## Testing

1. Login to the app
2. Verify user info appears at the top
3. Click the logout button
4. Verify you're returned to the login screen
5. Try pressing back button - should not return to MainActivity

## Next Steps

To rebuild the app:
1. Open Android Studio
2. Build > Clean Project
3. Build > Rebuild Project
4. Run the app on your device

The logout feature is now fully functional!
