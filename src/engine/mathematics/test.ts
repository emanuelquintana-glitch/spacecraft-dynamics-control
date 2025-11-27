/**
 * Pruebas básicas del sistema matemático
 */

import { MathematicsExamples } from './examples';

// Ejecutar pruebas
console.log('🧪 INICIANDO PRUEBAS DEL SISTEMA MATEMÁTICO\n');

try {
  MathematicsExamples.runAllExamples();
  console.log('\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE');
} catch (error) {
  console.error('\n❌ ERROR EN LAS PRUEBAS:', error);
}

