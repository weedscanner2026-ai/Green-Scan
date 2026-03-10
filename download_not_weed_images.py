"""
Download non-weed images to train the model to recognize what is NOT a weed.
This helps reduce false positives on random objects.
"""

import os
import requests
from pathlib import Path
import time

def download_image(url, filepath):
    """Download an image from URL to filepath"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=15, headers=headers)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"✓ Downloaded: {filepath.name}")
            return True
    except Exception as e:
        print(f"✗ Failed: {filepath.name}")
    return False

def main():
    # Create not_weed directory
    not_weed_dir = Path("dataset/weeds/not_weed")
    not_weed_dir.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("DOWNLOADING NON-WEED IMAGES FOR TRAINING")
    print("=" * 70)
    print("\nThis will download images of:")
    print("• Grass (lawn grass)")
    print("• Flowers (roses, sunflowers, etc.)")
    print("• Crops (rice, corn, vegetables)")
    print("• Soil and ground")
    print("• Common objects (phones, laptops, books)")
    print("• Leaves and trees")
    print("\nThese help the model learn what is NOT a weed.")
    print("=" * 70)
    
    # Free image URLs from Unsplash (no API key needed for direct links)
    # These are sample images - Unsplash allows hotlinking for development
    image_urls = [
        # Grass images
        ("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80", "grass_01.jpg"),
        ("https://images.unsplash.com/photo-1560493676-04071c5f467b?w=400&q=80", "grass_02.jpg"),
        ("https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=400&q=80", "grass_03.jpg"),
        ("https://images.unsplash.com/photo-1592419044706-39796d40f98c?w=400&q=80", "grass_04.jpg"),
        ("https://images.unsplash.com/photo-1587897773780-fe72528d5081?w=400&q=80", "grass_05.jpg"),
        
        # Flowers
        ("https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=400&q=80", "flower_01.jpg"),
        ("https://images.unsplash.com/photo-1462275646964-a0e3386b89fa?w=400&q=80", "flower_02.jpg"),
        ("https://images.unsplash.com/photo-1464146072230-91cabc968266?w=400&q=80", "flower_03.jpg"),
        ("https://images.unsplash.com/photo-1470058869958-2a77ade41c02?w=400&q=80", "flower_04.jpg"),
        ("https://images.unsplash.com/photo-1463852247062-1bbca38f7805?w=400&q=80", "flower_05.jpg"),
        ("https://images.unsplash.com/photo-1469259943454-aa100abba749?w=400&q=80", "flower_06.jpg"),
        ("https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=400&q=80", "flower_07.jpg"),
        
        # Rice plants
        ("https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=400&q=80", "rice_01.jpg"),
        ("https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?w=400&q=80", "rice_02.jpg"),
        ("https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?w=400&q=80", "rice_03.jpg"),
        ("https://images.unsplash.com/photo-1594241497197-4c8c8e0d3e3f?w=400&q=80", "rice_04.jpg"),
        
        # Corn/crops
        ("https://images.unsplash.com/photo-1603048588665-791ca8aea617?w=400&q=80", "corn_01.jpg"),
        ("https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&q=80", "corn_02.jpg"),
        ("https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&q=80", "crop_01.jpg"),
        
        # Soil/ground
        ("https://images.unsplash.com/photo-1464226184884-fa280b87c399?w=400&q=80", "soil_01.jpg"),
        ("https://images.unsplash.com/photo-1628352081506-83c43123ed6d?w=400&q=80", "soil_02.jpg"),
        ("https://images.unsplash.com/photo-1615671524827-c1fe3973b648?w=400&q=80", "soil_03.jpg"),
        
        # Vegetables
        ("https://images.unsplash.com/photo-1597362925123-77861d3fbac7?w=400&q=80", "vegetable_01.jpg"),
        ("https://images.unsplash.com/photo-1566385101042-1a0aa0c1268c?w=400&q=80", "vegetable_02.jpg"),
        ("https://images.unsplash.com/photo-1590779033100-9f60a05a013d?w=400&q=80", "vegetable_03.jpg"),
        
        # Trees/leaves
        ("https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?w=400&q=80", "tree_01.jpg"),
        ("https://images.unsplash.com/photo-1502082553048-f009c37129b9?w=400&q=80", "tree_02.jpg"),
        ("https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?w=400&q=80", "leaves_01.jpg"),
        
        # Common objects (phones, laptops, etc.)
        ("https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&q=80", "phone_01.jpg"),
        ("https://images.unsplash.com/photo-1484788984921-03950022c9ef?w=400&q=80", "laptop_01.jpg"),
        ("https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400&q=80", "book_01.jpg"),
        ("https://images.unsplash.com/photo-1497633762265-9d179a990aa6?w=400&q=80", "book_02.jpg"),
        
        # Pavement/concrete
        ("https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&q=80", "pavement_01.jpg"),
        ("https://images.unsplash.com/photo-1604537466158-719b1972feb8?w=400&q=80", "concrete_01.jpg"),
    ]
    
    print(f"\nAttempting to download {len(image_urls)} images...")
    print("This may take a few minutes...\n")
    
    success_count = 0
    
    for i, (url, filename) in enumerate(image_urls, 1):
        filepath = not_weed_dir / filename
        print(f"[{i}/{len(image_urls)}] ", end="")
        
        if download_image(url, filepath):
            success_count += 1
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    print("\n" + "=" * 70)
    print(f"✓ Successfully downloaded {success_count}/{len(image_urls)} images")
    print(f"\nImages saved to: {not_weed_dir.absolute()}")
    print("\n" + "=" * 70)
    
    if success_count < 20:
        print("\n⚠️  WARNING: Only a few images downloaded successfully.")
        print("This might not be enough for good training.")
        print("\nRECOMMENDATION:")
        print("1. Check your internet connection")
        print("2. Try running the script again")
        print("3. Manually add more images to the folder")
    else:
        print("\n✓ Good! You have enough images to start training.")
        print("\nNEXT STEPS:")
        print("1. Run: python train_model.py")
        print("2. Copy new model files to Android app")
        print("3. Rebuild and test the app")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
