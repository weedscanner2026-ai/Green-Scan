package com.example.weeddetector;

/**
 * API Configuration
 * IMPORTANT: Update SERVER_IP with your actual server IP address
 */
public class    ApiConfig {
    
    // Change this to your computer's IP address where the registration server is running
    // To find your IP:
    // - Windows: Open CMD and type "ipconfig", look for IPv4 Address
    // - Mac/Linux: Open Terminal and type "ifconfig" or "ip addr"
    // 
    // Examples:
    // - Local testing: "192.168.0.253"
    // - Same WiFi network: "192.168.0.105"
    // - Cloud server: "yourdomain.com"
    
    private static final String SERVER_IP = "192.168.0.253"; // CHANGE THIS!
    private static final String SERVER_PORT = "5000";
    
    public static final String BASE_URL = "http://" + SERVER_IP + ":" + SERVER_PORT;
    public static final String LOGIN_URL = BASE_URL + "/api/login";
    public static final String REGISTER_URL = BASE_URL + "/api/register";
}
