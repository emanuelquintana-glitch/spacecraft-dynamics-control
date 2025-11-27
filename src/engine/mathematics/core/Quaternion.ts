/**
 * Quaternion - Clase para rotaciones 3D
 */
import { Vector3D } from './Vector3D';

export class Quaternion {
  public w: number;
  public x: number;
  public y: number;
  public z: number;

  constructor(w: number = 1, x: number = 0, y: number = 0, z: number = 0) {
    this.w = w;
    this.x = x;
    this.y = y;
    this.z = z;
  }

  multiply(q: Quaternion): Quaternion {
    return new Quaternion(
      this.w * q.w - this.x * q.x - this.y * q.y - this.z * q.z,
      this.w * q.x + this.x * q.w + this.y * q.z - this.z * q.y,
      this.w * q.y - this.x * q.z + this.y * q.w + this.z * q.x,
      this.w * q.z + this.x * q.y - this.y * q.x + this.z * q.w
    );
  }

  magnitude(): number {
    return Math.sqrt(this.w * this.w + this.x * this.x + this.y * this.y + this.z * this.z);
  }

  normalize(): Quaternion {
    const mag = this.magnitude();
    if (mag === 0) return new Quaternion(1, 0, 0, 0);
    return new Quaternion(
      this.w / mag,
      this.x / mag,
      this.y / mag,
      this.z / mag
    );
  }

  conjugate(): Quaternion {
    return new Quaternion(this.w, -this.x, -this.y, -this.z);
  }

  rotateVector(v: Vector3D): Vector3D {
    const q = this.normalize();
    const vecQuat = new Quaternion(0, v.x, v.y, v.z);
    const result = q.multiply(vecQuat).multiply(q.conjugate());
    return new Vector3D(result.x, result.y, result.z);
  }

  toString(): string {
    return `Quaternion(${this.w}, ${this.x}i, ${this.y}j, ${this.z}k)`;
  }

  static fromAxisAngle(axis: Vector3D, angle: number): Quaternion {
    const halfAngle = angle / 2;
    const s = Math.sin(halfAngle);
    const normalizedAxis = axis.normalize();

    return new Quaternion(
      Math.cos(halfAngle),
      normalizedAxis.x * s,
      normalizedAxis.y * s,
      normalizedAxis.z * s
    );
  }

  static rotationX(angle: number): Quaternion {
    return Quaternion.fromAxisAngle(new Vector3D(1, 0, 0), angle);
  }

  static rotationY(angle: number): Quaternion {
    return Quaternion.fromAxisAngle(new Vector3D(0, 1, 0), angle);
  }

  static rotationZ(angle: number): Quaternion {
    return Quaternion.fromAxisAngle(new Vector3D(0, 0, 1), angle);
  }
}

export default Quaternion;
