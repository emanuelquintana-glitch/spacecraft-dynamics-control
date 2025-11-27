# Crear: spacecraft_dynamics_control/coordinate_systems/coordinate_transformations.py

import numpy as np
from typing import Tuple, Dict
import numpy.typing as npt

class CoordinateTransformations:
    """
    Transformaciones entre sistemas de coordenadas para dinámica espacial
    
    Sistemas implementados:
    - ECI (Earth-Centered Inertial)
    - ECEF (Earth-Centered Earth-Fixed)
    - LVLH (Local Vertical Local Horizontal) 
    - Body (Sistema cuerpo de la nave)
    - Orbital (Elementos orbitales)
    """
    
    @staticmethod
    def eci_to_ecef_position(r_eci: npt.NDArray, gmst: float) -> npt.NDArray:
        """
        Transforma posición de ECI a ECEF considerando rotación terrestre
        
        Args:
            r_eci: Vector posición en ECI [km]
            gmst: Greenwich Mean Sidereal Time en radianes
            
        Returns:
            Vector posición en ECEF [km]
        """
        # Matriz de rotación ECI->ECEF (rotación alrededor del eje Z)
        cos_gmst = np.cos(gmst)
        sin_gmst = np.sin(gmst)
        
        R_eci_ecef = np.array([
            [cos_gmst, sin_gmst, 0],
            [-sin_gmst, cos_gmst, 0],
            [0, 0, 1]
        ])
        
        return R_eci_ecef @ r_eci
    
    @staticmethod
    def ecef_to_eci_position(r_ecef: npt.NDArray, gmst: float) -> npt.NDArray:
        """
        Transforma posición de ECEF a ECI
        
        Args:
            r_ecef: Vector posición en ECEF [km]
            gmst: Greenwich Mean Sidereal Time en radianes
            
        Returns:
            Vector posición en ECI [km]
        """
        # Matriz de rotación ECEF->ECI (transpuesta de ECI->ECEF)
        cos_gmst = np.cos(gmst)
        sin_gmst = np.sin(gmst)
        
        R_ecef_eci = np.array([
            [cos_gmst, -sin_gmst, 0],
            [sin_gmst, cos_gmst, 0],
            [0, 0, 1]
        ])
        
        return R_ecef_eci @ r_ecef
    
    @staticmethod
    def eci_to_lvlh_velocity(r_eci: npt.NDArray, v_eci: npt.NDArray, 
                           omega_earth: float = 7.292115e-5) -> npt.NDArray:
        """
        Transforma velocidad de ECI a LVLH considerando rotación orbital
        
        Args:
            r_eci: Vector posición en ECI [km]
            v_eci: Vector velocidad en ECI [km/s]
            omega_earth: Tasa de rotación terrestre [rad/s]
            
        Returns:
            Vector velocidad en LVLH [km/s]
        """
        from .reference_frames import ReferenceFrames
        
        # Obtener matriz de transformación
        T_eci_lvlh = ReferenceFrames.eci_to_lvlh(r_eci, v_eci)
        
        # Velocidad angular orbital
        h = np.cross(r_eci, v_eci)
        r_norm = np.linalg.norm(r_eci)
        omega_orbital = h / (r_norm**2)
        
        # Transformar velocidad
        v_lvlh = T_eci_lvlh @ (v_eci - np.cross(omega_orbital, r_eci))
        
        return v_lvlh
    
    @staticmethod
    def cartesian_to_orbital_elements(r_eci: npt.NDArray, v_eci: npt.NDArray, 
                                    mu: float = 398600.4418) -> Dict[str, float]:
        """
        Convierte coordenadas cartesianas (ECI) a elementos orbitales
        
        Args:
            r_eci: Vector posición en ECI [km]
            v_eci: Vector velocidad en ECI [km/s]
            mu: Parámetro gravitacional terrestre [km³/s²]
            
        Returns:
            Diccionario con elementos orbitales
        """
        # Vector momento angular
        h = np.cross(r_eci, v_eci)
        h_norm = np.linalg.norm(h)
        
        # Vector excentricidad
        r_norm = np.linalg.norm(r_eci)
        v_norm = np.linalg.norm(v_eci)
        e_vec = ((v_norm**2 - mu/r_norm) * r_eci - np.dot(r_eci, v_eci) * v_eci) / mu
        e = np.linalg.norm(e_vec)
        
        # Semieje mayor
        energy = v_norm**2 / 2 - mu / r_norm
        if abs(energy) < 1e-10:
            a = float('inf')  # Órbita parabólica
        else:
            a = -mu / (2 * energy)
        
        # Inclinación
        i = np.arccos(h[2] / h_norm)
        
        # Ascensión recta del nodo ascendente
        n = np.cross([0, 0, 1], h)
        n_norm = np.linalg.norm(n)
        if n_norm == 0:
            raan = 0  # Órbita ecuatorial
        else:
            raan = np.arccos(n[0] / n_norm)
            if n[1] < 0:
                raan = 2 * np.pi - raan
        
        # Argumento del perigeo
        if n_norm == 0:
            arg_perigee = 0
        else:
            arg_perigee = np.arccos(np.dot(n, e_vec) / (n_norm * e))
            if e_vec[2] < 0:
                arg_perigee = 2 * np.pi - arg_perigee
        
        # Anomalía verdadera
        if e == 0:
            true_anomaly = 0  # Órbita circular
        else:
            true_anomaly = np.arccos(np.dot(e_vec, r_eci) / (e * r_norm))
            if np.dot(r_eci, v_eci) < 0:
                true_anomaly = 2 * np.pi - true_anomaly
        
        return {
            'semi_major_axis': a,
            'eccentricity': e,
            'inclination': i,
            'raan': raan,
            'argument_of_perigee': arg_perigee,
            'true_anomaly': true_anomaly
        }
    
    @staticmethod
    def orbital_elements_to_cartesian(elements: Dict[str, float], 
                                    mu: float = 398600.4418) -> Tuple[npt.NDArray, npt.NDArray]:
        """
        Convierte elementos orbitales a coordenadas cartesianas (ECI)
        
        Args:
            elements: Diccionario con elementos orbitales
            mu: Parámetro gravitacional terrestre [km³/s²]
            
        Returns:
            Tupla (r_eci, v_eci)
        """
        a = elements['semi_major_axis']
        e = elements['eccentricity']
        i = elements['inclination']
        raan = elements['raan']
        arg_perigee = elements['argument_of_perigee']
        true_anomaly = elements['true_anomaly']
        
        # Parámetros orbitales
        p = a * (1 - e**2)  # Semilatus rectum
        
        # Posición en el plano orbital
        r_orbital = p / (1 + e * np.cos(true_anomaly))
        r_perifocal = np.array([
            r_orbital * np.cos(true_anomaly),
            r_orbital * np.sin(true_anomaly),
            0
        ])
        
        # Velocidad en el plano orbital
        v_perifocal = np.array([
            -np.sqrt(mu/p) * np.sin(true_anomaly),
            np.sqrt(mu/p) * (e + np.cos(true_anomaly)),
            0
        ])
        
        # Matriz de transformación perifocal->ECI
        R_perifocal_eci = CoordinateTransformations._perifocal_to_eci_matrix(i, raan, arg_perigee)
        
        # Transformar a ECI
        r_eci = R_perifocal_eci @ r_perifocal
        v_eci = R_perifocal_eci @ v_perifocal
        
        return r_eci, v_eci
    
    @staticmethod
    def _perifocal_to_eci_matrix(i: float, raan: float, arg_perigee: float) -> npt.NDArray:
        """
        Matriz de transformación del sistema perifocal a ECI
        
        Args:
            i: Inclinación [rad]
            raan: Ascensión recta del nodo ascendente [rad]
            arg_perigee: Argumento del perigeo [rad]
            
        Returns:
            Matriz de transformación 3x3
        """
        cos_raan = np.cos(raan)
        sin_raan = np.sin(raan)
        cos_i = np.cos(i)
        sin_i = np.sin(i)
        cos_w = np.cos(arg_perigee)
        sin_w = np.sin(arg_perigee)
        
        R = np.array([
            [cos_raan*cos_w - sin_raan*sin_w*cos_i, -cos_raan*sin_w - sin_raan*cos_w*cos_i, sin_raan*sin_i],
            [sin_raan*cos_w + cos_raan*sin_w*cos_i, -sin_raan*sin_w + cos_raan*cos_w*cos_i, -cos_raan*sin_i],
            [sin_w*sin_i, cos_w*sin_i, cos_i]
        ])
        
        return R

# Ejemplo de uso
if __name__ == "__main__":
    print("🧪 Probando transformaciones de coordenadas...")
    
    # Ejemplo: Órbita circular
    r_eci = np.array([7000.0, 0.0, 0.0])
    v_eci = np.array([0.0, 7.5, 0.0])
    
    # Conversión a elementos orbitales
    elements = CoordinateTransformations.cartesian_to_orbital_elements(r_eci, v_eci)
    print("✅ Elementos orbitales:")
    for key, value in elements.items():
        print(f"  {key}: {value:.4f}")
    
    # Conversión de vuelta a cartesianas
    r_eci_recon, v_eci_recon = CoordinateTransformations.orbital_elements_to_cartesian(elements)
    print(f"✅ Reconstrucción posición: {np.allclose(r_eci, r_eci_recon)}")
    print(f"✅ Reconstrucción velocidad: {np.allclose(v_eci, v_eci_recon)}")
    
    # Transformación ECI->ECEF (ejemplo con GMST = 0)
    gmst = 0.0
    r_ecef = CoordinateTransformations.eci_to_ecef_position(r_eci, gmst)
    print(f"✅ Posición ECEF: {r_ecef}")
