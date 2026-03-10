package com.example.weeddetector;

import android.Manifest;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.ScrollView;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "WeedDetector";
    private static final int CAMERA_REQUEST = 1888;
    private static final int GALLERY_REQUEST = 1889;
    private static final int CAMERA_PERMISSION = 100;
    private static final int STORAGE_PERMISSION = 101;

    private WeedDetector detector;
    private ImageView imageView;
    private TextView resultText;
    private LinearLayout placeholderLayout;
    private TextView userInfoText;
    private ScrollView scrollView;
    private Button logoutButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "onCreate started");

        try {
            setContentView(R.layout.activity_main);
            Log.d(TAG, "Layout set successfully");

            imageView = findViewById(R.id.imageView);
            resultText = findViewById(R.id.resultText);
            placeholderLayout = findViewById(R.id.placeholderLayout);
            scrollView = findViewById(R.id.scrollView);
            userInfoText = findViewById(R.id.userInfoText);
            Button scanButton = findViewById(R.id.scanButton);
            Button galleryButton = findViewById(R.id.galleryButton);
            logoutButton = findViewById(R.id.logoutButton);

            Log.d(TAG, "All views found successfully");

            // Display user info
            displayUserInfo();

            try {
                detector = new WeedDetector(this);
                Log.d(TAG, "WeedDetector initialized successfully");
                resultText.setText("Ready to identify weeds.\n\nTake a photo or choose from gallery to identify weed species.");
            } catch (Exception e) {
                Log.e(TAG, "Error loading WeedDetector", e);
                resultText.setText("❌ Error Loading AI Model\n\n" + e.getMessage() + "\n\nPlease ensure:\n• App has proper permissions\n• Model files are included\n• Sufficient storage space");
                e.printStackTrace();
            }

            scanButton.setOnClickListener(v -> {
                Log.d(TAG, "Scan button clicked");
                if (checkCameraPermission()) {
                    openCamera();
                }
            });

            galleryButton.setOnClickListener(v -> {
                Log.d(TAG, "Gallery button clicked");
                if (checkStoragePermission()) {
                    openGallery();
                }
            });

            logoutButton.setOnClickListener(v -> {
                Log.d(TAG, "Logout button clicked");
                logout();
            });

            Log.d(TAG, "onCreate completed successfully");

            // Check for model updates (once per day)
            checkForModelUpdates();

        } catch (Exception e) {
            Log.e(TAG, "Fatal error in onCreate", e);
            e.printStackTrace();
        }
    }

    private void checkForModelUpdates() {
        ModelUpdateManager updateManager = new ModelUpdateManager(this);

        if (updateManager.shouldCheckForUpdates()) {
            updateManager.checkForUpdates(new ModelUpdateManager.UpdateCallback() {
                @Override
                public void onUpdateAvailable(int newVersion) {
                    runOnUiThread(() -> {
                        android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(MainActivity.this);
                        builder.setTitle("Model Update Available");
                        builder.setMessage("A new weed detection model (v" + newVersion + ") is available with support for more weed types. Would you like to download it now?");
                        builder.setPositiveButton("Update Now", (dialog, which) -> {
                            downloadModelUpdate();
                        });
                        builder.setNegativeButton("Later", null);
                        builder.show();
                    });
                }

                @Override
                public void onUpdateComplete(boolean success, String message) {
                    // Not called here
                }

                @Override
                public void onNoUpdateNeeded() {
                    Log.d(TAG, "Model is up to date");
                }

                @Override
                public void onError(String error) {
                    Log.e(TAG, "Error checking for updates: " + error);
                }
            });
        }
    }

    private void downloadModelUpdate() {
        ModelUpdateManager updateManager = new ModelUpdateManager(this);

        android.app.ProgressDialog progressDialog = new android.app.ProgressDialog(this);
        progressDialog.setTitle("Downloading Update");
        progressDialog.setMessage("Downloading new model...");
        progressDialog.setCancelable(false);
        progressDialog.show();

        updateManager.downloadUpdate(new ModelUpdateManager.UpdateCallback() {
            @Override
            public void onUpdateAvailable(int newVersion) {
                // Not called here
            }

            @Override
            public void onUpdateComplete(boolean success, String message) {
                runOnUiThread(() -> {
                    progressDialog.dismiss();

                    android.app.AlertDialog.Builder builder = new android.app.AlertDialog.Builder(MainActivity.this);
                    builder.setTitle(success ? "Update Complete" : "Update Failed");
                    builder.setMessage(message);

                    if (success) {
                        builder.setPositiveButton("Restart App", (dialog, which) -> {
                            // Restart the app
                            Intent intent = getIntent();
                            finish();
                            startActivity(intent);
                        });
                    } else {
                        builder.setPositiveButton("OK", null);
                    }

                    builder.show();
                });
            }

            @Override
            public void onNoUpdateNeeded() {
                // Not called here
            }

            @Override
            public void onError(String error) {
                runOnUiThread(() -> {
                    progressDialog.dismiss();
                    android.widget.Toast.makeText(MainActivity.this, "Update failed: " + error, android.widget.Toast.LENGTH_LONG).show();
                });
            }
        });
    }

    private boolean checkCameraPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA)
                != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this,
                new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION);
            return false;
        }
        return true;
    }
    
    private boolean checkStoragePermission() {
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.TIRAMISU) {
            // Android 13+ uses READ_MEDIA_IMAGES
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_MEDIA_IMAGES) 
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, 
                    new String[]{Manifest.permission.READ_MEDIA_IMAGES}, STORAGE_PERMISSION);
                return false;
            }
        } else {
            // Older Android versions use READ_EXTERNAL_STORAGE
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) 
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, 
                    new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, STORAGE_PERMISSION);
                return false;
            }
        }
        return true;
    }
    
    private void openGallery() {
        Intent galleryIntent = new Intent(Intent.ACTION_PICK);
        galleryIntent.setType("image/*");
        if (galleryIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(galleryIntent, GALLERY_REQUEST);
        }
    }

    private void displayUserInfo() {
        SharedPreferences prefs = getSharedPreferences("WeedDetectorPrefs", MODE_PRIVATE);
        String fullName = prefs.getString("fullName", "");
        String username = prefs.getString("username", "");
        String userType = prefs.getString("userType", "");

        String displayText;
        if (!fullName.isEmpty()) {
            displayText = "Welcome, " + fullName;
            if (!userType.isEmpty()) {
                displayText += " (" + userType + ")";
            }
        } else if (!username.isEmpty()) {
            displayText = "Welcome, " + username;
        } else {
            displayText = "Welcome";
        }

        userInfoText.setText(displayText);
    }

    private void logout() {
        // Clear all saved login data
        SharedPreferences prefs = getSharedPreferences("WeedDetectorPrefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = prefs.edit();
        editor.clear();
        editor.apply();

        // Go back to login activity
        Intent intent = new Intent(MainActivity.this, LoginActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        startActivity(intent);
        finish();
    }

    private void openCamera() {
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        if (cameraIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(cameraIntent, CAMERA_REQUEST);
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        
        Bitmap photo = null;
        
        // Handle camera result
        if (requestCode == CAMERA_REQUEST && resultCode == RESULT_OK) {
            photo = (Bitmap) data.getExtras().get("data");
            Log.d(TAG, "Camera photo received");
        }
        // Handle gallery result
        else if (requestCode == GALLERY_REQUEST && resultCode == RESULT_OK && data != null) {
            try {
                android.net.Uri selectedImage = data.getData();
                Log.d(TAG, "Gallery image URI: " + selectedImage);
                
                // Load bitmap from URI
                photo = android.provider.MediaStore.Images.Media.getBitmap(this.getContentResolver(), selectedImage);
                
                if (photo == null) {
                    Log.e(TAG, "Failed to load bitmap from gallery");
                    android.widget.Toast.makeText(this, "Failed to load image", android.widget.Toast.LENGTH_SHORT).show();
                    return;
                }
                
                Log.d(TAG, "Gallery photo loaded: " + photo.getWidth() + "x" + photo.getHeight());
                
            } catch (Exception e) {
                Log.e(TAG, "Error loading image from gallery", e);
                android.widget.Toast.makeText(this, "Error loading image: " + e.getMessage(), android.widget.Toast.LENGTH_LONG).show();
                return;
            }
        }
        
        // Process the image if we have one
        if (photo != null) {
            imageView.setImageBitmap(photo);

            // Hide placeholder layout
            if (placeholderLayout != null) {
                placeholderLayout.setVisibility(LinearLayout.GONE);
            }

            try {
                // Detect weed
                Log.d(TAG, "Starting weed detection...");
                WeedDetector.WeedResult result = detector.detectWeed(photo);
                Log.d(TAG, "Detection complete: " + result.name + " (" + result.confidence + ")");
                
                if (result.info != null) {
                    Log.d(TAG, "Scientific name: " + result.info.scientificName);
                    Log.d(TAG, "Description length: " + result.info.description.length());
                } else {
                    Log.e(TAG, "WeedInfo is null!");
                }

                // Check confidence threshold
                float confidenceThreshold = 0.75f; // 75% minimum confidence

                if (result.confidence < confidenceThreshold) {
                    // Low confidence - probably not a weed
                    resultText.setText("⚠️ UNCERTAIN DETECTION\n\nConfidence: " + String.format("%.0f%%", result.confidence * 100) + "\n\nThis image doesn't match any known weed in our database with high confidence. Please try:\n\n• Taking a clearer photo\n• Better lighting conditions\n• Closer view of the plant\n• Focusing on leaves and stems");
                } else if (result.name.equals("not_weed")) {
                    // Detected as not a weed
                    resultText.setText("✓ NOT A WEED\n\nConfidence: " + String.format("%.0f%%", result.confidence * 100) + "\n\nThis appears to be a non-weed plant or object. The AI has determined this is not a harmful weed species.\n\nIf you believe this is incorrect, please ensure you're scanning actual weed plants.");
                } else {
                    // High confidence weed detection
                    StringBuilder output = new StringBuilder();
                    output.append("🌿 ").append(result.name.toUpperCase()).append("\n\n");
                    output.append("━━━━━━━━━━━━━━━━━━━━\n\n");
                    output.append("📊 Confidence: ").append(String.format("%.1f%%", result.confidence * 100)).append("\n\n");
                    
                    if (result.info != null) {
                        output.append("🔬 Scientific Name:\n").append(result.info.scientificName).append("\n\n");
                        output.append("📝 Description:\n").append(result.info.description).append("\n\n");
                        output.append("🛡️ Control Methods:\n").append(result.info.controlMethods);
                    } else {
                        output.append("⚠️ No additional information available for this weed.");
                    }

                    resultText.setText(output.toString());
                    Log.d(TAG, "Result displayed successfully");
                }

                scrollView.post(() -> scrollView.fullScroll(ScrollView.FOCUS_UP));
                
            } catch (Exception e) {
                Log.e(TAG, "Error during detection", e);
                resultText.setText("❌ Error during detection\n\n" + e.getMessage());
            }
        } else {
            Log.w(TAG, "Photo is null, nothing to process");
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (detector != null) {
            detector.close();
        }
    }
}
