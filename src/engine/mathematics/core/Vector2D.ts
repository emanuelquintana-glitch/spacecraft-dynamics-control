/**
 * Vector2D - Clase para operaciones vectoriales en 2D
 */
export class Vector2D {
  public x: number;
  public y: number;

  constructor(x: number = 0, y: number = 0) {
    this.x = x;
    this.y = y;
  }

  // Operaciones básicas
  add(v: Vector2D): Vector2D {
    return new Vector2D(this.x + v.x, this.y + v.y);
  }

  subtract(v: Vector2D): Vector2D {
    return new Vector2D(this.x - v.x, this.y - v.y);
  }

  multiply(scalar: number): Vector2D {
    return new Vector2D(this.x * scalar, this.y * scalar);
  }

  magnitude(): number {
    return Math.sqrt(this.x * this.x + this.y * this.y);
  }

  normalize(): Vector2D {
    const mag = this.magnitude();
    if (mag === 0) return new Vector2D(0, 0);
    return this.divide(mag);
  }

  divide(scalar: number): Vector2D {
    if (scalar === 0) throw new Error("División por cero");
    return new Vector2D(this.x / scalar, this.y / scalar);
  }

  dot(v: Vector2D): number {
    return this.x * v.x + this.y * v.y;
  }

  toString(): string {
    return `Vector2D(${this.x}, ${this.y})`;
  }

  clone(): Vector2D {
    return new Vector2D(this.x, this.y);
  }

  static zero(): Vector2D {
    return new Vector2D(0, 0);
  }
}

export default Vector2D;
