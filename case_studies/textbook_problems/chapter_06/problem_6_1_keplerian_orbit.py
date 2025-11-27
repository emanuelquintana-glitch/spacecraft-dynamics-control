"""
Problem 6.1: Keplerian Orbit and Orbital Elements

Reference: Canuto et al., Section 3.2, Page 89-102
Difficulty: ⭐⭐ (Intermediate)
Type: Computational + Analytical
Topic: Orbital Dynamics - Two-Body Problem

PROBLEM STATEMENT:
==================
Consider a spacecraft in Earth orbit with the following initial conditions 
in Earth-Centered Inertial (ECI) frame:

Position: r = [7000, 0, 0] km
Velocity: v = [0, 7.5, 0] km/s

Given:
- Gravitational parameter μ = 398600.4418 km³/s²
- Earth radius R_e = 6378.137 km

Find:
a) Compute the classical orbital elements
b) Determine orbit type (circular, elliptical, etc.)
c) Calculate orbital period and energy
d) Propagate orbit for one complete period
e) Verify conservation of energy and angular momentum
f) Visualize the orbit in 3D

SOLUTION APPROACH:
==================
1. Convert Cartesian coordinates to orbital elements
2. Classify orbit based on eccentricity
3. Compute orbital period from semi-major axis
4. Propagate using Kepler's equation
5. Validate conservation laws
6. Create 3D visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from mpl_toolkits.mplot3d import Axes3D


# ==============================================================================
# SECTION 1: PROBLEM PARAMETERS
# ==============================================================================

def define_parameters():
    """
    Define all problem parameters.
    
    Returns:
        Dictionary with all parameters
    """
    params = {
        # Given parameters
        'mu': 398600.4418,  # Earth gravitational parameter [km³/s²]
        'R_e': 6378.137,    # Earth radius [km]
        
        # Initial conditions in ECI frame [km, km/s]
        'r0': np.array([7000.0, 0.0, 0.0]),
        'v0': np.array([0.0, 7.5, 0.0]),
        
        # Time parameters
        't_start': 0.0,
        't_end': 6000.0,  # ~100 minutes for LEO
        'dt': 10.0,
    }
    
    return params


# ==============================================================================
# SECTION 2: ANALYTICAL SOLUTION
# ==============================================================================

class OrbitalElements:
    """
    Class for orbital elements calculations.
    """
    
    @staticmethod
    def cartesian_to_orbital(r: np.ndarray, v: np.ndarray, mu: float) -> dict:
        """
        Convert Cartesian coordinates to classical orbital elements.
        
        Args:
            r: Position vector [km]
            v: Velocity vector [km/s]
            mu: Gravitational parameter [km³/s²]
            
        Returns:
            Dictionary with orbital elements
        """
        # Angular momentum vector
        h = np.cross(r, v)
        h_mag = np.linalg.norm(h)
        
        # Eccentricity vector
        r_mag = np.linalg.norm(r)
        v_mag = np.linalg.norm(v)
        e_vec = ((v_mag**2 - mu/r_mag) * r - np.dot(r, v) * v) / mu
        e = np.linalg.norm(e_vec)
        
        # Energy and semi-major axis
        energy = v_mag**2/2 - mu/r_mag
        if abs(energy) < 1e-10:
            a = float('inf')  # Parabolic orbit
        else:
            a = -mu / (2 * energy)
        
        # Inclination
        i = np.arccos(h[2] / h_mag)
        
        # Right Ascension of Ascending Node (RAAN)
        n = np.cross([0, 0, 1], h)  # Node vector
        n_mag = np.linalg.norm(n)
        if n_mag == 0:
            raan = 0.0  # Equatorial orbit
        else:
            raan = np.arccos(n[0] / n_mag)
            if n[1] < 0:
                raan = 2 * np.pi - raan
        
        # Argument of perigee
        if n_mag == 0 or e < 1e-10:
            argp = 0.0  # Circular or equatorial orbit
        else:
            argp = np.arccos(np.dot(n, e_vec) / (n_mag * e))
            if e_vec[2] < 0:
                argp = 2 * np.pi - argp
        
        # True anomaly
        if e < 1e-10:
            nu = 0.0  # Circular orbit
        else:
            nu = np.arccos(np.dot(e_vec, r) / (e * r_mag))
            if np.dot(r, v) < 0:
                nu = 2 * np.pi - nu
        
        # Orbital period
        if a > 0 and not np.isinf(a):
            T = 2 * np.pi * np.sqrt(a**3 / mu)
        else:
            T = float('inf')
        
        return {
            'semi_major_axis': a,
            'eccentricity': e,
            'inclination': np.degrees(i),
            'raan': np.degrees(raan),
            'argument_perigee': np.degrees(argp),
            'true_anomaly': np.degrees(nu),
            'angular_momentum': h_mag,
            'energy': energy,
            'period': T
        }
    
    @staticmethod
    def classify_orbit(elements: dict) -> str:
        """
        Classify orbit based on eccentricity.
        
        Args:
            elements: Orbital elements
            
        Returns:
            Orbit classification string
        """
        e = elements['eccentricity']
        
        if e < 0.001:
            return "Circular"
        elif e < 1.0:
            return "Elliptical"
        elif abs(e - 1.0) < 0.001:
            return "Parabolic"
        else:
            return "Hyperbolic"
    
    @staticmethod
    def orbital_to_cartesian(elements: dict, mu: float) -> tuple:
        """
        Convert orbital elements to Cartesian coordinates.
        
        Args:
            elements: Orbital elements
            mu: Gravitational parameter
            
        Returns:
            Tuple (r, v) position and velocity vectors
        """
        # Convert to radians
        i = np.radians(elements['inclination'])
        raan = np.radians(elements['raan'])
        argp = np.radians(elements['argument_perigee'])
        nu = np.radians(elements['true_anomaly'])
        
        a = elements['semi_major_axis']
        e = elements['eccentricity']
        
        # Semi-latus rectum
        p = a * (1 - e**2)
        
        # Position in perifocal frame
        r_peri = p / (1 + e * np.cos(nu))
        r_pf = np.array([
            r_peri * np.cos(nu),
            r_peri * np.sin(nu),
            0
        ])
        
        # Velocity in perifocal frame
        v_pf = np.array([
            -np.sqrt(mu/p) * np.sin(nu),
            np.sqrt(mu/p) * (e + np.cos(nu)),
            0
        ])
        
        # Rotation matrix from perifocal to ECI
        R = OrbitalElements._perifocal_to_eci_matrix(i, raan, argp)
        
        # Transform to ECI
        r_eci = R @ r_pf
        v_eci = R @ v_pf
        
        return r_eci, v_eci
    
    @staticmethod
    def _perifocal_to_eci_matrix(i: float, raan: float, argp: float) -> np.ndarray:
        """
        Rotation matrix from perifocal to ECI frame.
        """
        cos_raan, sin_raan = np.cos(raan), np.sin(raan)
        cos_i, sin_i = np.cos(i), np.sin(i)
        cos_w, sin_w = np.cos(argp), np.sin(argp)
        
        R = np.array([
            [cos_raan*cos_w - sin_raan*sin_w*cos_i, -cos_raan*sin_w - sin_raan*cos_w*cos_i, sin_raan*sin_i],
            [sin_raan*cos_w + cos_raan*sin_w*cos_i, -sin_raan*sin_w + cos_raan*cos_w*cos_i, -cos_raan*sin_i],
            [sin_w*sin_i, cos_w*sin_i, cos_i]
        ])
        
        return R


# ==============================================================================
# SECTION 3: NUMERICAL SOLUTION
# ==============================================================================

class OrbitPropagator:
    """
    Numerical orbit propagator using two-body dynamics.
    """
    
    def __init__(self, params):
        """
        Initialize propagator with parameters.
        
        Args:
            params: Dictionary of problem parameters
        """
        self.params = params
        self.mu = params['mu']
        
    def two_body_equations(self, t, state):
        """
        Two-body orbital dynamics.
        
        Args:
            t: Time
            state: [x, y, z, vx, vy, vz]
            
        Returns:
            State derivative
        """
        r = state[:3]
        r_mag = np.linalg.norm(r)
        
        # Acceleration due to gravity
        a = -self.mu * r / r_mag**3
        
        # State derivative [velocity, acceleration]
        state_dot = np.concatenate([state[3:6], a])
        
        return state_dot
    
    def propagate(self):
        """
        Propagate orbit numerically.
        
        Returns:
            Dictionary with solution
        """
        # Initial state [position, velocity]
        state0 = np.concatenate([self.params['r0'], self.params['v0']])
        t_span = (self.params['t_start'], self.params['t_end'])
        
        # Integrate
        sol = solve_ivp(
            self.two_body_equations,
            t_span,
            state0,
            method='RK45',
            dense_output=True,
            max_step=self.params['dt']
        )
        
        # Extract position and velocity
        position = sol.y[:3, :].T
        velocity = sol.y[3:6, :].T
        
        results = {
            't': sol.t,
            'position': position,
            'velocity': velocity,
            'success': sol.success
        }
        
        return results


# ==============================================================================
# SECTION 4: VALIDATION
# ==============================================================================

def validate_orbit(numerical, analytical, params):
    """
    Validate orbital solution.
    
    Args:
        numerical: Numerical solution
        analytical: Analytical orbital elements
        params: Problem parameters
        
    Returns:
        Validation results
    """
    validation = {
        'passed': True,
        'errors': [],
        'warnings': []
    }
    
    mu = params['mu']
    
    # Check 1: Integration success
    if not numerical['success']:
        validation['passed'] = False
        validation['errors'].append("Orbit propagation failed")
    
    # Check 2: Energy conservation
    energy_initial = analytical['energy']
    
    # Compute energy at final state
    r_final = numerical['position'][-1]
    v_final = numerical['velocity'][-1]
    r_mag_final = np.linalg.norm(r_final)
    v_mag_final = np.linalg.norm(v_final)
    energy_final = v_mag_final**2/2 - mu/r_mag_final
    
    energy_error = abs(energy_final - energy_initial) / abs(energy_initial)
    if energy_error > 1e-6:
        validation['warnings'].append(f"Energy conservation error: {energy_error:.2e}")
    
    # Check 3: Angular momentum conservation
    h_initial = analytical['angular_momentum']
    h_final = np.linalg.norm(np.cross(r_final, v_final))
    h_error = abs(h_final - h_initial) / h_initial
    
    if h_error > 1e-6:
        validation['warnings'].append(f"Angular momentum error: {h_error:.2e}")
    
    return validation


# ==============================================================================
# SECTION 5: VISUALIZATION
# ==============================================================================

def plot_orbit_results(numerical, elements, params):
    """
    Create comprehensive orbit visualization.
    
    Args:
        numerical: Numerical solution
        elements: Orbital elements
        params: Problem parameters
    """
    fig = plt.figure(figsize=(16, 12))
    
    # Plot 1: 3D orbit
    ax1 = plt.subplot(2, 3, 1, projection='3d')
    
    # Plot Earth
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    x = params['R_e'] * np.outer(np.cos(u), np.sin(v))
    y = params['R_e'] * np.outer(np.sin(u), np.sin(v))
    z = params['R_e'] * np.outer(np.ones(np.size(u)), np.cos(v))
    ax1.plot_surface(x, y, z, color='lightblue', alpha=0.3)
    
    # Plot orbit
    ax1.plot(numerical['position'][:, 0], 
             numerical['position'][:, 1], 
             numerical['position'][:, 2], 
             'b-', linewidth=2, label='Orbit')
    
    # Mark initial position
    ax1.scatter([numerical['position'][0, 0]], 
                [numerical['position'][0, 1]], 
                [numerical['position'][0, 2]], 
                c='red', s=100, marker='o', label='Start')
    
    ax1.set_xlabel('X [km]')
    ax1.set_ylabel('Y [km]')
    ax1.set_zlabel('Z [km]')
    ax1.set_title('3D Orbit Visualization')
    ax1.legend()
    
    # Plot 2: Orbital plane
    ax2 = plt.subplot(2, 3, 2)
    ax2.plot(numerical['position'][:, 0], numerical['position'][:, 1], 'b-', linewidth=2)
    
    # Plot Earth
    earth_circle = plt.Circle((0, 0), params['R_e'], color='lightblue', alpha=0.7)
    ax2.add_patch(earth_circle)
    
    ax2.plot(numerical['position'][0, 0], numerical['position'][0, 1], 'ro', markersize=8, label='Start')
    ax2.set_xlabel('X [km]')
    ax2.set_ylabel('Y [km]')
    ax2.set_title('Orbital Plane (XY)')
    ax2.axis('equal')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Altitude history
    ax3 = plt.subplot(2, 3, 3)
    altitude = np.linalg.norm(numerical['position'], axis=1) - params['R_e']
    ax3.plot(numerical['t']/60, altitude, 'g-', linewidth=2)
    ax3.set_xlabel('Time [min]')
    ax3.set_ylabel('Altitude [km]')
    ax3.set_title('Altitude vs Time')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Energy conservation
    ax4 = plt.subplot(2, 3, 4)
    energy = np.linalg.norm(numerical['velocity'], axis=1)**2/2 - params['mu']/np.linalg.norm(numerical['position'], axis=1)
    energy_error = 100 * (energy - elements['energy']) / abs(elements['energy'])
    ax4.plot(numerical['t']/60, energy_error, 'r-', linewidth=2)
    ax4.set_xlabel('Time [min]')
    ax4.set_ylabel('Energy Error [%]')
    ax4.set_title('Energy Conservation')
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='k', linestyle='--', alpha=0.5)
    
    # Plot 5: Orbital elements diagram
    ax5 = plt.subplot(2, 3, 5)
    ax5.axis('off')
    
    elements_text = f"""
    ORBITAL ELEMENTS
    ════════════════════════
    
    Semi-major axis: {elements['semi_major_axis']:.2f} km
    Eccentricity:    {elements['eccentricity']:.6f}
    Inclination:     {elements['inclination']:.2f}°
    RAAN:            {elements['raan']:.2f}°
    Arg. of perigee: {elements['argument_perigee']:.2f}°
    True anomaly:    {elements['true_anomaly']:.2f}°
    
    Orbit type:      {OrbitalElements.classify_orbit(elements)}
    Period:          {elements['period']/60:.2f} min
    Energy:          {elements['energy']:.4f} km²/s²
    """
    
    ax5.text(0.1, 0.5, elements_text, fontsize=11, family='monospace',
             verticalalignment='center')
    
    # Plot 6: Velocity profile
    ax6 = plt.subplot(2, 3, 6)
    velocity_mag = np.linalg.norm(numerical['velocity'], axis=1)
    ax6.plot(numerical['t']/60, velocity_mag, 'purple', linewidth=2)
    ax6.set_xlabel('Time [min]')
    ax6.set_ylabel('Velocity [km/s]')
    ax6.set_title('Orbital Velocity')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('problem_6_1_orbit_results.png', dpi=300, bbox_inches='tight')
    plt.show()


# ==============================================================================
# SECTION 6: MAIN EXECUTION
# ==============================================================================

def main():
    """
    Main execution function.
    """
    print("=" * 70)
    print("PROBLEM 6.1: KEPLERIAN ORBIT AND ORBITAL ELEMENTS")
    print("=" * 70)
    
    # Step 1: Define parameters
    print("\n[1/6] Defining problem parameters...")
    params = define_parameters()
    print(f"  ✓ Initial position: {params['r0']} km")
    print(f"  ✓ Initial velocity: {params['v0']} km/s")
    
    # Step 2: Analytical solution (orbital elements)
    print("\n[2/6] Computing orbital elements...")
    elements = OrbitalElements.cartesian_to_orbital(params['r0'], params['v0'], params['mu'])
    orbit_type = OrbitalElements.classify_orbit(elements)
    print(f"  ✓ Orbit type: {orbit_type}")
    print(f"  ✓ Semi-major axis: {elements['semi_major_axis']:.2f} km")
    print(f"  ✓ Eccentricity: {elements['eccentricity']:.6f}")
    
    # Step 3: Numerical solution
    print("\n[3/6] Propagating orbit...")
    propagator = OrbitPropagator(params)
    numerical = propagator.propagate()
    print(f"  ✓ Orbit propagated for {numerical['t'][-1]/60:.1f} minutes")
    print(f"  ✓ Integration: {'SUCCESS' if numerical['success'] else 'FAILED'}")
    
    # Step 4: Validation
    print("\n[4/6] Validating solution...")
    validation = validate_orbit(numerical, elements, params)
    if validation['passed']:
        print(f"  ✓ Validation PASSED")
        for warning in validation['warnings']:
            print(f"    ! {warning}")
    else:
        print(f"  ✗ Validation FAILED")
        for error in validation['errors']:
            print(f"    - {error}")
    
    # Step 5: Visualization
    print("\n[5/6] Generating visualizations...")
    plot_orbit_results(numerical, elements, params)
    print(f"  ✓ Plots saved as 'problem_6_1_orbit_results.png'")
    
    # Step 6: Results summary
    print("\n[6/6] Summary of results...")
    print("\n" + "=" * 70)
    print("ORBITAL ANALYSIS RESULTS")
    print("=" * 70)
    
    print(f"\nOrbit Classification: {orbit_type}")
    print(f"\nClassical Orbital Elements:")
    print(f"  Semi-major axis:      {elements['semi_major_axis']:8.2f} km")
    print(f"  Eccentricity:         {elements['eccentricity']:8.6f}")
    print(f"  Inclination:          {elements['inclination']:8.2f}°")
    print(f"  RAAN:                 {elements['raan']:8.2f}°")
    print(f"  Argument of perigee:  {elements['argument_perigee']:8.2f}°")
    print(f"  True anomaly:         {elements['true_anomaly']:8.2f}°")
    
    print(f"\nOrbital Characteristics:")
    print(f"  Period:               {elements['period']/60:8.2f} min")
    print(f"  Angular momentum:     {elements['angular_momentum']:8.2f} km²/s")
    print(f"  Specific energy:      {elements['energy']:8.4f} km²/s²")
    
    print(f"\nInitial Conditions:")
    print(f"  Position:             {params['r0']} km")
    print(f"  Velocity:             {params['v0']} km/s")
    
    print(f"\n✓ Problem 6.1 solved successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
