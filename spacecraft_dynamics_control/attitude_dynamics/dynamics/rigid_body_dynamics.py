"""
Dinámica de cuerpo rígido para naves espaciales
"""

import numpy as np
from typing import Tuple, Dict, Optional
import numpy.typing as npt

class RigidBodyDynamics:
    """
    Dinámica de cuerpo rígido para naves espaciales
    """
    
    @staticmethod
    def euler_equations(omega: npt.NDArray, I: npt.NDArray, torque: npt.NDArray = None) -> npt.NDArray:
        """
        Ecuaciones de Euler para dinámica rotacional
        
        Args:
            omega: Velocidad angular [rad/s]
            I: Tensor de inercia [kg⋅m²]
            torque: Torque externo [N⋅m] (opcional)
            
        Returns:
            Aceleración angular [rad/s²]
        """
        if torque is None:
            torque = np.zeros(3)
        
        I_inv = np.linalg.inv(I)
        gyro_term = np.cross(omega, I @ omega)
        
        omega_dot = I_inv @ (torque - gyro_term)
        
        return omega_dot
    
    @staticmethod
    def angular_momentum(omega: npt.NDArray, I: npt.NDArray) -> npt.NDArray:
        """Momento angular h = I⋅ω"""
        return I @ omega
    
    @staticmethod
    def kinetic_energy(omega: npt.NDArray, I: npt.NDArray) -> float:
        """Energía cinética T = 0.5 * ωᵀ I ω"""
        return 0.5 * omega.T @ I @ omega
    
    @staticmethod
    def inertia_tensor(mass: float, dimensions: npt.NDArray) -> npt.NDArray:
        """
        Calcula tensor de inercia para cuerpo rígido rectangular
        
        Args:
            mass: Masa total [kg]
            dimensions: Dimensiones [largo, ancho, alto] [m]
            
        Returns:
            Tensor de inercia [kg⋅m²]
        """
        a, b, c = dimensions / 2  # Semiejes
        
        I_xx = (mass / 3) * (b**2 + c**2)
        I_yy = (mass / 3) * (a**2 + c**2)
        I_zz = (mass / 3) * (a**2 + b**2)
        
        return np.diag([I_xx, I_yy, I_zz])
