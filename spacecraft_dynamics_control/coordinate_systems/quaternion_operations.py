import numpy as np
from typing import Tuple, Optional
import numpy.typing as npt

# Usar import absoluto en lugar de relativo
try:
    from .rotation_matrices import RotationMatrices
except ImportError:
    # Para cuando se ejecuta el archivo directamente
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from coordinate_systems.rotation_matrices import RotationMatrices

class QuaternionOperations:
    """
    Operaciones con cuaterniones para representación de actitud
    
    Referencias del índice:
    - Cuaterniones unitarios (página 39-45)
    - Cuaterniones antipodales (página 259)
    - Conversión entre representaciones (página 76-80)
    """
    
    @staticmethod
    def from_axis_angle(axis: npt.NDArray, angle: float) -> npt.NDArray:
        """
        Construye cuaternión a partir de eje-ángulo
        
        Args:
            axis: Eje de rotación (3 elementos)
            angle: Ángulo de rotación en radianes
            
        Returns:
            Cuaternión [q0, q1, q2, q3] donde q0 es la parte escalar
        """
        axis = axis / np.linalg.norm(axis)  # Normalizar
        sin_half = np.sin(angle / 2)
        cos_half = np.cos(angle / 2)
        
        q = np.array([
            cos_half,
            axis[0] * sin_half,
            axis[1] * sin_half, 
            axis[2] * sin_half
        ])
        
        return q
    
    @staticmethod
    def from_rotation_matrix(R: npt.NDArray) -> npt.NDArray:
        """
        Convierte matriz de rotación a cuaternión
        
        Args:
            R: Matriz de rotación 3x3
            
        Returns:
            Cuaternión [q0, q1, q2, q3]
        """
        if not RotationMatrices.is_rotation_matrix(R):
            raise ValueError("La matriz de entrada no es una matriz de rotación válida")
        
        # Diferentes casos para evitar división por cero
        trace = np.trace(R)
        
        if trace > 0:
            S = np.sqrt(trace + 1.0) * 2
            q0 = 0.25 * S
            q1 = (R[2, 1] - R[1, 2]) / S
            q2 = (R[0, 2] - R[2, 0]) / S
            q3 = (R[1, 0] - R[0, 1]) / S
        elif (R[0, 0] > R[1, 1]) and (R[0, 0] > R[2, 2]):
            S = np.sqrt(1.0 + R[0, 0] - R[1, 1] - R[2, 2]) * 2
            q0 = (R[2, 1] - R[1, 2]) / S
            q1 = 0.25 * S
            q2 = (R[0, 1] + R[1, 0]) / S
            q3 = (R[0, 2] + R[2, 0]) / S
        elif R[1, 1] > R[2, 2]:
            S = np.sqrt(1.0 + R[1, 1] - R[0, 0] - R[2, 2]) * 2
            q0 = (R[0, 2] - R[2, 0]) / S
            q1 = (R[0, 1] + R[1, 0]) / S
            q2 = 0.25 * S
            q3 = (R[1, 2] + R[2, 1]) / S
        else:
            S = np.sqrt(1.0 + R[2, 2] - R[0, 0] - R[1, 1]) * 2
            q0 = (R[1, 0] - R[0, 1]) / S
            q1 = (R[0, 2] + R[2, 0]) / S
            q2 = (R[1, 2] + R[2, 1]) / S
            q3 = 0.25 * S
        
        q = np.array([q0, q1, q2, q3])
        return QuaternionOperations.normalize(q)
    
    @staticmethod
    def to_rotation_matrix(q: npt.NDArray) -> npt.NDArray:
        """
        Convierte cuaternión a matriz de rotación
        
        Args:
            q: Cuaternión [q0, q1, q2, q3]
            
        Returns:
            Matriz de rotación 3x3
        """
        q = QuaternionOperations.normalize(q)
        q0, q1, q2, q3 = q
        
        # Matriz de cosenos directores
        R = np.array([
            [1 - 2*(q2**2 + q3**2), 2*(q1*q2 - q0*q3), 2*(q1*q3 + q0*q2)],
            [2*(q1*q2 + q0*q3), 1 - 2*(q1**2 + q3**2), 2*(q2*q3 - q0*q1)],
            [2*(q1*q3 - q0*q2), 2*(q2*q3 + q0*q1), 1 - 2*(q1**2 + q2**2)]
        ])
        
        return R
    
    @staticmethod
    def normalize(q: npt.NDArray) -> npt.NDArray:
        """
        Normaliza un cuaternión
        
        Args:
            q: Cuaternión a normalizar
            
        Returns:
            Cuaternión normalizado
        """
        norm = np.linalg.norm(q)
        if norm == 0:
            raise ValueError("No se puede normalizar un cuaternión cero")
        return q / norm
    
    @staticmethod
    def conjugate(q: npt.NDArray) -> npt.NDArray:
        """
        Calcula el conjugado de un cuaternión
        
        Args:
            q: Cuaternión de entrada
            
        Returns:
            Cuaternión conjugado [q0, -q1, -q2, -q3]
        """
        return np.array([q[0], -q[1], -q[2], -q[3]])
    
    @staticmethod
    def inverse(q: npt.NDArray) -> npt.NDArray:
        """
        Calcula el inverso de un cuaternión (q⁻¹ = q* / ||q||²)
        
        Args:
            q: Cuaternión de entrada
            
        Returns:
            Cuaternión inverso
        """
        q_conj = QuaternionOperations.conjugate(q)
        norm_sq = np.sum(q**2)
        return q_conj / norm_sq
    
    @staticmethod
    def multiply(q1: npt.NDArray, q2: npt.NDArray) -> npt.NDArray:
        """
        Multiplicación de cuaterniones (composición de rotaciones)
        
        Args:
            q1, q2: Cuaterniones a multiplicar
            
        Returns:
            Cuaternión producto q1 ⊗ q2
        """
        q10, q11, q12, q13 = q1
        q20, q21, q22, q23 = q2
        
        q0 = q10*q20 - q11*q21 - q12*q22 - q13*q23
        q1_val = q10*q21 + q11*q20 + q12*q23 - q13*q22
        q2_val = q10*q22 - q11*q23 + q12*q20 + q13*q21
        q3_val = q10*q23 + q11*q22 - q12*q21 + q13*q20
        
        return np.array([q0, q1_val, q2_val, q3_val])
    
    @staticmethod
    def rotate_vector(q: npt.NDArray, v: npt.NDArray) -> npt.NDArray:
        """
        Rota un vector usando un cuaternión
        
        Args:
            q: Cuaternión de rotación
            v: Vector 3D a rotar
            
        Returns:
            Vector rotado
        """
        # Convertir vector a cuaternión puro
        v_quat = np.array([0, v[0], v[1], v[2]])
        
        # Rotación: v' = q ⊗ v ⊗ q⁻¹
        q_inv = QuaternionOperations.inverse(q)
        v_rot_quat = QuaternionOperations.multiply(
            QuaternionOperations.multiply(q, v_quat), q_inv
        )
        
        # Extraer parte vectorial
        return v_rot_quat[1:]
    
    @staticmethod
    def slerp(q1: npt.NDArray, q2: npt.NDArray, t: float) -> npt.NDArray:
        """
        Interpolación esférica lineal (SLERP) entre dos cuaterniones
        
        Args:
            q1, q2: Cuaterniones de inicio y fin
            t: Parámetro de interpolación [0, 1]
            
        Returns:
            Cuaternión interpolado
        """
        q1 = QuaternionOperations.normalize(q1)
        q2 = QuaternionOperations.normalize(q2)
        
        # Calcular coseno del ángulo entre cuaterniones
        cos_half_theta = np.dot(q1, q2)
        
        # Si q2 está en el hemisferio opuesto, usar el cuaternión antipodal
        if cos_half_theta < 0:
            q2 = -q2
            cos_half_theta = -cos_half_theta
        
        # Si los cuaterniones son muy cercanos, usar interpolación lineal
        if cos_half_theta > 0.9995:
            result = q1 + t * (q2 - q1)
            return QuaternionOperations.normalize(result)
        
        half_theta = np.arccos(np.clip(cos_half_theta, -1.0, 1.0))
        sin_half_theta = np.sqrt(1.0 - cos_half_theta**2)
        
        # Evitar división por cero
        if abs(sin_half_theta) < 1e-8:
            return (q1 + q2) / 2
        
        ratio1 = np.sin((1 - t) * half_theta) / sin_half_theta
        ratio2 = np.sin(t * half_theta) / sin_half_theta
        
        return ratio1 * q1 + ratio2 * q2
    
    @staticmethod
    def from_euler_angles(angles: Tuple[float, float, float], 
                         sequence: str = '321') -> npt.NDArray:
        """
        Convierte ángulos de Euler a cuaternión
        
        Args:
            angles: Tupla de 3 ángulos (phi, theta, psi) en radianes
            sequence: Secuencia de ejes (ej: '321' para yaw-pitch-roll)
            
        Returns:
            Cuaternión equivalente
        """
        phi, theta, psi = angles
        
        # Calcular cuaterniones para cada rotación elemental
        if sequence == '321':  # Z-Y-X (yaw-pitch-roll)
            cy = np.cos(psi * 0.5)
            sy = np.sin(psi * 0.5)
            cp = np.cos(theta * 0.5)
            sp = np.sin(theta * 0.5)
            cr = np.cos(phi * 0.5)
            sr = np.sin(phi * 0.5)
            
            q0 = cr * cp * cy + sr * sp * sy
            q1 = sr * cp * cy - cr * sp * sy
            q2 = cr * sp * cy + sr * cp * sy
            q3 = cr * cp * sy - sr * sp * cy
            
        else:
            # Para otras secuencias, usar matrices de rotación
            R = RotationMatrices.euler_sequence(angles, sequence)
            return QuaternionOperations.from_rotation_matrix(R)
        
        return np.array([q0, q1, q2, q3])
    
    @staticmethod
    def to_euler_angles(q: npt.NDArray, sequence: str = '321') -> Tuple[float, float, float]:
        """
        Convierte cuaternión a ángulos de Euler
        
        Args:
            q: Cuaternión de entrada
            sequence: Secuencia de ejes deseada
            
        Returns:
            Tupla de 3 ángulos (phi, theta, psi) en radianes
        """
        q = QuaternionOperations.normalize(q)
        q0, q1, q2, q3 = q
        
        if sequence == '321':  # Z-Y-X (yaw-pitch-roll)
            # Roll (x-axis)
            sinr_cosp = 2 * (q0 * q1 + q2 * q3)
            cosr_cosp = 1 - 2 * (q1**2 + q2**2)
            roll = np.arctan2(sinr_cosp, cosr_cosp)
            
            # Pitch (y-axis)
            sinp = 2 * (q0 * q2 - q3 * q1)
            if abs(sinp) >= 1:
                pitch = np.copysign(np.pi / 2, sinp)  # 90 grados
            else:
                pitch = np.arcsin(sinp)
            
            # Yaw (z-axis)
            siny_cosp = 2 * (q0 * q3 + q1 * q2)
            cosy_cosp = 1 - 2 * (q2**2 + q3**2)
            yaw = np.arctan2(siny_cosp, cosy_cosp)
            
            return roll, pitch, yaw
        else:
            # Para otras secuencias, usar matriz de rotación
            R = QuaternionOperations.to_rotation_matrix(q)
            # Esto requeriría implementar la extracción de ángulos Euler
            # para secuencias arbitrarias
            raise NotImplementedError(f"Secuencia {sequence} no implementada aún")

# Ejemplo de uso y pruebas
if __name__ == "__main__":
    print("🧪 Probando operaciones con cuaterniones...")
    
    # Prueba de creación desde eje-ángulo
    axis = np.array([1, 0, 0])
    angle = np.pi / 2
    q = QuaternionOperations.from_axis_angle(axis, angle)
    print(f"✅ Cuaternión desde eje-ángulo: {q}")
    
    # Prueba de conversión a matriz de rotación
    R = QuaternionOperations.to_rotation_matrix(q)
    print(f"✅ Matriz de rotación:\n{R}")
    
    # Prueba de conversión inversa
    q_recon = QuaternionOperations.from_rotation_matrix(R)
    print(f"✅ Reconstrucción exitosa: {np.allclose(q, q_recon)}")
    
    # Prueba de rotación de vector
    v = np.array([0, 1, 0])
    v_rot = QuaternionOperations.rotate_vector(q, v)
    print(f"✅ Vector rotado: {v} -> {v_rot}")
    
    # Prueba de ángulos Euler
    angles = (np.pi/6, np.pi/4, np.pi/3)
    q_euler = QuaternionOperations.from_euler_angles(angles)
    angles_recon = QuaternionOperations.to_euler_angles(q_euler)
    print(f"✅ Conversión Euler: {angles} -> {angles_recon}")
    
    # Prueba de SLERP
    q1 = QuaternionOperations.from_axis_angle([1, 0, 0], 0)
    q2 = QuaternionOperations.from_axis_angle([1, 0, 0], np.pi/2)
    q_slerp = QuaternionOperations.slerp(q1, q2, 0.5)
    print(f"✅ SLERP intermedio: {q_slerp}")
