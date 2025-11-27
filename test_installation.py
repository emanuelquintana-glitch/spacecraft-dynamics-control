#!/usr/bin/env python3
"""
Test script to verify the installation and basic functionality
"""

try:
    import numpy as np
    import matplotlib.pyplot as plt
    from visualizations.python.advanced_plots.orbital_3d import OrbitalVisualizer3D
    
    print("✅ All imports successful!")
    
    # Test basic functionality
    visualizer = OrbitalVisualizer3D()
    print("✅ OrbitalVisualizer3D instantiated successfully!")
    
    # Test orbital elements conversion
    positions = visualizer.orbital_elements_to_cartesian(6771, 0.001, 51.6, 0, 0, 0)
    print(f"✅ Orbital elements conversion successful! Generated {len(positions)} points")
    
    print("\n🎉 Installation test passed! Everything is working correctly.")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please check your installation and dependencies.")
    
except Exception as e:
    print(f"❌ Error during testing: {e}")
