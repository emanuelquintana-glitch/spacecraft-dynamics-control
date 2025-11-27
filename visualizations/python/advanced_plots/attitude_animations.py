"""
Attitude animation visualizations for spacecraft dynamics
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class AttitudeAnimator:
    """Animator for spacecraft attitude dynamics"""
    
    def __init__(self):
        self.fig = None
        self.ax = None
        
    def animate_quaternion_evolution(self, time, quaternions):
        """Animate the evolution of quaternions over time"""
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Set up the coordinate axes
        self._setup_reference_frame(ax)
        
        def update(frame):
            ax.clear()
            self._setup_reference_frame(ax)
            
            # Get current quaternion
            q = quaternions[frame]
            
            # Convert quaternion to rotation matrix
            R = self.quaternion_to_rotation_matrix(q)
            
            # Draw spacecraft body axes
            self._draw_body_axes(ax, R)
            
            ax.set_title(f'Time: {time[frame]:.2f}s')
            
        anim = FuncAnimation(fig, update, frames=len(time), 
                           interval=50, blit=False, repeat=True)
        
        return anim
    
    def quaternion_to_rotation_matrix(self, q):
        """Convert quaternion to rotation matrix"""
        q0, q1, q2, q3 = q
        
        R = np.array([
            [1-2*(q2**2 + q3**2), 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
            [2*(q1*q2 + q0*q3), 1-2*(q1**2 + q3**2), 2*(q2*q3 - q0*q1)],
            [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), 1-2*(q1**2 + q2**2)]
        ])
        
        return R
    
    def _setup_reference_frame(self, ax):
        """Set up the reference coordinate system"""
        # Reference axes (ECI frame)
        ax.quiver(0, 0, 0, 1, 0, 0, color='r', label='X', linewidth=2)
        ax.quiver(0, 0, 0, 0, 1, 0, color='g', label='Y', linewidth=2)
        ax.quiver(0, 0, 0, 0, 0, 1, color='b', label='Z', linewidth=2)
        
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
    
    def _draw_body_axes(self, ax, rotation_matrix):
        """Draw spacecraft body axes"""
        # Body axes in body frame
        body_x = rotation_matrix @ np.array([1, 0, 0])
        body_y = rotation_matrix @ np.array([0, 1, 0])
        body_z = rotation_matrix @ np.array([0, 0, 1])
        
        # Draw body axes
        ax.quiver(0, 0, 0, body_x[0], body_x[1], body_x[2], 
                 color='r', linewidth=3, alpha=0.7, label='Body X')
        ax.quiver(0, 0, 0, body_y[0], body_y[1], body_y[2], 
                 color='g', linewidth=3, alpha=0.7, label='Body Y')
        ax.quiver(0, 0, 0, body_z[0], body_z[1], body_z[2], 
                 color='b', linewidth=3, alpha=0.7, label='Body Z')

if __name__ == "__main__":
    # Example usage
    animator = AttitudeAnimator()
    
    # Generate sample data (simple rotation about z-axis)
    time = np.linspace(0, 10, 100)
    angle = np.linspace(0, 2*np.pi, 100)
    
    quaternions = []
    for t in angle:
        q = np.array([np.cos(t/2), 0, 0, np.sin(t/2)])  # Rotation about z-axis
        quaternions.append(q)
    
    quaternions = np.array(quaternions)
    
    # Create animation
    anim = animator.animate_quaternion_evolution(time, quaternions)
    plt.show()
