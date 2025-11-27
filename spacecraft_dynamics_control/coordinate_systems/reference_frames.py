"""
Reference Frame Definitions for Spacecraft Dynamics

This module defines various reference frames used in spacecraft dynamics:
- ECI (Earth-Centered Inertial)
- ECEF (Earth-Centered Earth-Fixed) 
- Body Frame (Spacecraft Body Frame)
"""

import numpy as np
from typing import List, Tuple

class ReferenceFrame:
    """
    Base class for reference frames in spacecraft dynamics
    """
    
    def __init__(self, name: str, description: str = ""):
        """
        Initialize reference frame
        
        Parameters:
        -----------
        name : str
            Name of the reference frame
        description : str
            Description of the reference frame
        """
        self.name = name
        self.description = description
    
    def __str__(self) -> str:
        return f"ReferenceFrame({self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()

class ECI(ReferenceFrame):
    """
    Earth-Centered Inertial (ECI) Reference Frame
    
    An inertial frame with origin at Earth's center:
    - X-axis: Vernal equinox direction
    - Y-axis: Completes right-handed system in equatorial plane  
    - Z-axis: Earth's rotation axis
    """
    
    def __init__(self):
        super().__init__("ECI", "Earth-Centered Inertial Frame")
        
    def to_string(self) -> str:
        return "ECI Frame: Earth-Centered Inertial"

class ECEF(ReferenceFrame):
    """
    Earth-Centered Earth-Fixed (ECEF) Reference Frame
    
    A rotating frame fixed to Earth:
    - X-axis: Prime meridian in equatorial plane
    - Y-axis: 90° east in equatorial plane
    - Z-axis: Earth's rotation axis
    """
    
    def __init__(self):
        super().__init__("ECEF", "Earth-Centered Earth-Fixed Frame")
        
    def to_string(self) -> str:
        return "ECEF Frame: Earth-Centered Earth-Fixed"

class BodyFrame(ReferenceFrame):
    """
    Spacecraft Body Reference Frame
    
    Frame fixed to the spacecraft body:
    - X-axis: Typically along principal axis (roll)
    - Y-axis: Typically along principal axis (pitch) 
    - Z-axis: Typically along principal axis (yaw)
    """
    
    def __init__(self, spacecraft_name: str = "Spacecraft"):
        super().__init__("Body", f"Body Frame of {spacecraft_name}")
        self.spacecraft_name = spacecraft_name
        
    def to_string(self) -> str:
        return f"Body Frame: {self.spacecraft_name}"

# Convenience instances
ECI_FRAME = ECI()
ECEF_FRAME = ECEF()

__all__ = ['ReferenceFrame', 'ECI', 'ECEF', 'BodyFrame', 'ECI_FRAME', 'ECEF_FRAME']
