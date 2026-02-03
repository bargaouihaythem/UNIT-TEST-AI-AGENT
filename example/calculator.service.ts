import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
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
    if (n < 0) {
      throw new Error('Cannot calculate square root of negative number');
    }
    return Math.sqrt(n);
  }

  percentage(value: number, percent: number): number {
    return (value * percent) / 100;
  }

  factorial(n: number): number {
    if (n < 0) {
      throw new Error('Factorial of negative number is undefined');
    }
    if (n === 0 || n === 1) {
      return 1;
    }
    return n * this.factorial(n - 1);
  }
}
