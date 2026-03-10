"""
Quick script to create dataset folder structure for Philippine weeds
"""

import os

# Philippine weeds list
philippine_weeds = [
    'crabgrass',
    'morsikos',
    'paragis',
    'teki',
    'makahiya',
    'kulitis',
    'talahib',
    'damong-maria',
    'tawa-tawa',
    'kangkong-aso',
    'ulasiman-bato',
    'alusiman',
    'halamang-aso',
    'sabila-sabila',
    'botoncillo'
]

def create_folders(base_dir='dataset/weeds'):
    """Create folder structure for all Philippine weeds"""
    print("Creating dataset folder structure...")
    print("="*60)
    
    for weed in philippine_weeds:
        path = os.path.join(base_dir, weed)
        os.makedirs(path, exist_ok=True)
        print(f"✓ Created: {path}")
    
    print("="*60)
    print(f"\nFolder structure created successfully!")
    print(f"\nNext steps:")
    print("1. Read 'dataset_guide_philippines.md' for collection tips")
    print("2. Start collecting photos for each weed type")
    print("3. Aim for 200+ images per weed")
    print("4. Save images in respective folders")
    print("5. Run 'python train_model.py' when ready")
    
    print(f"\n📁 Your dataset folders:")
    for weed in philippine_weeds:
        print(f"   dataset/weeds/{weed}/")

if __name__ == "__main__":
    create_folders()
