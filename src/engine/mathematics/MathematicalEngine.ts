import { Vector3D } from './core/Vector3D';
import { Matrix } from './core/Matrix';

export class MathematicalEngine {
  constructor() {}

  async initialize(): Promise<void> {
    console.log('🧮 Mathematical Engine initialized');
    return Promise.resolve();
  }

  /**
   * Resolver sistema lineal Ax = b
   */
  solveLinearSystem(A: Matrix, b: number[]): number[] {
    if (A.rows !== A.cols) {
      throw new Error("La matriz A debe ser cuadrada");
    }
    if (A.rows !== b.length) {
      throw new Error("Dimensiones incompatibles entre A y b");
    }

    try {
      const A_inv = A.inverse();
      return A_inv.multiplyVector(b);
    } catch (error) {
      throw new Error(`No se pudo resolver el sistema: ${error}`);
    }
  }

  /**
   * Matriz de vista lookAt
   */
  lookAtMatrix(eye: Vector3D, target: Vector3D, up: Vector3D): Matrix {
    const forward = target.subtract(eye).normalize();
    const right = forward.cross(up).normalize();
    const newUp = right.cross(forward);

    return Matrix.fromArray([
      [right.x, right.y, right.z, -right.dot(eye)],
      [newUp.x, newUp.y, newUp.z, -newUp.dot(eye)],
      [-forward.x, -forward.y, -forward.z, forward.dot(eye)],
      [0, 0, 0, 1]
    ]);
  }

  /**
   * Calcular distancia entre dos puntos
   */
  distanceBetweenPoints(p1: Vector3D, p2: Vector3D): number {
    return p1.distanceTo(p2);
  }

  dispose(): void {
    console.log('🧹 Mathematical Engine disposed');
  }
}

export default MathematicalEngine;
