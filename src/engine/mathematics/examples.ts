/**
 * Ejemplos de uso del sistema matemático
 */
import { Vector2D, Vector3D, Matrix, Quaternion, MathematicalEngine, MathUtils } from './index';

export class MathematicsExamples {
  /**
   * Ejemplos básicos de Vector2D
   */
  static vector2DExamples(): void {
    console.log('=== VECTOR2D EJEMPLOS ===');
    const v1 = new Vector2D(3, 4);
    const v2 = new Vector2D(1, 2);
    console.log('v1:', v1.toString());
    console.log('v2:', v2.toString());
    console.log('Suma:', v1.add(v2).toString());
    console.log('Producto punto:', v1.dot(v2));
    console.log('Magnitud v1:', v1.magnitude());
  }

  /**
   * Ejemplos avanzados de Vector3D
   */
  static vector3DExamples(): void {
    console.log('\n=== VECTOR3D EJEMPLOS ===');
    const v1 = new Vector3D(1, 0, 0);
    const v2 = new Vector3D(0, 1, 0);
    console.log('v1:', v1.toString());
    console.log('v2:', v2.toString());
    console.log('Producto cruz:', v1.cross(v2).toString());
    console.log('Producto punto:', v1.dot(v2));
    
    // Interpolación lineal
    const v3 = new Vector3D(0, 0, 1);
    const lerped = v1.add(v3.subtract(v1).multiply(0.5));
    console.log('LERP entre v1 y v3:', lerped.toString());
  }

  /**
   * Ejemplos de operaciones matriciales
   */
  static matrixExamples(): void {
    console.log('\n=== MATRIX EJEMPLOS ===');
    // Matriz 2x2
    const A = Matrix.fromArray([
      [1, 2],
      [3, 4]
    ]);
    const B = Matrix.fromArray([
      [5, 6],
      [7, 8]
    ]);
    console.log('Matriz A:');
    console.log(A.toString());
    console.log('Matriz B:');
    console.log(B.toString());
    console.log('A + B:');
    console.log(A.add(B).toString());
    
    // Matriz identidad
    const I = Matrix.identity(2);
    console.log('Matriz identidad 2x2:');
    console.log(I.toString());
    
    // Determinante
    console.log('Determinante de A:', A.determinant());
  }

  /**
   * Ejemplos de cuaterniones para rotaciones 3D
   */
  static quaternionExamples(): void {
    console.log('\n=== QUATERNION EJEMPLOS ===');
    // Rotación de 90 grados alrededor del eje X
    const qx = Quaternion.rotationX(MathUtils.degToRad(90));
    console.log('Quaternion rotación X 90°:', qx.toString());
    
    // Rotación de 45 grados alrededor del eje Y
    const qy = Quaternion.rotationY(MathUtils.degToRad(45));
    console.log('Quaternion rotación Y 45°:', qy.toString());
    
    // Rotar un vector
    const point = new Vector3D(1, 0, 0);
    const rotatedPoint = qx.rotateVector(point);
    console.log('Punto original:', point.toString());
    console.log('Punto rotado:', rotatedPoint.toString());
  }

  /**
   * Ejemplos del motor matemático avanzado
   */
  static engineExamples(): void {
    console.log('\n=== MATHEMATICAL ENGINE EJEMPLOS ===');
    const engine = new MathematicalEngine();
    
    // Transformaciones 3D
    const eye = new Vector3D(0, 0, 5);
    const target = new Vector3D(0, 0, 0);
    const up = new Vector3D(0, 1, 0);
    
    try {
      const viewMatrix = engine.lookAtMatrix(eye, target, up);
      console.log('Matriz de vista lookAt:');
      console.log(viewMatrix.toString());
    } catch (error) {
      console.error('Error creando matriz de vista:', error);
    }
  }

  /**
   * Ejemplo completo: Simulación de rotación orbital
   */
  static orbitalRotationExample(): void {
    console.log('\n=== SIMULACIÓN ROTACIÓN ORBITAL ===');
    // Posición inicial de un satélite
    const satellitePos = new Vector3D(10, 0, 0);
    
    // Crear rotación orbital (45° inclinación)
    const inclination = MathUtils.degToRad(45);
    const orbitalQuaternion = Quaternion.rotationY(inclination);
    
    // Animar rotación
    const steps = 4;
    console.log('Animación orbital:');
    for (let i = 0; i <= steps; i++) {
      const t = i / steps;
      // Rotación progresiva alrededor del eje Y
      const rotationAngle = t * MathUtils.degToRad(360);
      const stepQuaternion = Quaternion.rotationY(rotationAngle);
      
      // Aplicar rotación
      const currentPos = stepQuaternion.rotateVector(satellitePos);
      console.log(`Paso ${i}: ${currentPos.toString()}`);
    }
  }

  /**
   * Ejecutar todos los ejemplos
   */
  static runAllExamples(): void {
    console.log('�� INICIANDO EJEMPLOS DEL SISTEMA MATEMÁTICO AVANZADO\n');
    this.vector2DExamples();
    this.vector3DExamples();
    this.matrixExamples();
    this.quaternionExamples();
    this.engineExamples();
    this.orbitalRotationExample();
    console.log('\n✅ TODOS LOS EJEMPLOS COMPLETADOS');
  }
}

// Ejecutar ejemplos si este archivo se ejecuta directamente
if (require.main === module) {
  MathematicsExamples.runAllExamples();
}
