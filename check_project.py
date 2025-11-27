#!/usr/bin/env python3
"""
Comprehensive project verification script
"""

import os
import sys

def check_file_completeness(filepath):
    """Check if a Python file is properly terminated"""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if lines and "EOF" in lines[-1]:
                return False, "File ends with EOF marker"
            return True, "Complete"
    except Exception as e:
        return False, f"Error reading file: {e}"

def main():
    print("🔍 Verifying spacecraft-dynamics-control project...")
    
    # Check critical files
    critical_files = [
        'requirements.txt',
        'pyproject.toml', 
        'setup.py',
        'README.md',
        '.gitignore',
        'test_installation.py'
    ]
    
    print("\n📁 Critical files check:")
    all_good = True
    for file in critical_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            all_good = False
    
    # Check Python files
    print("\n🐍 Python files check:")
    python_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    for py_file in python_files:
        complete, message = check_file_completeness(py_file)
        status = "✅" if complete else "❌"
        print(f"  {status} {py_file}: {message}")
        if not complete:
            all_good = False
    
    # Check imports
    print("\n📦 Import check:")
    try:
        from visualizations.python.advanced_plots.orbital_3d import OrbitalVisualizer3D
        from visualizations.python.advanced_plots.attitude_animations import AttitudeAnimator
        print("  ✅ All imports successful")
    except ImportError as e:
        print(f"  ❌ Import failed: {e}")
        all_good = False
    
    # Final result
    print(f"\n{'🎉 PROJECT VERIFICATION PASSED' if all_good else '❌ PROJECT HAS ISSUES'}")
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main())
