package com.example.weeddetector;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class ModelUpdateManager {
    private static final String TAG = "ModelUpdateManager";
    private static final String PREFS_NAME = "ModelPrefs";
    private static final String KEY_MODEL_VERSION = "model_version";
    private static final String KEY_LAST_CHECK = "last_check";
    
    private Context context;
    private String serverUrl;
    
    public interface UpdateCallback {
        void onUpdateAvailable(int newVersion);
        void onUpdateComplete(boolean success, String message);
        void onNoUpdateNeeded();
        void onError(String error);
    }
    
    public ModelUpdateManager(Context context) {
        this.context = context;
        this.serverUrl = ApiConfig.BASE_URL;
    }
    
    // Check if update is available
    public void checkForUpdates(UpdateCallback callback) {
        new Thread(() -> {
            try {
                URL url = new URL(serverUrl + "/model/version");
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                
                int responseCode = conn.getResponseCode();
                if (responseCode == 200) {
                    BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                    StringBuilder response = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        response.append(line);
                    }
                    br.close();
                    
                    JSONObject json = new JSONObject(response.toString());
                    int serverVersion = json.getInt("version");
                    int currentVersion = getCurrentModelVersion();
                    
                    if (serverVersion > currentVersion) {
                        callback.onUpdateAvailable(serverVersion);
                    } else {
                        callback.onNoUpdateNeeded();
                    }
                } else {
                    callback.onError("Server returned code: " + responseCode);
                }
            } catch (Exception e) {
                Log.e(TAG, "Error checking for updates", e);
                callback.onError(e.getMessage());
            }
        }).start();
    }
    
    // Download and install model update
    public void downloadUpdate(UpdateCallback callback) {
        new Thread(() -> {
            try {
                // Download model file
                File modelFile = downloadFile("/model/download/model", "weed_detector.tflite");
                if (modelFile == null) {
                    callback.onUpdateComplete(false, "Failed to download model");
                    return;
                }
                
                // Download labels file
                File labelsFile = downloadFile("/model/download/labels", "labels.txt");
                if (labelsFile == null) {
                    callback.onUpdateComplete(false, "Failed to download labels");
                    return;
                }
                
                // Download weed info
                File infoFile = downloadFile("/model/download/info", "weed_info.json");
                if (infoFile == null) {
                    callback.onUpdateComplete(false, "Failed to download weed info");
                    return;
                }
                
                // Get new version number
                URL versionUrl = new URL(serverUrl + "/model/version");
                HttpURLConnection conn = (HttpURLConnection) versionUrl.openConnection();
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
                br.close();
                
                JSONObject json = new JSONObject(response.toString());
                int newVersion = json.getInt("version");
                
                // Update version in preferences
                setCurrentModelVersion(newVersion);
                
                callback.onUpdateComplete(true, "Model updated successfully! Please restart the app.");
                
            } catch (Exception e) {
                Log.e(TAG, "Error downloading update", e);
                callback.onUpdateComplete(false, "Download failed: " + e.getMessage());
            }
        }).start();
    }
    
    private File downloadFile(String endpoint, String filename) {
        try {
            URL url = new URL(serverUrl + endpoint);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            
            if (conn.getResponseCode() != 200) {
                return null;
            }
            
            // Save to internal storage
            File outputFile = new File(context.getFilesDir(), filename);
            FileOutputStream fos = new FileOutputStream(outputFile);
            InputStream is = conn.getInputStream();
            
            byte[] buffer = new byte[4096];
            int bytesRead;
            while ((bytesRead = is.read(buffer)) != -1) {
                fos.write(buffer, 0, bytesRead);
            }
            
            fos.close();
            is.close();
            
            Log.d(TAG, "Downloaded: " + filename + " (" + outputFile.length() + " bytes)");
            return outputFile;
            
        } catch (Exception e) {
            Log.e(TAG, "Error downloading " + filename, e);
            return null;
        }
    }
    
    private int getCurrentModelVersion() {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        return prefs.getInt(KEY_MODEL_VERSION, 1); // Default version 1
    }
    
    private void setCurrentModelVersion(int version) {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        prefs.edit().putInt(KEY_MODEL_VERSION, version).apply();
    }
    
    public boolean shouldCheckForUpdates() {
        SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        long lastCheck = prefs.getLong(KEY_LAST_CHECK, 0);
        long now = System.currentTimeMillis();
        long dayInMillis = 24 * 60 * 60 * 1000;
        
        if (now - lastCheck > dayInMillis) {
            prefs.edit().putLong(KEY_LAST_CHECK, now).apply();
            return true;
        }
        return false;
    }
}
