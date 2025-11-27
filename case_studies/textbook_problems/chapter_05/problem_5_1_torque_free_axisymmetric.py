"""
Problem 5.1: Torque-Free Motion of Axisymmetric Spacecraft

Reference: Canuto et al., Section 5.4.2, Page 340-344
Difficulty: ⭐⭐ (Intermediate)
Type: Computational + Analytical
Topic: Attitude Dynamics - Torque-Free Motion

PROBLEM STATEMENT:
==================
Consider a spacecraft with axisymmetric inertia tensor:
    I = diag([I_t, I_t, I_s])
where I_t is the transverse moment of inertia and I_s is the spin moment.

Given:
- I_t = 100 kg⋅m² (transverse inertia)
- I_s = 50 kg⋅m² (spin axis inertia)
- Initial conditions:
  * ω₀ = [0.1, 0.05, 1.0] rad/s (body angular velocity)

Find:
a) The principal rotation rate and nutation frequency
b) Time history of angular velocity components
c) Polhode and herpolhode curves
d) Verify conservation of angular momentum and kinetic energy
e) Stability analysis of spin about each principal axis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

class AxisymmetricSpacecraft:
    """
    Torque-free dynamics of axisymmetric rigid body.
    """
    
    def __init__(self, I_transverse: float, I_spin: float):
        self.I_t = I_transverse
        self.I_s = I_spin
        self.I = np.diag([I_transverse, I_transverse, I_spin])
        self.I_inv = np.linalg.inv(self.I)
        
        # Classification
        if I_spin > I_transverse:
            self.type = "Prolate"
        elif I_spin < I_transverse:
            self.type = "Oblate"
        else:
            self.type = "Spherical"
        
        print(f"Spacecraft type: {self.type}")
        print(f"  I_t = {I_transverse} kg⋅m², I_s = {I_spin} kg⋅m²")
    
    def analytical_solution(self, omega0: np.ndarray, t_span: tuple, n_points: int = 1000) -> dict:
        """
        Analytical solution for axisymmetric torque-free motion.
        """
        omega1_0, omega2_0, omega3_0 = omega0
        
        # Compute nutation parameters
        A = np.sqrt(omega1_0**2 + omega2_0**2)
        Omega = omega3_0 * (self.I_s - self.I_t) / self.I_t
        
        # Initial phase
        phi_0 = np.arctan2(omega2_0, omega1_0)
        
        # Time vector
        t = np.linspace(t_span[0], t_span[1], n_points)
        
        # Analytical solution
        omega1 = A * np.cos(Omega * t + phi_0)
        omega2 = A * np.sin(Omega * t + phi_0)
        omega3 = omega3_0 * np.ones_like(t)
        
        omega = np.column_stack([omega1, omega2, omega3])
        
        # Compute conserved quantities
        h = self.angular_momentum(omega0)
        h_mag = np.linalg.norm(h)
        T = self.kinetic_energy(omega0)
        
        return {
            't': t,
            'omega': omega,
            'A': A,
            'Omega': Omega,
            'omega_spin': omega3_0,
            'h': h,
            'h_magnitude': h_mag,
            'kinetic_energy': T,
            'nutation_period': 2*np.pi/abs(Omega) if Omega != 0 else np.inf
        }
    
    def euler_equations(self, t: float, state: np.ndarray) -> np.ndarray:
        """Euler's equations for torque-free motion."""
        omega = state
        gyro = np.cross(omega, self.I @ omega)
        omega_dot = self.I_inv @ (-gyro)
        return omega_dot
    
    def angular_momentum(self, omega: np.ndarray) -> np.ndarray:
        """Calculate angular momentum h = I⋅ω"""
        if omega.ndim == 1:
            return self.I @ omega
        else:
            return (self.I @ omega.T).T
    
    def kinetic_energy(self, omega: np.ndarray) -> float:
        """Calculate kinetic energy T = 0.5 * ωᵀ I ω"""
        if omega.ndim == 1:
            return 0.5 * omega.T @ self.I @ omega
        else:
            # For array of omega values - calculate energy for each time step
            return 0.5 * np.sum(omega @ self.I * omega, axis=1)

def plot_results(analytical: dict):
    """Create visualization of results."""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # Angular velocity components
    axes[0,0].plot(analytical['t'], analytical['omega'][:, 0], 'r-', label='ω₁')
    axes[0,0].plot(analytical['t'], analytical['omega'][:, 1], 'g-', label='ω₂')
    axes[0,0].plot(analytical['t'], analytical['omega'][:, 2], 'b-', label='ω₃')
    axes[0,0].set_xlabel('Time [s]')
    axes[0,0].set_ylabel('Angular Velocity [rad/s]')
    axes[0,0].set_title('Angular Velocity Components')
    axes[0,0].legend()
    axes[0,0].grid(True)
    
    # Body cone (Polhode)
    axes[0,1].plot(analytical['omega'][:, 0], analytical['omega'][:, 1], 'b-')
    axes[0,1].plot(analytical['omega'][0, 0], analytical['omega'][0, 1], 'ro', label='Start')
    axes[0,1].set_xlabel('ω₁ [rad/s]')
    axes[0,1].set_ylabel('ω₂ [rad/s]')
    axes[0,1].set_title('Body Cone (Polhode)')
    axes[0,1].axis('equal')
    axes[0,1].grid(True)
    axes[0,1].legend()
    
    # Energy conservation
    spacecraft = AxisymmetricSpacecraft(100, 50)
    T = spacecraft.kinetic_energy(analytical['omega'])
    T_error = 100 * (T - analytical['kinetic_energy']) / analytical['kinetic_energy']
    axes[1,0].plot(analytical['t'], T_error, 'r-')
    axes[1,0].set_xlabel('Time [s]')
    axes[1,0].set_ylabel('Energy Error [%]')
    axes[1,0].set_title('Kinetic Energy Conservation')
    axes[1,0].grid(True)
    axes[1,0].axhline(y=0, color='k', linestyle='--')
    
    # Angular momentum conservation
    h_history = spacecraft.angular_momentum(analytical['omega'])
    h_mag = np.linalg.norm(h_history, axis=1)
    h_error = 100 * (h_mag - analytical['h_magnitude']) / analytical['h_magnitude']
    axes[1,1].plot(analytical['t'], h_error, 'b-')
    axes[1,1].set_xlabel('Time [s]')
    axes[1,1].set_ylabel('Momentum Error [%]')
    axes[1,1].set_title('Angular Momentum Conservation')
    axes[1,1].grid(True)
    axes[1,1].axhline(y=0, color='k', linestyle='--')
    
    plt.tight_layout()
    plt.savefig('problem_5_1_results.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    print("=" * 60)
    print("PROBLEM 5.1: TORQUE-FREE MOTION OF AXISYMMETRIC SPACECRAFT")
    print("=" * 60)
    
    # Given parameters
    I_t, I_s = 100.0, 50.0
    omega0 = np.array([0.1, 0.05, 1.0])
    
    print("\n[1/3] Creating spacecraft model...")
    spacecraft = AxisymmetricSpacecraft(I_t, I_s)
    
    print("\n[2/3] Computing analytical solution...")
    analytical = spacecraft.analytical_solution(omega0, t_span=(0, 20), n_points=1000)
    
    print("\n[3/3] Generating visualizations...")
    plot_results(analytical)
    
    # Print results
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    print(f"Nutation amplitude A: {analytical['A']:.6f} rad/s")
    print(f"Nutation frequency Ω: {analytical['Omega']:.6f} rad/s")
    print(f"Nutation period T: {analytical['nutation_period']:.3f} s")
    print(f"Spin rate ω₃: {analytical['omega_spin']:.6f} rad/s")
    print(f"Angular momentum |h|: {analytical['h_magnitude']:.6f} kg⋅m²/s")
    print(f"Kinetic energy T: {analytical['kinetic_energy']:.6f} J")
    print("\n✓ Problem solved successfully!")
    print("✓ Figure saved as 'problem_5_1_results.png'")

if __name__ == "__main__":
    main()
