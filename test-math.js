// Cargar los módulos compilados
import('./dist/engine/mathematics/index.js')
  .then(module => {
    const { Vector3D, MathematicalEngine } = module;
    
    console.log('🧪 PRUEBA DEL SISTEMA MATEMÁTICO\n');
    
    const v1 = new Vector3D(1, 2, 3);
    const v2 = new Vector3D(4, 5, 6);
    console.log('Vector1:', v1.toString());
    console.log('Vector2:', v2.toString());
    console.log('Suma:', v1.add(v2).toString());
    
    const engine = new MathematicalEngine();
    console.log('Engine creado correctamente');
    
    console.log('\n✅ PRUEBA COMPLETADA');
  })
  .catch(error => {
    console.error('Error:', error);
  });
