/**
 * Matrix - Clase para operaciones matriciales básicas
 */
export class Matrix {
  public rows: number;
  public cols: number;
  public data: number[][];

  constructor(rows: number, cols: number, data?: number[][]) {
    this.rows = rows;
    this.cols = cols;
    this.data = data || Array(rows).fill(0).map(() => Array(cols).fill(0));
  }

  add(m: Matrix): Matrix {
    if (this.rows !== m.rows || this.cols !== m.cols) {
      throw new Error("Dimensiones incompatibles para suma");
    }
    
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] + m.data[i][j];
      }
    }
    return result;
  }

  multiply(scalar: number): Matrix {
    const result = new Matrix(this.rows, this.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[i][j] = this.data[i][j] * scalar;
      }
    }
    return result;
  }

  matmul(m: Matrix): Matrix {
    if (this.cols !== m.rows) {
      throw new Error(`Dimensiones incompatibles: ${this.rows}x${this.cols} × ${m.rows}x${m.cols}`);
    }
    
    const result = new Matrix(this.rows, m.cols);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < m.cols; j++) {
        let sum = 0;
        for (let k = 0; k < this.cols; k++) {
          sum += this.data[i][k] * m.data[k][j];
        }
        result.data[i][j] = sum;
      }
    }
    return result;
  }

  transpose(): Matrix {
    const result = new Matrix(this.cols, this.rows);
    for (let i = 0; i < this.rows; i++) {
      for (let j = 0; j < this.cols; j++) {
        result.data[j][i] = this.data[i][j];
      }
    }
    return result;
  }

  determinant(): number {
    if (this.rows !== this.cols) {
      throw new Error("Solo matrices cuadradas tienen determinante");
    }
    
    if (this.rows === 2) {
      return this.data[0][0] * this.data[1][1] - this.data[0][1] * this.data[1][0];
    }
    
    // Para matrices 3x3
    if (this.rows === 3) {
      return (
        this.data[0][0] * (this.data[1][1] * this.data[2][2] - this.data[1][2] * this.data[2][1]) -
        this.data[0][1] * (this.data[1][0] * this.data[2][2] - this.data[1][2] * this.data[2][0]) +
        this.data[0][2] * (this.data[1][0] * this.data[2][1] - this.data[1][1] * this.data[2][0])
      );
    }
    
    throw new Error("Determinante solo implementado para matrices 2x2 y 3x3");
  }

  inverse(): Matrix {
    if (this.rows !== this.cols) {
      throw new Error("Solo matrices cuadradas tienen inversa");
    }
    
    const det = this.determinant();
    if (Math.abs(det) < 1e-10) {
      throw new Error("Matriz singular, no tiene inversa");
    }
    
    if (this.rows === 2) {
      const invDet = 1 / det;
      return new Matrix(2, 2, [
        [this.data[1][1] * invDet, -this.data[0][1] * invDet],
        [-this.data[1][0] * invDet, this.data[0][0] * invDet]
      ]);
    }
    
    throw new Error("Inversa solo implementada para matrices 2x2");
  }

  multiplyVector(v: number[]): number[] {
    if (this.cols !== v.length) {
      throw new Error("Dimensiones incompatibles");
    }
    
    const result: number[] = [];
    for (let i = 0; i < this.rows; i++) {
      let sum = 0;
      for (let j = 0; j < this.cols; j++) {
        sum += this.data[i][j] * v[j];
      }
      result.push(sum);
    }
    return result;
  }

  toString(): string {
    return `Matrix[${this.rows}x${this.cols}]`;
  }

  static identity(size: number): Matrix {
    const result = new Matrix(size, size);
    for (let i = 0; i < size; i++) {
      result.data[i][i] = 1;
    }
    return result;
  }

  static fromArray(data: number[][]): Matrix {
    const rows = data.length;
    const cols = data[0].length;
    return new Matrix(rows, cols, data.map(row => [...row]));
  }
}

export default Matrix;
