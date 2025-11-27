#!/usr/bin/env python3
"""
Quick start script for spacecraft-dynamics-control
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def demo_orbital_visualizer():
    """Demo the orbital visualizer"""
    try:
        from visualizations.python.advanced_plots.orbital_3d import OrbitalVisualizer3D
        
        print("🚀 Running Orbital Visualizer Demo...")
        visualizer = OrbitalVisualizer3D()
        
        # ISS-like orbit
        positions = visualizer.orbital_elements_to_cartesian(
            a=6771, e=0.001, i=51.6, raan=0, argp=0, nu=0
        )
        
        print(f"✅ Generated {len(positions)} orbital points")
        print("📍 First few positions:")
        for i in range(min(3, len(positions))):
            print(f"   Point {i}: {positions[i]}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Could not import orbital visualizer: {e}")
        return False

def demo_attitude_animator():
    """Demo the attitude animator"""
    try:
        from visualizations.python.advanced_plots.attitude_animations import AttitudeAnimator
        import numpy as np
        
        print("\n🛰️ Running Attitude Animator Demo...")
        animator = AttitudeAnimator()
        
        # Generate sample quaternion data (rotation about z-axis)
        time = np.linspace(0, 10, 5)  # Reduced points for demo
        angle = np.linspace(0, np.pi/2, 5)
        
        quaternions = []
        for t in angle:
            q = np.array([np.cos(t/2), 0, 0, np.sin(t/2)])
            quaternions.append(q)
        
        quaternions = np.array(quaternions)
        print(f"✅ Generated {len(quaternions)} attitude quaternions")
        print("📍 Quaternion examples:")
        for i in range(min(3, len(quaternions))):
            print(f"   Q{i}: {quaternions[i]}")
            
        return True
        
    except ImportError as e:
        print(f"❌ Could not import attitude animator: {e}")
        return False

if __name__ == "__main__":
    print("🌌 Spacecraft Dynamics & Control - Quick Start")
    print("=" * 50)
    
    success1 = demo_orbital_visualizer()
    success2 = demo_attitude_animator()
    
    if success1 or success2:
        print("\n🎉 Demo completed successfully!")
        print("\n📚 Available modules:")
        print("   • OrbitalVisualizer3D - 3D orbital trajectories")
        print("   • AttitudeAnimator - Spacecraft attitude animations") 
        print("   • PrecisePointingSimulator - Control system simulations")
    else:
        print("\n❌ Demo failed. Check installation.")
        print("💡 Make sure dependencies are installed and PYTHONPATH is set.")
