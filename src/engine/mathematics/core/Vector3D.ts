/**
 * Vector3D - Clase para operaciones vectoriales en 3D
 */
export class Vector3D {
  public x: number;
  public y: number;
  public z: number;

  constructor(x: number = 0, y: number = 0, z: number = 0) {
    this.x = x;
    this.y = y;
    this.z = z;
  }

  // Operaciones básicas
  add(v: Vector3D): Vector3D {
    return new Vector3D(this.x + v.x, this.y + v.y, this.z + v.z);
  }

  subtract(v: Vector3D): Vector3D {
    return new Vector3D(this.x - v.x, this.y - v.y, this.z - v.z);
  }

  multiply(scalar: number): Vector3D {
    return new Vector3D(this.x * scalar, this.y * scalar, this.z * scalar);
  }

  magnitude(): number {
    return Math.sqrt(this.x * this.x + this.y * this.y + this.z * this.z);
  }

  normalize(): Vector3D {
    const mag = this.magnitude();
    if (mag === 0) return new Vector3D(0, 0, 0);
    return this.divide(mag);
  }

  divide(scalar: number): Vector3D {
    if (scalar === 0) throw new Error("División por cero");
    return new Vector3D(this.x / scalar, this.y / scalar, this.z / scalar);
  }

  dot(v: Vector3D): number {
    return this.x * v.x + this.y * v.y + this.z * v.z;
  }

  cross(v: Vector3D): Vector3D {
    return new Vector3D(
      this.y * v.z - this.z * v.y,
      this.z * v.x - this.x * v.z,
      this.x * v.y - this.y * v.x
    );
  }

  distanceTo(v: Vector3D): number {
    return this.subtract(v).magnitude();
  }

  toString(): string {
    return `Vector3D(${this.x}, ${this.y}, ${this.z})`;
  }

  clone(): Vector3D {
    return new Vector3D(this.x, this.y, this.z);
  }

  static zero(): Vector3D {
    return new Vector3D(0, 0, 0);
  }

  static unitX(): Vector3D {
    return new Vector3D(1, 0, 0);
  }

  static unitY(): Vector3D {
    return new Vector3D(0, 1, 0);
  }

  static unitZ(): Vector3D {
    return new Vector3D(0, 0, 1);
  }
}

export default Vector3D;
