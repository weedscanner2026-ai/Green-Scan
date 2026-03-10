"""
Dataset validation script - Run before training to catch issues early
"""

import os
from PIL import Image
import hashlib
from collections import defaultdict

def validate_dataset(data_dir='dataset/weeds'):
    """Comprehensive dataset validation"""
    print("\n" + "="*60)
    print("DATASET VALIDATION")
    print("="*60)
    
    if not os.path.exists(data_dir):
        print(f"\n❌ Dataset directory not found: {data_dir}")
        print("Run: python create_dataset_folders.py")
        return False
    
    issues = []
    warnings = []
    stats = defaultdict(lambda: {'count': 0, 'corrupted': 0, 'duplicates': 0})
    image_hashes = defaultdict(list)
    
    # Get all weed folders
    weed_folders = [f for f in os.listdir(data_dir) 
                   if os.path.isdir(os.path.join(data_dir, f))]
    
    if len(weed_folders) == 0:
        print(f"\n❌ No weed folders found in {data_dir}")
        return False
    
    print(f"\nValidating {len(weed_folders)} weed types...")
    print("-"*60)
    
    # Validate each weed folder
    for weed in sorted(weed_folders):
        weed_path = os.path.join(data_dir, weed)
        image_files = [f for f in os.listdir(weed_path) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
        
        stats[weed]['count'] = len(image_files)
        
        # Check minimum images
        if len(image_files) < 50:
            issues.append(f"{weed}: Only {len(image_files)} images (need 100+ for good accuracy)")
        elif len(image_files) < 100:
            warnings.append(f"{weed}: {len(image_files)} images (recommend 200+ for best accuracy)")
        
        # Validate each image
        for img_file in image_files:
            img_path = os.path.join(weed_path, img_file)
            
            try:
                # Try to open and verify image
                with Image.open(img_path) as img:
                    img.verify()
                
                # Reopen for hash (verify closes the file)
                with Image.open(img_path) as img:
                    # Check image size
                    if img.width < 100 or img.height < 100:
                        warnings.append(f"{weed}/{img_file}: Very small image ({img.width}x{img.height})")
                    
                    # Calculate hash for duplicate detection
                    img_hash = hashlib.md5(img.tobytes()).hexdigest()
                    image_hashes[img_hash].append(f"{weed}/{img_file}")
                    
            except Exception as e:
                stats[weed]['corrupted'] += 1
                issues.append(f"{weed}/{img_file}: Corrupted or invalid ({str(e)})")
        
        # Print stats for this weed
        status = "✓" if len(image_files) >= 100 else "⚠" if len(image_files) >= 50 else "❌"
        print(f"{status} {weed:20s}: {len(image_files):4d} images")
    
    # Check for duplicates
    print("\n" + "-"*60)
    print("Checking for duplicate images...")
    duplicate_count = 0
    for img_hash, paths in image_hashes.items():
        if len(paths) > 1:
            duplicate_count += len(paths) - 1
            warnings.append(f"Duplicate images found: {', '.join(paths[:3])}")
            for weed in [p.split('/')[0] for p in paths]:
                stats[weed]['duplicates'] += 1
    
    if duplicate_count > 0:
        print(f"⚠ Found {duplicate_count} duplicate images")
    else:
        print("✓ No duplicates found")
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    total_images = sum(s['count'] for s in stats.values())
    total_corrupted = sum(s['corrupted'] for s in stats.values())
    
    print(f"\nTotal weed types: {len(weed_folders)}")
    print(f"Total images: {total_images}")
    print(f"Corrupted images: {total_corrupted}")
    print(f"Duplicate images: {duplicate_count}")
    
    # Check class balance
    counts = [s['count'] for s in stats.values()]
    if counts:
        min_count = min(counts)
        max_count = max(counts)
        imbalance_ratio = max_count / min_count if min_count > 0 else float('inf')
        
        if imbalance_ratio > 3:
            warnings.append(f"Class imbalance detected: {max_count} vs {min_count} images (ratio: {imbalance_ratio:.1f}x)")
    
    # Print issues
    if issues:
        print(f"\n❌ ISSUES FOUND ({len(issues)}):")
        for issue in issues[:10]:  # Show first 10
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... and {len(issues)-10} more")
    
    if warnings:
        print(f"\n⚠ WARNINGS ({len(warnings)}):")
        for warning in warnings[:10]:  # Show first 10
            print(f"   - {warning}")
        if len(warnings) > 10:
            print(f"   ... and {len(warnings)-10} more")
    
    # Final verdict
    print("\n" + "="*60)
    if len(issues) == 0:
        print("✓ VALIDATION PASSED")
        print("\nDataset is ready for training!")
        if warnings:
            print("Note: Some warnings were found but won't prevent training.")
        return True
    else:
        print("❌ VALIDATION FAILED")
        print("\nPlease fix the issues above before training.")
        return False

if __name__ == "__main__":
    success = validate_dataset()
    exit(0 if success else 1)
