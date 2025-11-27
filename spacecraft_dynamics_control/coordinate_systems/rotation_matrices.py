# Crear: spacecraft_dynamics_control/coordinate_systems/rotation_matrices.py

import numpy as np
from typing import Tuple, List
import numpy.typing as npt

class RotationMatrices:
    """
    Operaciones con matrices de rotación 3D
    Implementa rotaciones elementales, composición y propiedades
    
    Referencias del índice:
    - Matrices ortogonales propias (página 28)
    - Rotaciones elementales de Euler (página 30-31)
    - Interpretaciones alibi y alias (página 44)
    """
    
    @staticmethod
    def rx(theta: float) -> npt.NDArray:
        """
        Matriz de rotación alrededor del eje X (roll)
        
        Args:
            theta: Ángulo de rotación en radianes
            
        Returns:
            Matriz de rotación 3x3 alrededor del eje X
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        R_x = np.array([
            [1, 0, 0],
            [0, cos_theta, -sin_theta],
            [0, sin_theta, cos_theta]
        ])
        
        return R_x
    
    @staticmethod
    def ry(theta: float) -> npt.NDArray:
        """
        Matriz de rotación alrededor del eje Y (pitch)
        
        Args:
            theta: Ángulo de rotación en radianes
            
        Returns:
            Matriz de rotación 3x3 alrededor del eje Y
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        R_y = np.array([
            [cos_theta, 0, sin_theta],
            [0, 1, 0],
            [-sin_theta, 0, cos_theta]
        ])
        
        return R_y
    
    @staticmethod
    def rz(theta: float) -> npt.NDArray:
        """
        Matriz de rotación alrededor del eje Z (yaw)
        
        Args:
            theta: Ángulo de rotación en radianes
            
        Returns:
            Matriz de rotación 3x3 alrededor del eje Z
        """
        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)
        
        R_z = np.array([
            [cos_theta, -sin_theta, 0],
            [sin_theta, cos_theta, 0],
            [0, 0, 1]
        ])
        
        return R_z
    
    @staticmethod
    def euler_sequence(angles: Tuple[float, float, float], 
                      sequence: str = '321') -> npt.NDArray:
        """
        Matriz de rotación para secuencia de Euler (Tait-Bryan)
        
        Args:
            angles: Tupla de 3 ángulos en radianes (phi, theta, psi)
            sequence: Secuencia de ejes (ej: '321' para Z-Y-X)
            
        Returns:
            Matriz de rotación compuesta 3x3
            
        Raises:
            ValueError: Si la secuencia no es válida
        """
        if len(sequence) != 3:
            raise ValueError("La secuencia debe tener exactamente 3 caracteres")
        
        phi, theta, psi = angles
        
        # Mapeo de ejes a funciones de rotación
        axis_map = {
            '1': (RotationMatrices.rx, phi),
            '2': (RotationMatrices.ry, theta), 
            '3': (RotationMatrices.rz, psi)
        }
        
        # Verificar que la secuencia sea válida
        for char in sequence:
            if char not in axis_map:
                raise ValueError(f"Eje '{char}' no válido. Use '1', '2', o '3'")
        
        # Construir la rotación compuesta (multiplicación en orden inverso)
        rotation = np.eye(3)
        for char in reversed(sequence):
            rot_func, angle = axis_map[char]
            rotation = rot_func(angle) @ rotation
        
        return rotation
    
    @staticmethod
    def is_rotation_matrix(R: npt.NDArray, tolerance: float = 1e-6) -> bool:
        """
        Verifica si una matriz es una matriz de rotación válida
        
        Criterios:
        1. Determinante ≈ 1 (para rotaciones propias)
        2. R.T @ R ≈ I (ortogonalidad)
        
        Args:
            R: Matriz a verificar
            tolerance: Tolerancia para comparaciones
            
        Returns:
            True si es una matriz de rotación válida
        """
        if R.shape != (3, 3):
            return False
        
        # Verificar ortogonalidad: R^T R = I
        identity_check = R.T @ R
        is_orthogonal = np.allclose(identity_check, np.eye(3), atol=tolerance)
        
        # Verificar determinante ≈ 1 (rotación propia)
        det = np.linalg.det(R)
        is_proper = abs(det - 1.0) < tolerance
        
        return is_orthogonal and is_proper
    
    @staticmethod
    def rotation_angle_axis(R: npt.NDArray) -> Tuple[float, npt.NDArray]:
        """
        Extrae ángulo y eje de rotación de una matriz de rotación
        basado en el Teorema de Rotación de Euler
        
        Args:
            R: Matriz de rotación 3x3
            
        Returns:
            Tuple (ángulo, eje_unitario)
        """
        if not RotationMatrices.is_rotation_matrix(R):
            raise ValueError("La matriz de entrada no es una matriz de rotación válida")
        
        # Calcular el ángulo de rotación
        trace = np.trace(R)
        angle = np.arccos(np.clip((trace - 1) / 2, -1.0, 1.0))
        
        # Calcular el eje de rotación
        # Para ángulos no nulos
        if not np.isclose(angle, 0):
            skew_symmetric = (R - R.T) / (2 * np.sin(angle))
            axis = np.array([skew_symmetric[2, 1], 
                           skew_symmetric[0, 2], 
                           skew_symmetric[1, 0]])
            axis = axis / np.linalg.norm(axis)
        else:
            # Para rotación nula, el eje es arbitrario
            axis = np.array([1.0, 0.0, 0.0])
        
        return angle, axis
    
    @staticmethod
    def rodrigues_formula(axis: npt.NDArray, angle: float) -> npt.NDArray:
        """
        Fórmula de Rodrigues para construir matriz de rotación
        a partir de eje-ángulo
        
        Args:
            axis: Eje de rotación (no necesariamente unitario)
            angle: Ángulo de rotación en radianes
            
        Returns:
            Matriz de rotación 3x3
        """
        axis = axis / np.linalg.norm(axis)  # Normalizar
        kx, ky, kz = axis
        
        # Matriz antisimétrica del eje K
        K = np.array([
            [0, -kz, ky],
            [kz, 0, -kx],
            [-ky, kx, 0]
        ])
        
        # Fórmula de Rodrigues: R = I + sin(θ)K + (1-cos(θ))K²
        I = np.eye(3)
        sin_theta = np.sin(angle)
        cos_theta = np.cos(angle)
        
        R = I + sin_theta * K + (1 - cos_theta) * (K @ K)
        
        return R

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    print("🧪 Probando matrices de rotación...")
    
    # Prueba de rotaciones elementales
    theta = np.pi / 4  # 45 grados
    
    R_x = RotationMatrices.rx(theta)
    R_y = RotationMatrices.ry(theta) 
    R_z = RotationMatrices.rz(theta)
    
    print("✅ Rotaciones elementales creadas")
    print(f"R_x(π/4):\n{R_x}")
    
    # Prueba de secuencia de Euler
    angles = (np.pi/6, np.pi/4, np.pi/3)  # 30, 45, 60 grados
    R_321 = RotationMatrices.euler_sequence(angles, '321')
    print(f"✅ Secuencia 321: {angles}")
    print(f"R_321:\n{R_321}")
    
    # Verificación de matriz de rotación
    is_rot = RotationMatrices.is_rotation_matrix(R_321)
    print(f"✅ Es matriz de rotación válida: {is_rot}")
    
    # Extracción de ángulo y eje
    angle, axis = RotationMatrices.rotation_angle_axis(R_321)
    print(f"✅ Ángulo de rotación: {angle:.4f} rad")
    print(f"✅ Eje de rotación: {axis}")
    
    # Reconstrucción con fórmula de Rodrigues
    R_reconstructed = RotationMatrices.rodrigues_formula(axis, angle)
    print(f"✅ Reconstrucción exitosa: {np.allclose(R_321, R_reconstructed)}")