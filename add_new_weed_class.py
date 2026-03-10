"""
Add New Weed Class to Dataset
This script helps you add a new weed species to your training dataset
"""

import os
import json
from pathlib import Path

def create_weed_folder(weed_name):
    """Create a new folder for a weed class"""
    # Sanitize the weed name (lowercase, replace spaces with underscores)
    folder_name = weed_name.lower().replace(' ', '_').replace('-', '_')
    
    # Create the folder path
    dataset_path = Path('dataset/weeds') / folder_name
    
    if dataset_path.exists():
        print(f"⚠️  Folder '{folder_name}' already exists!")
        return folder_name, False
    
    # Create the folder
    dataset_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created folder: {dataset_path}")
    
    return folder_name, True

def add_weed_info(weed_name, folder_name):
    """Add weed information to weed_info.json"""
    
    print("\n" + "="*60)
    print("WEED INFORMATION")
    print("="*60)
    print("Please provide information about this weed:")
    print("(Press Enter to skip optional fields)")
    print()
    
    # Get weed information from user
    scientific_name = input("Scientific Name (e.g., Digitaria sanguinalis): ").strip()
    common_names = input("Common Names (comma-separated, e.g., Crabgrass, Damong-alat): ").strip()
    family = input("Plant Family (e.g., Poaceae): ").strip()
    description = input("Description: ").strip()
    identification = input("How to Identify: ").strip()
    habitat = input("Habitat: ").strip()
    control_methods = input("Control Methods: ").strip()
    toxicity = input("Toxicity (e.g., Non-toxic): ").strip()
    growth_season = input("Growth Season: ").strip()
    
    # Create weed info entry
    weed_info = {
        "scientific_name": scientific_name or "Unknown",
        "common_names": [name.strip() for name in common_names.split(',')] if common_names else [weed_name],
        "family": family or "Unknown",
        "description": description or f"{weed_name} is a common weed species.",
        "identification": identification or "Identification details to be added.",
        "habitat": habitat or "Various habitats",
        "control_methods": control_methods or "Hand pulling, herbicides",
        "toxicity": toxicity or "Unknown",
        "growth_season": growth_season or "Year-round"
    }
    
    # Load existing weed_info.json
    info_file = Path('weed_info.json')
    
    if info_file.exists():
        with open(info_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"weeds": {}}
    
    # Add new weed info
    data['weeds'][folder_name] = weed_info
    
    # Save updated weed_info.json
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Added weed information to weed_info.json")

def show_instructions(folder_name):
    """Show instructions for adding images"""
    dataset_path = Path('dataset/weeds') / folder_name
    
    print("\n" + "="*60)
    print("NEXT STEPS")
    print("="*60)
    print(f"\n1. Add images to: {dataset_path.absolute()}")
    print("\n   Recommended:")
    print("   • Minimum: 200 images")
    print("   • Optimal: 500-1000 images")
    print("   • Format: JPG or PNG")
    print("   • Quality: Clear, well-lit photos")
    print("\n2. Image Guidelines:")
    print("   • Take photos from different angles")
    print("   • Include close-ups and full plant shots")
    print("   • Vary lighting conditions")
    print("   • Include different growth stages")
    print("   • Avoid blurry or dark images")
    print("\n3. After adding images, retrain the model:")
    print("   • Option A: Run in terminal:")
    print("     python train_model.py")
    print("   • Option B: Use admin panel:")
    print("     python unified_admin_server.py")
    print("     Go to Model Training page")
    print("\n4. Update Android app:")
    print("   • Copy new model files to app")
    print("   • Rebuild and test")
    print("\n" + "="*60)

def main():
    print("="*60)
    print("ADD NEW WEED CLASS TO DATASET")
    print("="*60)
    print()
    
    # Get weed name
    weed_name = input("Enter the weed name (e.g., Cogon Grass): ").strip()
    
    if not weed_name:
        print("❌ Weed name cannot be empty!")
        return
    
    # Create folder
    folder_name, created = create_weed_folder(weed_name)
    
    if not created:
        choice = input("Do you want to update the information? (y/n): ").lower()
        if choice != 'y':
            print("Cancelled.")
            return
    
    # Add weed information
    add_weed_info(weed_name, folder_name)
    
    # Show instructions
    show_instructions(folder_name)
    
    print("\n✓ Setup complete!")
    print(f"✓ Folder created: dataset/weeds/{folder_name}")
    print(f"✓ Information added to weed_info.json")
    print("\nNow add images to the folder and retrain the model!")

if __name__ == "__main__":
    main()
