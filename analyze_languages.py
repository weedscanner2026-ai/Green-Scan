import os
import pathlib

def count_lines(file_path):
    """Count non-empty lines in a file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for line in f if line.strip())
    except:
        return 0

def analyze_project():
    language_stats = {
        'Java': {'extensions': ['.java'], 'lines': 0, 'files': 0},
        'Python': {'extensions': ['.py'], 'lines': 0, 'files': 0},
        'XML': {'extensions': ['.xml'], 'lines': 0, 'files': 0},
        'HTML': {'extensions': ['.html'], 'lines': 0, 'files': 0},
        'CSS': {'extensions': ['.css'], 'lines': 0, 'files': 0},
        'JavaScript': {'extensions': ['.js'], 'lines': 0, 'files': 0},
        'JSON': {'extensions': ['.json'], 'lines': 0, 'files': 0},
        'Gradle': {'extensions': ['.gradle'], 'lines': 0, 'files': 0},
    }
    
    # Directories to exclude
    exclude_dirs = {'.git', '__pycache__', 'node_modules', '.idea', 'build', 
                   '.gradle', 'dataset', 'models', 'venv', 'env'}
    
    # Walk through project
    for root, dirs, files in os.walk('.'):
        # Remove excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = pathlib.Path(file).suffix.lower()
            
            # Count lines for each language
            for lang, info in language_stats.items():
                if ext in info['extensions']:
                    lines = count_lines(file_path)
                    info['lines'] += lines
                    info['files'] += 1
                    break
    
    # Calculate totals
    total_lines = sum(info['lines'] for info in language_stats.values())
    
    print("=" * 70)
    print("PROJECT LANGUAGE STATISTICS")
    print("=" * 70)
    print(f"\nTotal Lines of Code: {total_lines:,}\n")
    
    # Sort by lines of code
    sorted_langs = sorted(language_stats.items(), 
                         key=lambda x: x[1]['lines'], 
                         reverse=True)
    
    print(f"{'Language':<15} {'Files':<8} {'Lines':<12} {'Percentage':<12}")
    print("-" * 70)
    
    for lang, info in sorted_langs:
        if info['lines'] > 0:
            percentage = (info['lines'] / total_lines * 100) if total_lines > 0 else 0
            print(f"{lang:<15} {info['files']:<8} {info['lines']:<12,} {percentage:>6.2f}%")
    
    print("=" * 70)
    
    # Summary by category
    print("\nCATEGORY BREAKDOWN:")
    print("-" * 70)
    
    backend = language_stats['Python']['lines']
    mobile = language_stats['Java']['lines']
    frontend = (language_stats['HTML']['lines'] + 
                language_stats['CSS']['lines'] + 
                language_stats['JavaScript']['lines'])
    config = (language_stats['XML']['lines'] + 
              language_stats['JSON']['lines'] + 
              language_stats['Gradle']['lines'])
    
    print(f"Backend (Python):           {backend:>8,} lines ({backend/total_lines*100:>5.1f}%)")
    print(f"Mobile App (Java):          {mobile:>8,} lines ({mobile/total_lines*100:>5.1f}%)")
    print(f"Frontend (HTML/CSS/JS):     {frontend:>8,} lines ({frontend/total_lines*100:>5.1f}%)")
    print(f"Config (XML/JSON/Gradle):   {config:>8,} lines ({config/total_lines*100:>5.1f}%)")
    print("=" * 70)

if __name__ == "__main__":
    analyze_project()
