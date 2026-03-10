"""
Helper script to download weed images from online sources
Requires: pip install requests pillow
"""

import os
import requests
from PIL import Image
from io import BytesIO
import time

def download_image(url, save_path):
    """Download and save an image from URL"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize if too large
            if img.width > 1024 or img.height > 1024:
                img.thumbnail((1024, 1024), Image.Resampling.LANCZOS)
            img.save(save_path, 'JPEG', quality=95)
            return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return False

def create_dataset_structure(base_dir='dataset/weeds'):
    """Create folder structure for all weed types"""
    weed_types = [
        'dandelion', 'crabgrass', 'bindweed', 'chickweed', 'purslane',
        'clover', 'plantain', 'lambsquarters', 'nutsedge', 'pigweed',
        'quackgrass', 'ragweed', 'thistle', 'spurge', 'oxalis'
    ]
    
    for weed in weed_types:
        path = os.path.join(base_dir, weed)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}")

def download_from_inaturalist_api(weed_name, scientific_name, output_dir, max_images=100):
    """
    Download images from iNaturalist API
    Note: This is a simplified example. For production use, implement proper API authentication
    """
    print(f"\nDownloading {weed_name} images...")
    
    # iNaturalist API endpoint (simplified - check their API docs for full implementation)
    # This is a placeholder - you'll need to implement actual API calls
    print(f"To download from iNaturalist:")
    print(f"1. Visit: https://www.inaturalist.org/taxa/search?q={scientific_name.replace(' ', '+')}")
    print(f"2. Browse observations and download images manually")
    print(f"3. Save to: {output_dir}")
    print(f"4. Or use their API with proper authentication")

def manual_download_guide():
    """Print guide for manual image collection"""
    print("\n" + "="*60)
    print("MANUAL IMAGE COLLECTION GUIDE")
    print("="*60)
    
    print("\n1. INATURALIST (Best source)")
    print("   - Visit: https://www.inaturalist.org")
    print("   - Search for weed scientific name")
    print("   - Filter by 'Research Grade' observations")
    print("   - Download images (check license - use CC0, CC-BY)")
    
    print("\n2. GOOGLE IMAGES")
    print("   - Search: '[weed name] plant identification'")
    print("   - Tools > Usage Rights > Creative Commons licenses")
    print("   - Download and verify accuracy")
    
    print("\n3. PLANTNET")
    print("   - Visit: https://plantnet.org")
    print("   - Search by scientific name")
    print("   - Download verified observations")
    
    print("\n4. KAGGLE DATASETS")
    print("   - Visit: https://www.kaggle.com/datasets")
    print("   - Search: 'weed detection dataset'")
    print("   - Download and extract to dataset folder")
    
    print("\n5. TAKE YOUR OWN PHOTOS (RECOMMENDED)")
    print("   - Most accurate for your region")
    print("   - Use your smartphone")
    print("   - Follow guidelines in dataset_guide.md")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    print("Weed Dataset Downloader")
    print("="*60)
    
    # Create folder structure
    create_dataset_structure()
    
    # Show manual download guide
    manual_download_guide()
    
    print("\n\nRECOMMENDATION:")
    print("For best accuracy, combine:")
    print("  - 50% your own photos (real-world conditions)")
    print("  - 50% online images (variety and volume)")
    print("\nAim for 200+ images per weed type for 90%+ accuracy")
