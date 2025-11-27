"""
Precise pointing simulation for Earth observation missions
"""

import numpy as np
from scipy.integrate import solve_ivp

class PrecisePointingSimulator:
    """Simulator for precise pointing control of Earth observation satellites"""
    
    def __init__(self, spacecraft_params):
        self.spacecraft_params = spacecraft_params
        self.inertia = np.array(spacecraft_params['inertia'])
        self.mass = spacecraft_params['mass']
        
    def attitude_dynamics(self, t, state):
        """Attitude dynamics with disturbance torques"""
        # state: [q0, q1, q2, q3, wx, wy, wz]
        q = state[0:4]
        w = state[4:7]
        
        # Quaternion kinematics
        q_dot = 0.5 * self.quaternion_kinematics(q, w)
        
        # Euler's equations for rigid body rotation
        w_dot = np.linalg.inv(self.inertia) @ (
            -np.cross(w, self.inertia @ w) + self.disturbance_torque(t)
        )
        
        return np.concatenate([q_dot, w_dot])
    
    def quaternion_kinematics(self, q, w):
        """Quaternion kinematic equations"""
        q0, q1, q2, q3 = q
        wx, wy, wz = w
        
        Omega = np.array([
            [0, -wx, -wy, -wz],
            [wx, 0, wz, -wy],
            [wy, -wz, 0, wx],
            [wz, wy, -wx, 0]
        ])
        
        return 0.5 * Omega @ q
    
    def disturbance_torque(self, t):
        """Simplified disturbance torque model"""
        # Gravity gradient torque (simplified)
        gravity_gradient = np.array([0.1 * np.sin(0.1*t), 
                                   0.05 * np.cos(0.1*t), 
                                   0.02 * np.sin(0.05*t)]) * 1e-5
        
        # Other disturbances
        other_disturbances = np.random.normal(0, 1e-6, 3)
        
        return gravity_gradient + other_disturbances
    
    def simulate(self, duration, initial_state):
        """Run the simulation"""
        sol = solve_ivp(
            self.attitude_dynamics,
            [0, duration],
            initial_state,
            method='RK45',
            t_eval=np.linspace(0, duration, 1000)
        )
        
        return sol

if __name__ == "__main__":
    # Example usage
    spacecraft_params = {
        'mass': 1000,  # kg
        'inertia': [[1000, 0, 0],
                   [0, 800, 0],
                   [0, 0, 1200]]  # kg*m^2
    }
    
    simulator = PrecisePointingSimulator(spacecraft_params)
    
    # Initial state: pointing at target with small angular velocity
    initial_state = np.array([1, 0, 0, 0,  # quaternion (no rotation)
                             0.001, -0.0005, 0.0002])  # angular velocity (rad/s)
    
    # Simulate for 100 seconds
    result = simulator.simulate(100, initial_state)
    print(f"Simulation completed with {len(result.t)} time points")
