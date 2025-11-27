"""
Rotation Matrix Operations for Spacecraft Dynamics

This module provides comprehensive rotation matrix operations for 3D coordinate transformations
in spacecraft attitude dynamics and control.
"""

import numpy as np
from typing import Union, Tuple

class RotationMatrix:
    """
    Rotation Matrix class for 3D coordinate transformations
    
    Provides methods for creating rotation matrices and performing
    coordinate transformations between different reference frames.
    """
    
    def __init__(self, matrix: np.ndarray = None):
        """
        Initialize rotation matrix
        
        Parameters:
        -----------
        matrix : np.ndarray, optional
            3x3 rotation matrix. If None, creates identity matrix.
        """
        if matrix is None:
            self.matrix = np.eye(3)
        else:
            if matrix.shape != (3, 3):
                raise ValueError("Rotation matrix must be 3x3")
            self.matrix = matrix
    
    @classmethod
    def from_euler_angles(cls, angles: Union[list, tuple, np.ndarray], 
                         sequence: str = '321') -> 'RotationMatrix':
        """
        Create rotation matrix from Euler angles
        
        Parameters:
        -----------
        angles : array-like
            Euler angles in radians [phi, theta, psi]
        sequence : str
            Rotation sequence (default '321' for yaw-pitch-roll)
            
        Returns:
        --------
        RotationMatrix
            Rotation matrix object
        """
        angles = np.array(angles)
        if len(angles) != 3:
            raise ValueError("Must provide exactly 3 Euler angles")
        
        phi, theta, psi = angles
        
        # Default sequence: 3-2-1 (yaw-pitch-roll)
        if sequence == '321':
            R1 = np.array([[1, 0, 0],
                          [0, np.cos(phi), np.sin(phi)],
                          [0, -np.sin(phi), np.cos(phi)]])
            
            R2 = np.array([[np.cos(theta), 0, -np.sin(theta)],
                          [0, 1, 0],
                          [np.sin(theta), 0, np.cos(theta)]])
            
            R3 = np.array([[np.cos(psi), np.sin(psi), 0],
                          [-np.sin(psi), np.cos(psi), 0],
                          [0, 0, 1]])
            
            matrix = R1 @ R2 @ R3
            
        else:
            raise NotImplementedError(f"Rotation sequence {sequence} not implemented")
        
        return cls(matrix)
    
    @classmethod
    def from_quaternion(cls, q: Union[list, tuple, np.ndarray]) -> 'RotationMatrix':
        """
        Create rotation matrix from quaternion
        
        Parameters:
        -----------
        q : array-like
            Quaternion [q0, q1, q2, q3] where q0 is scalar part
            
        Returns:
        --------
        RotationMatrix
            Rotation matrix object
        """
        q = np.array(q)
        if len(q) != 4:
            raise ValueError("Quaternion must have 4 elements")
        
        q0, q1, q2, q3 = q
        
        # Normalize quaternion
        q_norm = np.linalg.norm(q)
        q0, q1, q2, q3 = q / q_norm
        
        # Compute rotation matrix elements
        R11 = 1 - 2*(q2**2 + q3**2)
        R12 = 2*(q1*q2 - q0*q3)
        R13 = 2*(q1*q3 + q0*q2)
        
        R21 = 2*(q1*q2 + q0*q3)
        R22 = 1 - 2*(q1**2 + q3**2)
        R23 = 2*(q2*q3 - q0*q1)
        
        R31 = 2*(q1*q3 - q0*q2)
        R32 = 2*(q2*q3 + q0*q1)
        R33 = 1 - 2*(q1**2 + q2**2)
        
        matrix = np.array([[R11, R12, R13],
                          [R21, R22, R23],
                          [R31, R32, R33]])
        
        return cls(matrix)
    
    def transform_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Transform vector using rotation matrix
        
        Parameters:
        -----------
        vector : np.ndarray
            3D vector to transform
            
        Returns:
        --------
        np.ndarray
            Transformed vector
        """
        return self.matrix @ vector
    
    def inverse(self) -> 'RotationMatrix':
        """
        Get inverse rotation matrix (transpose)
        
        Returns:
        --------
        RotationMatrix
            Inverse rotation matrix
        """
        return RotationMatrix(self.matrix.T)
    
    def __matmul__(self, other: Union['RotationMatrix', np.ndarray]) -> Union['RotationMatrix', np.ndarray]:
        """
        Matrix multiplication operator
        
        Parameters:
        -----------
        other : RotationMatrix or np.ndarray
            Other rotation matrix or vector
            
        Returns:
        --------
        RotationMatrix or np.ndarray
            Result of multiplication
        """
        if isinstance(other, RotationMatrix):
            return RotationMatrix(self.matrix @ other.matrix)
        elif isinstance(other, np.ndarray):
            return self.matrix @ other
        else:
            raise TypeError("Unsupported type for multiplication")
    
    def __str__(self) -> str:
        """String representation"""
        return f"RotationMatrix:\n{self.matrix}"

def create_rotation_matrix(axis: str, angle: float) -> np.ndarray:
    """
    Create basic rotation matrix for rotation about a principal axis
    
    Parameters:
    -----------
    axis : str
        Rotation axis ('x', 'y', or 'z')
    angle : float
        Rotation angle in radians
        
    Returns:
    --------
    np.ndarray
        3x3 rotation matrix
    """
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    
    if axis == 'x':
        return np.array([[1, 0, 0],
                        [0, cos_a, sin_a],
                        [0, -sin_a, cos_a]])
    elif axis == 'y':
        return np.array([[cos_a, 0, -sin_a],
                        [0, 1, 0],
                        [sin_a, 0, cos_a]])
    elif axis == 'z':
        return np.array([[cos_a, sin_a, 0],
                        [-sin_a, cos_a, 0],
                        [0, 0, 1]])
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")

# For backward compatibility
RotationMatrix3D = RotationMatrix

__all__ = ['RotationMatrix', 'RotationMatrix3D', 'create_rotation_matrix']
