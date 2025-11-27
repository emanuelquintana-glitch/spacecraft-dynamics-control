"""
Coordinate Transformation Utilities

This module provides utility functions for coordinate transformations
between different reference frames.
"""

import numpy as np
from typing import Union

def transform_vector(vector: np.ndarray, rotation_matrix: np.ndarray) -> np.ndarray:
    """
    Transform vector using rotation matrix
    
    Parameters:
    -----------
    vector : np.ndarray
        3D vector to transform
    rotation_matrix : np.ndarray
        3x3 rotation matrix
        
    Returns:
    --------
    np.ndarray
        Transformed vector
    """
    if vector.shape != (3,):
        raise ValueError("Vector must be 3D")
    if rotation_matrix.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")
    
    return rotation_matrix @ vector

def transform_matrix(matrix: np.ndarray, rotation_matrix: np.ndarray) -> np.ndarray:
    """
    Transform matrix using similarity transformation
    
    Parameters:
    -----------
    matrix : np.ndarray
        Matrix to transform (e.g., inertia tensor)
    rotation_matrix : np.ndarray
        3x3 rotation matrix
        
    Returns:
    --------
    np.ndarray
        Transformed matrix
    """
    if matrix.shape != (3, 3):
        raise ValueError("Matrix must be 3x3")
    if rotation_matrix.shape != (3, 3):
        raise ValueError("Rotation matrix must be 3x3")
    
    return rotation_matrix @ matrix @ rotation_matrix.T

def eci_to_ecef(vector_eci: np.ndarray, gmst: float) -> np.ndarray:
    """
    Transform vector from ECI to ECEF frame
    
    Parameters:
    -----------
    vector_eci : np.ndarray
        Vector in ECI frame
    gmst : float
        Greenwich Mean Sidereal Time in radians
        
    Returns:
    --------
    np.ndarray
        Vector in ECEF frame
    """
    # Rotation about Z-axis by GMST
    cos_gmst = np.cos(gmst)
    sin_gmst = np.sin(gmst)
    
    R_eci_to_ecef = np.array([
        [cos_gmst, sin_gmst, 0],
        [-sin_gmst, cos_gmst, 0],
        [0, 0, 1]
    ])
    
    return R_eci_to_ecef @ vector_eci

def ecef_to_eci(vector_ecef: np.ndarray, gmst: float) -> np.ndarray:
    """
    Transform vector from ECEF to ECI frame
    
    Parameters:
    -----------
    vector_ecef : np.ndarray
        Vector in ECEF frame
    gmst : float
        Greenwich Mean Sidereal Time in radians
        
    Returns:
    --------
    np.ndarray
        Vector in ECI frame
    """
    # Inverse rotation (transpose)
    cos_gmst = np.cos(gmst)
    sin_gmst = np.sin(gmst)
    
    R_ecef_to_eci = np.array([
        [cos_gmst, -sin_gmst, 0],
        [sin_gmst, cos_gmst, 0],
        [0, 0, 1]
    ])
    
    return R_ecef_to_eci @ vector_ecef

__all__ = [
    'transform_vector', 
    'transform_matrix',
    'eci_to_ecef', 
    'ecef_to_eci'
]
