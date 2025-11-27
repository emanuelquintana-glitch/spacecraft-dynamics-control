"""
Coordinate Systems Module

This module provides coordinate system transformations and rotation operations
for spacecraft dynamics and control applications.

Includes:
- Rotation matrices for 3D coordinate transformations
- Reference frame definitions and conversions
- Quaternion operations for attitude representation
- Coordinate transformation utilities
"""

from .rotation_matrices import RotationMatrix, RotationMatrix3D, create_rotation_matrix
from .reference_frames import ReferenceFrame, ECI, ECEF, BodyFrame, ECI_FRAME, ECEF_FRAME
from .coordinate_transformations import transform_vector, transform_matrix, eci_to_ecef, ecef_to_eci
from .quaternion_operations import Quaternion, quaternion_from_euler, euler_from_quaternion

__all__ = [
    'RotationMatrix',
    'RotationMatrix3D', 
    'create_rotation_matrix',
    'ReferenceFrame',
    'ECI',
    'ECEF', 
    'BodyFrame',
    'ECI_FRAME',
    'ECEF_FRAME',
    'transform_vector',
    'transform_matrix',
    'eci_to_ecef',
    'ecef_to_eci',
    'Quaternion',
    'quaternion_from_euler',
    'euler_from_quaternion'
]
