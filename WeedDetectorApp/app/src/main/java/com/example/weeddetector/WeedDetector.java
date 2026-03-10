package com.example.weeddetector;

import android.content.Context;
import android.graphics.Bitmap;
import org.tensorflow.lite.Interpreter;
import org.tensorflow.lite.support.common.FileUtil;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

public class WeedDetector {
    private static final int IMG_SIZE = 224;
    private static final int PIXEL_SIZE = 3;
    private static final int IMAGE_MEAN = 127;
    private static final float IMAGE_STD = 128.0f;
    
    private Interpreter interpreter;
    private List<String> labels;
    private JSONObject weedInfo;
    private Context context;
    
    public WeedDetector(Context context) throws IOException {
        this.context = context;
        
        // Try to load updated model from internal storage first
        File updatedModel = new File(context.getFilesDir(), "weed_detector.tflite");
        File updatedLabels = new File(context.getFilesDir(), "labels.txt");
        File updatedInfo = new File(context.getFilesDir(), "weed_info.json");
        
        if (updatedModel.exists() && updatedLabels.exists() && updatedInfo.exists()) {
            // Load updated model from internal storage
            interpreter = new Interpreter(loadModelFile(updatedModel));
            labels = loadLabelsFile(updatedLabels);
            loadWeedInfoFile(updatedInfo);
        } else {
            // Load default model from assets
            ByteBuffer model = FileUtil.loadMappedFile(context, "weed_detector.tflite");
            interpreter = new Interpreter(model);
            labels = FileUtil.loadLabels(context, "labels.txt");
            loadWeedInfo();
        }
    }
    
    private MappedByteBuffer loadModelFile(File file) throws IOException {
        FileInputStream inputStream = new FileInputStream(file);
        FileChannel fileChannel = inputStream.getChannel();
        long startOffset = 0;
        long declaredLength = fileChannel.size();
        MappedByteBuffer buffer = fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declaredLength);
        inputStream.close();
        return buffer;
    }
    
    private List<String> loadLabelsFile(File file) throws IOException {
        List<String> labelList = new ArrayList<>();
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
        String line;
        while ((line = reader.readLine()) != null) {
            labelList.add(line);
        }
        reader.close();
        return labelList;
    }
    
    private void loadWeedInfoFile(File file) throws IOException {
        FileInputStream fis = new FileInputStream(file);
        int size = fis.available();
        byte[] buffer = new byte[size];
        fis.read(buffer);
        fis.close();
        String json = new String(buffer, StandardCharsets.UTF_8);
        try {
            weedInfo = new JSONObject(json);
        } catch (Exception e) {
            e.printStackTrace();
            weedInfo = new JSONObject();
        }
    }
    
    private void loadWeedInfo() throws IOException {
        InputStream is = context.getAssets().open("weed_info.json");
        int size = is.available();
        byte[] buffer = new byte[size];
        is.read(buffer);
        is.close();
        String json = new String(buffer, StandardCharsets.UTF_8);
        try {
            weedInfo = new JSONObject(json);
        } catch (Exception e) {
            e.printStackTrace();
            weedInfo = new JSONObject();
        }
    }
    
    public WeedResult detectWeed(Bitmap bitmap) {
        // Preprocess image
        ByteBuffer inputBuffer = preprocessImage(bitmap);
        
        // Run inference
        float[][] output = new float[1][labels.size()];
        interpreter.run(inputBuffer, output);
        
        // Find best result
        int maxIndex = 0;
        float maxConfidence = 0;
        for (int i = 0; i < output[0].length; i++) {
            if (output[0][i] > maxConfidence) {
                maxConfidence = output[0][i];
                maxIndex = i;
            }
        }
        
        String weedName = labels.get(maxIndex);
        WeedInfo info = getWeedInfo(weedName);
        
        return new WeedResult(weedName, maxConfidence, info);
    }
    
    private WeedInfo getWeedInfo(String weedName) {
        try {
            android.util.Log.d("WeedDetector", "Looking up weed info for: '" + weedName + "'");
            JSONObject weeds = weedInfo.getJSONObject("weeds");
            android.util.Log.d("WeedDetector", "Total weeds in JSON: " + weeds.length());
            
            // Try exact match first
            if (weeds.has(weedName)) {
                android.util.Log.d("WeedDetector", "Found exact match for: " + weedName);
                JSONObject weed = weeds.getJSONObject(weedName);
                String scientificName = weed.optString("scientific_name", "N/A");
                String description = weed.optString("description", "No description available");
                android.util.Log.d("WeedDetector", "Scientific name: " + scientificName);
                android.util.Log.d("WeedDetector", "Description length: " + description.length());
                return new WeedInfo(
                    scientificName,
                    description,
                    weed.optString("family", "N/A"),
                    weed.optString("identification", "N/A"),
                    weed.optString("habitat", "N/A"),
                    weed.optString("control_methods", "N/A"),
                    weed.optString("toxicity", "N/A"),
                    weed.optString("growth_season", "N/A")
                );
            }
            
            // Try case-insensitive match
            android.util.Log.d("WeedDetector", "No exact match, trying case-insensitive...");
            String lowerWeedName = weedName.toLowerCase();
            java.util.Iterator<String> keys = weeds.keys();
            while (keys.hasNext()) {
                String key = keys.next();
                if (key.toLowerCase().equals(lowerWeedName)) {
                    android.util.Log.d("WeedDetector", "Found case-insensitive match: " + key);
                    JSONObject weed = weeds.getJSONObject(key);
                    String scientificName = weed.optString("scientific_name", "N/A");
                    String description = weed.optString("description", "No description available");
                    android.util.Log.d("WeedDetector", "Scientific name: " + scientificName);
                    android.util.Log.d("WeedDetector", "Description length: " + description.length());
                    return new WeedInfo(
                        scientificName,
                        description,
                        weed.optString("family", "N/A"),
                        weed.optString("identification", "N/A"),
                        weed.optString("habitat", "N/A"),
                        weed.optString("control_methods", "N/A"),
                        weed.optString("toxicity", "N/A"),
                        weed.optString("growth_season", "N/A")
                    );
                }
            }
            
            android.util.Log.e("WeedDetector", "No match found for: " + weedName);
            // Log all available keys for debugging
            keys = weeds.keys();
            StringBuilder availableKeys = new StringBuilder("Available keys: ");
            while (keys.hasNext()) {
                availableKeys.append(keys.next()).append(", ");
            }
            android.util.Log.d("WeedDetector", availableKeys.toString());
            
        } catch (Exception e) {
            android.util.Log.e("WeedDetector", "Error getting weed info", e);
            e.printStackTrace();
        }
        return new WeedInfo("Unknown", "No information available", "", "", "", "", "", "");
    }
    
    private ByteBuffer preprocessImage(Bitmap bitmap) {
        Bitmap resized = Bitmap.createScaledBitmap(bitmap, IMG_SIZE, IMG_SIZE, true);
        ByteBuffer buffer = ByteBuffer.allocateDirect(4 * IMG_SIZE * IMG_SIZE * PIXEL_SIZE);
        buffer.order(ByteOrder.nativeOrder());
        
        int[] pixels = new int[IMG_SIZE * IMG_SIZE];
        resized.getPixels(pixels, 0, IMG_SIZE, 0, 0, IMG_SIZE, IMG_SIZE);
        
        for (int pixel : pixels) {
            buffer.putFloat(((pixel >> 16 & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
            buffer.putFloat(((pixel >> 8 & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
            buffer.putFloat(((pixel & 0xFF) - IMAGE_MEAN) / IMAGE_STD);
        }
        
        return buffer;
    }
    
    public void close() {
        if (interpreter != null) {
            interpreter.close();
        }
    }
    
    public static class WeedResult {
        public String name;
        public float confidence;
        public WeedInfo info;
        
        public WeedResult(String name, float confidence, WeedInfo info) {
            this.name = name;
            this.confidence = confidence;
            this.info = info;
        }
    }
    
    public static class WeedInfo {
        public String scientificName;
        public String description;
        public String family;
        public String identification;
        public String habitat;
        public String controlMethods;
        public String toxicity;
        public String growthSeason;
        
        public WeedInfo(String scientificName, String description, String family,
                       String identification, String habitat, String controlMethods,
                       String toxicity, String growthSeason) {
            this.scientificName = scientificName;
            this.description = description;
            this.family = family;
            this.identification = identification;
            this.habitat = habitat;
            this.controlMethods = controlMethods;
            this.toxicity = toxicity;
            this.growthSeason = growthSeason;
        }
    }
}
