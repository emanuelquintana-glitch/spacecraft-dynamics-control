"""
Advanced 3D orbital visualizations for spacecraft dynamics
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class OrbitalVisualizer3D:
    """Advanced 3D visualizer for orbital mechanics"""
    
    def __init__(self, earth_radius=6371):
        self.earth_radius = earth_radius  # km
        
    def plot_keplerian_orbit(self, a, e, i, raan, argp, nu):
        """Plot Keplerian orbit in 3D"""
        # Convert orbital elements to Cartesian coordinates
        positions = self.orbital_elements_to_cartesian(a, e, i, raan, argp, nu)
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot Earth
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = self.earth_radius * np.outer(np.cos(u), np.sin(v))
        y = self.earth_radius * np.outer(np.sin(u), np.sin(v))
        z = self.earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
        
        ax.plot_surface(x, y, z, color='b', alpha=0.3)
        
        # Plot orbit
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 
                'r-', linewidth=2, label='Orbit')
        
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Y (km)')
        ax.set_zlabel('Z (km)')
        ax.legend()
        
        return fig, ax
    
    def orbital_elements_to_cartesian(self, a, e, i, raan, argp, nu):
        """Convert orbital elements to Cartesian coordinates"""
        n_points = 100
        true_anomaly = np.linspace(0, 2*np.pi, n_points)
        
        # Semi-latus rectum
        p = a * (1 - e**2)
        
        # Position in orbital plane
        r = p / (1 + e * np.cos(true_anomaly))
        x_orb = r * np.cos(true_anomaly)
        y_orb = r * np.sin(true_anomaly)
        
        # Convert to radians
        i_rad = np.radians(i)
        raan_rad = np.radians(raan)
        argp_rad = np.radians(argp)
        
        # Transformation matrix
        positions = np.zeros((n_points, 3))
        for idx, ta in enumerate(true_anomaly):
            # Position in perifocal frame
            r_pf = np.array([x_orb[idx], y_orb[idx], 0])
            
            # Rotation matrices
            R3_raan = np.array([
                [np.cos(raan_rad), -np.sin(raan_rad), 0],
                [np.sin(raan_rad), np.cos(raan_rad), 0],
                [0, 0, 1]
            ])
            
            R1_i = np.array([
                [1, 0, 0],
                [0, np.cos(i_rad), -np.sin(i_rad)],
                [0, np.sin(i_rad), np.cos(i_rad)]
            ])
            
            R3_argp = np.array([
                [np.cos(argp_rad), -np.sin(argp_rad), 0],
                [np.sin(argp_rad), np.cos(argp_rad), 0],
                [0, 0, 1]
            ])
            
            # Combined rotation
            R = R3_raan @ R1_i @ R3_argp
            positions[idx] = R @ r_pf
        
        return positions
    
    def create_interactive_plot(self, positions, title="3D Orbital Trajectory"):
        """Create interactive 3D plot using Plotly"""
        fig = go.Figure()
        
        # Add Earth
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=20, color='blue', opacity=0.8),
            name='Earth'
        ))
        
        # Add trajectory
        x, y, z = positions[:, 0], positions[:, 1], positions[:, 2]
        fig.add_trace(go.Scatter3d(
            x=x, y=y, z=z,
            mode='lines',
            line=dict(color='red', width=6),
            name='Orbit'
        ))
        
        fig.update_layout(
            title=title,
            scene=dict(
                xaxis_title='X (km)',
                yaxis_title='Y (km)',
                zaxis_title='Z (km)',
                aspectmode='data'
            )
        )
        
        return fig

if __name__ == "__main__":
    # Example usage
    visualizer = OrbitalVisualizer3D()
    
    # Example orbital elements (ISS-like orbit)
    a = 6771  # km
    e = 0.001
    i = 51.6  # degrees
    raan = 0
    argp = 0
    nu = 0
    
    fig, ax = visualizer.plot_keplerian_orbit(a, e, i, raan, argp, nu)
    plt.savefig('orbit_example.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create interactive version
    positions = visualizer.orbital_elements_to_cartesian(a, e, i, raan, argp, nu)
    fig_interactive = visualizer.create_interactive_plot(positions)
    fig_interactive.write_html('orbit_interactive.html')
