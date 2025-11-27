"""
Quaternion Operations for Spacecraft Attitude

This module provides quaternion operations for spacecraft attitude representation
and transformations between different attitude parameterizations.
"""

import numpy as np
from typing import Union, Tuple

class Quaternion:
    """
    Quaternion class for attitude representation
    
    Quaternion format: [q0, q1, q2, q3] where q0 is scalar part
    """
    
    def __init__(self, q: Union[list, tuple, np.ndarray] = None):
        """
        Initialize quaternion
        
        Parameters:
        -----------
        q : array-like, optional
            Quaternion [q0, q1, q2, q3]. If None, creates identity quaternion.
        """
        if q is None:
            self.q = np.array([1.0, 0.0, 0.0, 0.0])
        else:
            self.q = np.array(q)
            if len(self.q) != 4:
                raise ValueError("Quaternion must have 4 elements")
    
    @classmethod
    def from_euler_angles(cls, angles: Union[list, tuple, np.ndarray], 
                         sequence: str = '321') -> 'Quaternion':
        """
        Create quaternion from Euler angles
        
        Parameters:
        -----------
        angles : array-like
            Euler angles in radians [phi, theta, psi]
        sequence : str
            Rotation sequence (default '321' for yaw-pitch-roll)
            
        Returns:
        --------
        Quaternion
            Quaternion object
        """
        angles = np.array(angles)
        if len(angles) != 3:
            raise ValueError("Must provide exactly 3 Euler angles")
        
        phi, theta, psi = angles
        
        # Half angles
        half_phi = phi / 2.0
        half_theta = theta / 2.0  
        half_psi = psi / 2.0
        
        # Compute quaternion elements for 3-2-1 sequence
        if sequence == '321':
            c1, s1 = np.cos(half_psi), np.sin(half_psi)  # yaw
            c2, s2 = np.cos(half_theta), np.sin(half_theta)  # pitch
            c3, s3 = np.cos(half_phi), np.sin(half_phi)  # roll
            
            q0 = c1 * c2 * c3 + s1 * s2 * s3
            q1 = c1 * c2 * s3 - s1 * s2 * c3
            q2 = c1 * s2 * c3 + s1 * c2 * s3
            q3 = s1 * c2 * c3 - c1 * s2 * s3
            
        else:
            raise NotImplementedError(f"Rotation sequence {sequence} not implemented")
        
        return cls([q0, q1, q2, q3])
    
    def to_euler_angles(self, sequence: str = '321') -> np.ndarray:
        """
        Convert quaternion to Euler angles
        
        Parameters:
        -----------
        sequence : str
            Rotation sequence (default '321')
            
        Returns:
        --------
        np.ndarray
            Euler angles in radians [phi, theta, psi]
        """
        q0, q1, q2, q3 = self.q
        
        if sequence == '321':
            # 3-2-1 sequence (yaw-pitch-roll)
            phi = np.arctan2(2*(q0*q1 + q2*q3), 1 - 2*(q1**2 + q2**2))
            theta = np.arcsin(2*(q0*q2 - q3*q1))
            psi = np.arctan2(2*(q0*q3 + q1*q2), 1 - 2*(q2**2 + q3**2))
        else:
            raise NotImplementedError(f"Rotation sequence {sequence} not implemented")
        
        return np.array([phi, theta, psi])
    
    def conjugate(self) -> 'Quaternion':
        """
        Get quaternion conjugate
        
        Returns:
        --------
        Quaternion
            Conjugate quaternion
        """
        return Quaternion([self.q[0], -self.q[1], -self.q[2], -self.q[3]])
    
    def inverse(self) -> 'Quaternion':
        """
        Get quaternion inverse (conjugate for unit quaternion)
        
        Returns:
        --------
        Quaternion
            Inverse quaternion
        """
        return self.conjugate()
    
    def norm(self) -> float:
        """
        Get quaternion norm
        
        Returns:
        --------
        float
            Quaternion norm
        """
        return np.linalg.norm(self.q)
    
    def normalize(self) -> 'Quaternion':
        """
        Normalize quaternion to unit quaternion
        
        Returns:
        --------
        Quaternion
            Normalized quaternion
        """
        norm = self.norm()
        if norm > 0:
            return Quaternion(self.q / norm)
        return self
    
    def __mul__(self, other: 'Quaternion') -> 'Quaternion':
        """
        Quaternion multiplication
        
        Parameters:
        -----------
        other : Quaternion
            Other quaternion
            
        Returns:
        --------
        Quaternion
            Product quaternion
        """
        q0, q1, q2, q3 = self.q
        p0, p1, p2, p3 = other.q
        
        r0 = q0*p0 - q1*p1 - q2*p2 - q3*p3
        r1 = q0*p1 + q1*p0 + q2*p3 - q3*p2
        r2 = q0*p2 - q1*p3 + q2*p0 + q3*p1
        r3 = q0*p3 + q1*p2 - q2*p1 + q3*p0
        
        return Quaternion([r0, r1, r2, r3])
    
    def __str__(self) -> str:
        return f"Quaternion({self.q})"

def quaternion_from_euler(angles: Union[list, tuple, np.ndarray], 
                         sequence: str = '321') -> Quaternion:
    """
    Create quaternion from Euler angles (convenience function)
    
    Parameters:
    -----------
    angles : array-like
        Euler angles in radians [phi, theta, psi]
    sequence : str
        Rotation sequence
        
    Returns:
    --------
    Quaternion
        Quaternion representing the rotation
    """
    return Quaternion.from_euler_angles(angles, sequence)

def euler_from_quaternion(q: Union[Quaternion, list, tuple, np.ndarray], 
                         sequence: str = '321') -> np.ndarray:
    """
    Convert quaternion to Euler angles (convenience function)
    
    Parameters:
    -----------
    q : Quaternion or array-like
        Quaternion or quaternion components
    sequence : str
        Rotation sequence
        
    Returns:
    --------
    np.ndarray
        Euler angles in radians [phi, theta, psi]
    """
    if not isinstance(q, Quaternion):
        q = Quaternion(q)
    return q.to_euler_angles(sequence)

__all__ = ['Quaternion', 'quaternion_from_euler', 'euler_from_quaternion']
