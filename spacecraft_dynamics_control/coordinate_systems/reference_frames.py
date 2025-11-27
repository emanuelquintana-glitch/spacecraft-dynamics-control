# Crear: spacecraft_dynamics_control/coordinate_systems/reference_frames.py

import numpy as np
from typing import Tuple, Dict, Optional
import numpy.typing as npt

class ReferenceFrames:
    """
    Sistemas de referencia para dinámica de naves espaciales
    
    Sistemas implementados:
    - ECI (Earth-Centered Inertial)
    - ECEF (Earth-Centered Earth-Fixed) 
    - LVLH (Local Vertical Local Horizontal)
    - Body (Sistema cuerpo de la nave)
    """
    
    @staticmethod
    def eci_to_lvlh(r_eci: npt.NDArray, v_eci: npt.NDArray) -> npt.NDArray:
        """
        Transforma del sistema ECI al sistema LVLH (Local Vertical Local Horizontal)
        
        Args:
            r_eci: Vector posición en ECI [km] (3 elementos)
            v_eci: Vector velocidad en ECI [km/s] (3 elementos)
            
        Returns:
            Matriz de transformación 3x3 de ECI a LVLH
            
        Raises:
            ValueError: Si los vectores no son 3D o son colineales
        """
        if r_eci.shape != (3,) or v_eci.shape != (3,):
            raise ValueError("Los vectores posición y velocidad deben ser de 3 elementos")
        
        # Vector radial unitario (eje R - Radial)
        r_norm = np.linalg.norm(r_eci)
        if r_norm == 0:
            raise ValueError("El vector posición no puede ser cero")
        r_hat = r_eci / r_norm
        
        # Vector momento angular (eje H - Orbit Normal)
        h = np.cross(r_eci, v_eci)
        h_norm = np.linalg.norm(h)
        if h_norm == 0:
            raise ValueError("Los vectores posición y velocidad son colineales")
        h_hat = h / h_norm
        
        # Vector transversal unitario (eje T - Transverse)
        t_hat = np.cross(h_hat, r_hat)
        
        # Matriz de transformación ECI -> LVLH
        # Las columnas son los vectores unitarios de LVLH expresados en ECI
        T_eci_lvlh = np.column_stack([r_hat, t_hat, h_hat])
        
        return T_eci_lvlh
    
    @staticmethod
    def lvlh_to_eci(r_eci: npt.NDArray, v_eci: npt.NDArray) -> npt.NDArray:
        """
        Transforma del sistema LVLH al sistema ECI
        
        Args:
            r_eci: Vector posición en ECI [km]
            v_eci: Vector velocidad en ECI [km/s]
            
        Returns:
            Matriz de transformación 3x3 de LVLH a ECI
        """
        # La transformación inversa es la transpuesta
        T_eci_lvlh = ReferenceFrames.eci_to_lvlh(r_eci, v_eci)
        return T_eci_lvlh.T
    
    @staticmethod
    def eci_to_ecef(epoch_time: float) -> npt.NDArray:
        """
        Transforma del sistema ECI al sistema ECEF considerando rotación terrestre
        
        Args:
            epoch_time: Tiempo desde epoch en segundos
            
        Returns:
            Matriz de transformación 3x3 de ECI a ECEF
        """
        # Tasa de rotación terrestre (rad/s)
        omega_earth = 7.292115e-5  # rad/s
        
        # Ángulo de rotación
        theta = omega_earth * epoch_time
        
        # Matriz de rotación alrededor del eje Z
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        T_eci_ecef = np.array([
            [cos_theta, sin_theta, 0],
            [-sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])
        
        return T_eci_ecef
    
    @staticmethod
    def quaternion_to_dcm(q: npt.NDArray) -> npt.NDArray:
        """
        Convierte un cuaternión a matriz de cosenos directores (DCM)
        
        Args:
            q: Cuaternión [q0, q1, q2, q3] donde q0 es la parte escalar
            
        Returns:
            Matriz de transformación 3x3
        """
        if q.shape != (4,):
            raise ValueError("El cuaternión debe tener 4 elementos")
        
        q0, q1, q2, q3 = q
        
        # Normalizar el cuaternión
        q_norm = np.linalg.norm(q)
        if q_norm == 0:
            raise ValueError("El cuaternión no puede ser cero")
        q0, q1, q2, q3 = q / q_norm
        
        # Matriz de cosenos directores
        dcm = np.array([
            [q0**2 + q1**2 - q2**2 - q3**2, 2*(q1*q2 + q0*q3), 2*(q1*q3 - q0*q2)],
            [2*(q1*q2 - q0*q3), q0**2 - q1**2 + q2**2 - q3**2, 2*(q2*q3 + q0*q1)],
            [2*(q1*q3 + q0*q2), 2*(q2*q3 - q0*q1), q0**2 - q1**2 - q2**2 + q3**2]
        ])
        
        return dcm
    
    @staticmethod
    def transform_vector(vector: npt.NDArray, transformation_matrix: npt.NDArray) -> npt.NDArray:
        """
        Transforma un vector usando una matriz de transformación
        
        Args:
            vector: Vector 3D a transformar
            transformation_matrix: Matriz de transformación 3x3
            
        Returns:
            Vector transformado
        """
        if vector.shape != (3,):
            raise ValueError("El vector debe ser de 3 elementos")
        if transformation_matrix.shape != (3, 3):
            raise ValueError("La matriz de transformación debe ser 3x3")
        
        return transformation_matrix @ vector

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    # Ejemplo de prueba
    print("🔧 Probando sistemas de referencia...")
    
    # Vector posición y velocidad de ejemplo (órbita circular)
    r_eci = np.array([7000.0, 0.0, 0.0])  # km
    v_eci = np.array([0.0, 7.5, 0.0])     # km/s
    
    try:
        # Transformación ECI to LVLH
        T_eci_lvlh = ReferenceFrames.eci_to_lvlh(r_eci, v_eci)
        print("✅ Transformación ECI->LVLH exitosa")
        print(f"Matriz de transformación:\n{T_eci_lvlh}")
        
        # Verificar que es ortogonal
        identity_check = T_eci_lvlh.T @ T_eci_lvlh
        print(f"✅ Verificación ortogonalidad:\n{identity_check}")
        
        # Transformación inversa
        T_lvlh_eci = ReferenceFrames.lvlh_to_eci(r_eci, v_eci)
        print("✅ Transformación LVLH->ECI exitosa")
        
    except Exception as e:
        print(f"❌ Error: {e}")
