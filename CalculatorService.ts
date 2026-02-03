export class CalculatorService {
  
  add(a: number, b: number): number {
    return a + b;
  }
  
  subtract(a: number, b: number): number {
    return a - b;
  }
  
  multiply(a: number, b: number): number {
    return a * b;
  }
  
  divide(a: number, b: number): number {
    if (b === 0) {
      throw new Error('Division by zero');
    }
    return a / b;
  }
  
  power(base: number, exponent: number): number {
    return Math.pow(base, exponent);
  }
  
  squareRoot(n: number): number {
    return Math.sqrt(n);
  }
  
  percentage(value: number, total: number): number {
    return (value / total) * 100;
  }
  
  factorial(n: number): number {
    if (n === 0 || n === 1) return 1;
    return n * this.factorial(n - 1);
  }
}
