/**
 * Mathematics Module - Exportaciones principales
 */

// Importar las clases
import Vector2D from './core/Vector2D';
import Vector3D from './core/Vector3D';
import Matrix from './core/Matrix';
import Quaternion from './core/Quaternion';
import MathematicalEngine from './MathematicalEngine';

// Re-exportar las clases
export { Vector2D, Vector3D, Matrix, Quaternion, MathematicalEngine };

// Utilidades matemáticas
export const MathUtils = {
  degToRad(degrees: number): number {
    return degrees * (Math.PI / 180);
  },

  radToDeg(radians: number): number {
    return radians * (180 / Math.PI);
  },

  lerp(a: number, b: number, t: number): number {
    return a + (b - a) * t;
  },

  lerpClamped(a: number, b: number, t: number): number {
    return a + (b - a) * Math.max(0, Math.min(1, t));
  },

  map(value: number, inMin: number, inMax: number, outMin: number, outMax: number): number {
    return ((value - inMin) * (outMax - outMin)) / (inMax - inMin) + outMin;
  },

  clamp(value: number, min: number, max: number): number {
    return Math.max(min, Math.min(max, value));
  },

  approximately(a: number, b: number, epsilon: number = 1e-6): boolean {
    return Math.abs(a - b) < epsilon;
  }
};

/**
 * Constantes matemáticas útiles
 */
export const MathConstants = {
  PI: Math.PI,
  TWO_PI: 2 * Math.PI,
  HALF_PI: Math.PI / 2,
  DEG_TO_RAD: Math.PI / 180,
  RAD_TO_DEG: 180 / Math.PI,
  EPSILON: 1e-12,
  GOLDEN_RATIO: 1.618033988749895
};

// Exportación por defecto para importaciones convenientes
const Mathematics = {
  Vector2D,
  Vector3D,
  Matrix,
  Quaternion,
  MathematicalEngine,
  MathUtils,
  MathConstants
};

export default Mathematics;
