package com.example.weeddetector;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;
import androidx.appcompat.app.AppCompatActivity;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class RegisterActivity extends AppCompatActivity {
    
    // Server URL from ApiConfig
    private static final String SERVER_URL = ApiConfig.REGISTER_URL;
    
    private EditText fullNameInput;
    private EditText usernameInput;
    private EditText emailInput;
    private EditText passwordInput;
    private Spinner userTypeSpinner;
    private EditText institutionInput;
    private EditText phoneInput;
    private Button registerButton;
    private TextView loginLink;
    
    private String selectedUserType = "Student";
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);
        
        fullNameInput = findViewById(R.id.fullNameInput);
        usernameInput = findViewById(R.id.usernameInput);
        emailInput = findViewById(R.id.emailInput);
        passwordInput = findViewById(R.id.passwordInput);
        userTypeSpinner = findViewById(R.id.userTypeSpinner);
        institutionInput = findViewById(R.id.institutionInput);
        phoneInput = findViewById(R.id.phoneInput);
        registerButton = findViewById(R.id.registerButton);
        loginLink = findViewById(R.id.loginLink);
        
        // Setup user type spinner
        String[] userTypes = {"Student", "Agriculturist", "Other"};
        ArrayAdapter<String> adapter = new ArrayAdapter<>(this, 
            android.R.layout.simple_spinner_item, userTypes);
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        userTypeSpinner.setAdapter(adapter);
        
        userTypeSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override
            public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
                selectedUserType = userTypes[position];
            }
            
            @Override
            public void onNothingSelected(AdapterView<?> parent) {
                selectedUserType = "Student";
            }
        });
        
        registerButton.setOnClickListener(v -> registerUser());
        
        loginLink.setOnClickListener(v -> {
            finish(); // Go back to login
        });
    }
    
    private void registerUser() {
        String fullName = fullNameInput.getText().toString().trim();
        String username = usernameInput.getText().toString().trim();
        String email = emailInput.getText().toString().trim();
        String password = passwordInput.getText().toString().trim();
        String institution = institutionInput.getText().toString().trim();
        String phone = phoneInput.getText().toString().trim();
        
        // Validate required fields
        if (fullName.isEmpty() || username.isEmpty() || email.isEmpty() || password.isEmpty()) {
            Toast.makeText(this, "Please fill all required fields", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (!email.contains("@")) {
            Toast.makeText(this, "Please enter a valid email", Toast.LENGTH_SHORT).show();
            return;
        }
        
        if (password.length() < 6) {
            Toast.makeText(this, "Password must be at least 6 characters", Toast.LENGTH_SHORT).show();
            return;
        }
        
        registerButton.setEnabled(false);
        registerButton.setText("Registering...");
        
        new Thread(() -> {
            try {
                URL url = new URL(SERVER_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setDoOutput(true);
                
                // Create JSON payload
                JSONObject json = new JSONObject();
                json.put("full_name", fullName);
                json.put("username", username);
                json.put("email", email);
                json.put("password", password);
                json.put("user_type", selectedUserType);
                json.put("institution", institution);
                json.put("phone", phone);
                
                // Send request
                OutputStream os = conn.getOutputStream();
                os.write(json.toString().getBytes());
                os.flush();
                os.close();
                
                // Read response
                int responseCode = conn.getResponseCode();
                BufferedReader br;
                
                if (responseCode == 201 || responseCode == 200) {
                    br = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                } else {
                    br = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
                }
                
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) {
                    response.append(line);
                }
                br.close();
                
                JSONObject responseJson = new JSONObject(response.toString());
                boolean success = responseJson.getBoolean("success");
                String message = responseJson.getString("message");
                
                runOnUiThread(() -> {
                    registerButton.setEnabled(true);
                    registerButton.setText("Register");
                    
                    if (success) {
                        Toast.makeText(this, "Registration successful! Please login.", Toast.LENGTH_LONG).show();
                        finish(); // Go back to login
                    } else {
                        Toast.makeText(this, message, Toast.LENGTH_LONG).show();
                    }
                });
                
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> {
                    registerButton.setEnabled(true);
                    registerButton.setText("Register");
                    Toast.makeText(this, "Connection error: " + e.getMessage(), Toast.LENGTH_LONG).show();
                });
            }
        }).start();
    }
}
