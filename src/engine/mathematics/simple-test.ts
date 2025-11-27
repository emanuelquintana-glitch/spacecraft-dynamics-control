import { Vector2D, Vector3D, Matrix, Quaternion, MathematicalEngine } from './index';

console.log('🧪 PRUEBA SIMPLE DEL SISTEMA MATEMÁTICO\n');

// Prueba básica
const v1 = new Vector3D(1, 2, 3);
const v2 = new Vector3D(4, 5, 6);
console.log('Vector1:', v1.toString());
console.log('Vector2:', v2.toString());
console.log('Suma:', v1.add(v2).toString());

// Prueba del engine
const engine = new MathematicalEngine();
console.log('MathematicalEngine creado correctamente');

// Prueba de distancia
const p1 = new Vector3D(0, 0, 0);
const p2 = new Vector3D(3, 4, 0);
console.log('Distancia:', engine.distanceBetweenPoints(p1, p2));

console.log('\n✅ PRUEBA COMPLETADA');
